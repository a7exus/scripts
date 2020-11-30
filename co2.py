#!/usr/bin/python

import sys, re, glob, time, serial, json, csv, requests
import os.path

influxdb_connection={
  'host': '<hostname>',
  'db': 'db1',
  'user': 'w',
  'password': '<password>'
}

class Co2Meter(object):
    """ TIM10 compataible Co2Meter serial protocol (aka AZ-0004) """

    def __init__(self):
        if os.path.exists('/dev/tty.SLAB_USBtoUART'):
            serial_port='/dev/tty.SLAB_USBtoUART'
        else:
            serial_port=glob.glob('/dev/ttyUSB*')[0]
        self.t_zero=int(time.mktime((2000, 1, 1, 0, 0, 0, 0,0, time.localtime().tm_isdst)))
        self.serial_port=serial_port
        self.ser=serial.Serial(serial_port, timeout=2)
        #self.ser.open()
        
    def getInfo(self):
        self.ser.write(b'I')
        return self.ser.read(21)

    def setDate(self):
        t=str(int(time.time()-self.t_zero))
        self.ser.write(b'C '+t+'\r')
        return self.ser.read(256)

    def getReadings(self):
        self.ser.write(b':')
        return self.ser.read(25)
        #return self.ser.readline()
        
    def getStat(self):
        self.ser.write(b'M')
        return self.ser.read(20)
    
    def setInterval(self, interval):
        self.ser.write(b'S '+str(interval))
        return self.ser.read(200)

    def getLog(self):
        self.ser.write(b'D')
        result=[]
        lastread=b'begin'
        while lastread:
            lastread=self.ser.read(2048)
            print 'Read %d of 2048 bytes'%len(lastread)
            result.append(lastread)
        return ''.join(result)

    def parseLog(self):
        log=self.getLog()
        l={}
        fulllog=[]
        n=0
        for line in log.split('\r'):
            a=line.split()
            if n==0:
                if len(a)!=6: print "ERROR: Wrong data header length"
                if a[0]!='m': print 'ERROR Wrong data header magic. Got: %s. Expected: m'%a[0]
                l['count']=a[1]
                l['interval']=int(a[2])
                if a[3]!='C': print 'ERROR Wrong data header middle magic. Got: %s. Expected: C'%a[3]
                l['timestamp']=int(a[4]+a[5],16)+self.t_zero
                l['time']=time.strftime("%Y-%m-%d %H:%M:%S [%s]", time.localtime(l['timestamp']))
                print l
            else:
                if len(a) > 0:
                    a[0]=l['timestamp']+(l['interval']*n)
                    fulllog.append(a)
            n+=1
        with open('fulllog-%d.json'%int(time.time()), 'w') as f:
            json.dump(fulllog, f, sort_keys=True)
        with open('fulllog-%d.csv'%int(time.time()), 'w') as f:
            csv.writer(f).writerows(fulllog)
        return fulllog

    def send(self, cmd):
        self.ser.write(cmd)
        return self.ser.read(2500)
    
def log(a, *argv):
    print time.strftime('%c', time.localtime()), a, argv

m=Co2Meter()
m.setDate()

while True:
    s=m.getReadings()  #: T22.6C:C1012ppm:H38.8%
    try:
        data = re.search(': T(?P<temp>\d\d\.\d)C:C(?P<co2>\d{3,4})ppm:H(?P<humid>\d\d\.\d)%', s).groupdict()
    except AttributeError:
        log("AttributeError: %s"%s)
        time.sleep(10)
        continue
    log(data)
    url = 'http://%(host)s:8086/write?db=%(db)s&u=%(username)s&p=%(password)s' % influxdb_connection
    linedata = 'temp v=%(temp)s\nhumid v=%(humid)s\nco2 v=%(co2)s\n' % data
    try:
        r=requests.post(url, linedata)
    except requests.exceptions.ConnectionError:
        log("ConnectionError") 
        time.sleep(10)
        continue
    if r.status_code != 204:
        log(r.status_code, r.text)

    sys.stdout.flush()
    time.sleep(58)

#print m.parseLog()
#print m.setInterval(6)
