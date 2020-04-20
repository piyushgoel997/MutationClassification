import time

import pandas as pd

nos = list(range(2, 22)) + ['X', 'Y']
columns = [line.split(":")[0] for line in open("DataColumns").read().split("\n")]

master_start_time = time.time()

for p in nos:
    print("Starting with chr " + str(p))
    chr_start_time = time.time()

    errors = []
    probs = []

    data_file_path = "Chromosome Data/" + "chr" + str(p) + ".fa"
    csv_file_path = "Chromosome Data/" + "chr" + str(p) + ".csv"
    output_file_path = "Chromosome Data/" + "chr" + str(p) + ".data"
    queries = pd.read_csv(csv_file_path, names=columns)  # TODO
    sequence = open(data_file_path, 'r').read()
    output = open(output_file_path, 'w')
    print(queries.shape)
    print("Data loaded in " + str(time.time() - chr_start_time))
    buffer = []

    for idx, row in queries.iterrows():
        ref_codon = row['ref_codon']
        alt_codon = row['alt_codon']
        if row['strand'] == 1:
            replacement = row['alt_nuc']
        else:
            replacement = row['ref_nuc']
            opp = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'A'}
            replacement = opp[replacement]

        i = 0
        if replacement + ref_codon[1:] == alt_codon:
            i = 0
        elif ref_codon[0] + replacement + ref_codon[-1] == alt_codon:
            i = 1
        elif ref_codon[:2] + replacement == alt_codon:
            i = 2
        else:
            errors.append(row)

        if str(ref_codon).upper() != sequence[row['pos'] - i - 1:row['pos'] - i + 2].upper():
            # print(str(ref_codon).upper(), sequence[row['pos'] - i - 1:row['pos'] - i + 2].upper())
            probs.append(row)
        else:
            buffer.append(
                sequence[row['pos'] - i - 1 - 75:row['pos'] - i + 2 + 75].upper() + "," + alt_codon + "," + row[
                    'label'] + "," + row['species'] + "," + str(row['strand']))
            # if row['strand'] == 0:
            #     print(row)
            #     print(sequence[row['pos'] - i - 1 - 75:row['pos'] - i + 2 + 75].upper() + "," + alt_codon + "," + row[
            #         'label'] + "," + row['species'] + "," + str(row['strand']))
        if idx % 1000000 == 0:
            print(str(idx) + "/" + str(queries.shape[0]) + " done. Time from the start = " + str(
                time.time() - chr_start_time))
    print("processed in " + str(time.time() - chr_start_time))
    for line in buffer:
        output.write(line + "\n")
    output.close()
    print("Total time taken for chr " + str(p) + " = " + str(time.time() - chr_start_time))
    print(len(errors))
    print(len(probs))
print("Total time = " + str(time.time() - master_start_time))
# print(probs)

# for k in range(int(1000_000_000 / advance_by)):
#     data = pd.read_csv(data_path, skiprows=range(1, 1 + k * advance_by), nrows=advance_by)
#     # find the pos of the starting index
#     ct = 0
#     for idx, row in data.iterrows():
#         i = 0
#         # print(row['ref_codon'])
#         ref_codon = row['ref_codon']
#         alt_codon = row['alt_codon']
#         replacement = row['alt_nuc']
#         if replacement + ref_codon[1:] == alt_codon:
#             i = 0
#         elif ref_codon[0] + replacement + ref_codon[-1] == alt_codon:
#             i = 1
#         elif ref_codon[:2] + replacement == alt_codon:
#             i = 2
#         else:
#             i = -1
#         if i == -1:
#             data['alt_nuc'][idx] = row['ref_nuc']
#             data['ref_nuc'][idx] = replacement
#             # print(data.loc[idx])
#             ct += 1
#             # print(idx)
#
#     data.to_csv("new_data.csv", mode='a', header=False)
#     print(k)
