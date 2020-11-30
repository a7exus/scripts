import struct, math, sys

def eswp(a):
	# a is assumed 32-bit unsigned int
	a0 = a & 0xff
	a1 = (a & (0xff << 8)) >> 8
	a2 = (a & (0xff << 16)) >> 16
	a3 = (a & (0xff << 24)) >> 24
	return a0 << 24 | a1 << 16 | a2 << 8 | a3

# x*1 second
size=3*11025

f=open("1.wav", 'rb')

print 'RIFF=%s, size=%d, WAVEfmt =%s'%struct.unpack('4sI8s', f.read(16))
print 'len16=%d, fmt1=%d, channels=%d, Hz=%d, byterate=%d'%struct.unpack('IHHII', f.read(16))
print 'ch*bytes/smpl=%d, bits/smpl=%d'%struct.unpack('HH', f.read(4))
# , data=%s

tag=f.read(4)
print 'tag=%s'%tag
if tag != 'data':
	len,=struct.unpack('I', f.read(4))
	print 'len=%d'%len
	print f.read(len)

tag=f.read(4)
print 'tag=%s'%tag
if tag != 'data':
	print 'tag = %s'%tag
	print 'Giving up'
	sys.exit(1)

N=441000
a=struct.unpack('%dh'%N, f.read(2*N))

#print a
lastsign=False
cnt=0
C=0
newline_cnt=0

for i in a:
	isign = i>=0
	cnt+=1
	C+=1
	if (lastsign and not isign):
		#if cnt==16 or cnt==17: cnt = '..'
		#if cnt==26 or cnt==27 or cnt==28: cnt='++'
		print cnt ,
		cnt=1
		#newline_cnt+=1
	if C%133 == 0:#newline_cnt > 80:
		#newline_cnt=1
		print
	lastsign = isign



# eswp(0x52494646), 2*size+32, 'WAVEfmt '))


#f.write(struct.pack('IHHII', 16, 1, 1, 11025, 22050))
# Section ("fmt ") Length, 1 = PCM, Number of channels, sample rate, byterate (all chan)
#f.write(struct.pack('HH4s', 2, 16, 'data')) # Bytes/sample (all channels), bits per sample (per channel)