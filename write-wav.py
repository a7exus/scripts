import struct, math

def eswp(a):
	# a is assumed 32-bit unsigned int
	a0 = a & 0xff
	a1 = (a & (0xff << 8)) >> 8
	a2 = (a & (0xff << 16)) >> 16
	a3 = (a & (0xff << 24)) >> 24
	return a0 << 24 | a1 << 16 | a2 << 8 | a3

# x*1 second
size=3*11025

f=open("test.wav", 'wb')
f.write(struct.pack('II8s', eswp(0x52494646), 2*size+32, 'WAVEfmt '))
f.write(struct.pack('IHHII', 16, 1, 1, 11025, 22050))
# Section ("fmt ") Length, 1 = PCM, Number of channels, sample rate, byterate (all chan)
f.write(struct.pack('HH4s', 2, 16, 'data')) # Bytes/sample (all channels), bits per sample (per channel)

for i in xrange(size):
	# val = (1+math.cos(i/40.0))*(1<<14)
	# print i/10.0, math.cos(i/10.0), val
	if i<size/3:
		val=i%2 * (0x7fff)
	elif i<size/3*2:
		val=i%2 * (0x8000)
	else:
		val=i%2 + (0x7fff)
	f.write(struct.pack('H',val))

f.close()