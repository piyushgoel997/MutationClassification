import time

import pandas as pd

nos = list(range(13, 22)) + ['X', 'Y']
columns = ["seq", "alt", "class", "species", "strand"]

master_start_time = time.time()


def make_codon_dict():
    path = "AminoAcidCodes"
    f = open(path, 'r')
    file = f.read()
    codon = {}
    for line in file.split("\n"):
        sp = line.split(":")
        aa = sp[0]
        for s in sp[1].split(","):
            codon[s] = aa
    return codon


codon_dict = make_codon_dict()

print("Dict loaded in " + str(time.time() - master_start_time))

for p in nos:
    print("Starting with chr " + str(p))
    chr_start_time = time.time()

    input_file_path = "ProteinSequences/" + "chr" + str(p) + ".data"
    output_file_path = "ProteinSequences/" + "chr" + str(p) + ".data2"
    chr_start_time = time.time()

    data = pd.read_csv(input_file_path, names=columns)
    buffer = []

    print(data.shape)
    print("Data loaded in " + str(time.time() - chr_start_time))

    for idx, row in data.iterrows():

        dna_seq = row["seq"]
        new_row = ""
        normal = True
        for i in range(0, 51):
            codon = dna_seq[3 * i:3 * i + 3]
            if codon not in codon_dict:
                normal = False
                break
            new_row += codon_dict[codon]
        if not normal:
            continue
        new_row += "," + codon_dict[row["alt"]]
        for x in row[2:]:
            new_row += "," + str(x)
        buffer.append(new_row)
        if idx % 1000000 == 0:
            print(str(idx) + "/" + str(data.shape[0]) + " done. Time from the start = " + str(
                time.time() - chr_start_time))

    out = open(output_file_path, 'w')
    for c in columns[:-1]:
        out.write(c+",")
    out.write(columns[-1]+"\n")
    for r in buffer:
        out.write(r + "\n")
    out.close()

    print("Total time taken for chr " + str(p) + " = " + str(time.time() - chr_start_time))

print("Total time = " + str(time.time() - master_start_time))
