
def eswp(a):
	# a is assumed 32-bit unsigned int
	a0 = a & 0xff
	a1 = (a & (0xff << 8)) >> 8
	a2 = (a & (0xff << 16)) >> 16
	a3 = (a & (0xff << 24)) >> 24
	# print '%2.2X %2.2X %2.2X %2.2X '%(a0,a1,a2,a3)
	return a0 << 24 | a1 << 16 | a2 << 8 | a3

print eswp(0x112b0000)