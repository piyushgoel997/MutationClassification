nos = list(range(1, 22)) + ['X', 'Y']
print(nos)

for i in nos:
    f = open("chr" + str(i) + ".fa", 'r')
    chr = f.read()
    f.close()
    chr = chr[6:]
    chr = chr.replace("\n", "")
    f = open("chr" + str(i) + ".fa", 'w')
    f.write(chr)
    f.close()
