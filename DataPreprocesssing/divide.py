f = open('pre_final2').read()
i = 0
buffer = []
lines = ""
for l in f.split("\n"):
	if i % 50000 == 49999:
		buffer.append(lines)
		lines = ""
	lines += l + "\n"
	i += 1
buffer.append(lines)

for idx, file in enumerate(buffer):
	f = open("pf" + str(idx), 'w')
	f.write(file)
	f.close()