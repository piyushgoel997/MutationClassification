import pandas as pd


data = pd.read_csv("Separate/last_last_pre_final")
rng = list(range(1, 22)) + ['X', 'Y']
seq = [""]*len(data)


def get_pos(codon, pos):
    x = 0
    for c in codon:
        if "A" <= c <= "Z":
            return pos - x
        x += 1


for i in rng:
    f = open("Separate/chr" + str(i) + ".fa")
    chr = f.read()
    f.close()
    for idx, row in data.iterrows():
        if row["CHROMOSOME"] == str(i):
            pos = get_pos(row["CODON_CHANGE"].split("/")[0], row["COORDS"])
            seq[idx] = chr[pos-1:pos+2]

############################################

f = open("GenomeSequence/GRCh38_latest_rna.fna").read()
found = False
curr = ""
for line in f.split("\n"):
    if found and line[0] == ">":
        break
    elif found:
        curr += line
    elif line.count("NM_018013") > 0:
        found = True

def make_codon_dict():
    path = "ClinVar/RefTable"
    f = open(path, 'r')
    file = f.read()
    codon = {}
    for line in file.split("\n"):
        sp = line.split(":")
        aa = sp[0]
        for s in sp[1].split(","):
            codon[s] = aa
    return codon

ref_table = make_codon_dict()

ps = ""
for i in range(int(len(curr)/3)):
    ps += ref_table[curr[3*i:3*i+3]]
