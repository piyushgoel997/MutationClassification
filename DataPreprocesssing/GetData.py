
# columns = [line.split(":")[0] for line in open("DataColumns").read().split("\n")]
data_path = "PrimateAI Data/demodata/full_set_snp_info.csv"

advance_by = 10000

for k in range(int(1000_000_000 / advance_by)):
    data = pd.read_csv(data_path, skiprows=range(1, 1 + k*advance_by), nrows=advance_by)
    # find the pos of the starting index
    ct = 0
    for idx, row in data.iterrows():
        i = 0
        # print(row['ref_codon'])
        ref_codon = row['ref_codon']
        alt_codon = row['alt_codon']
        replacement = row['alt_nuc']
        if replacement + ref_codon[1:] == alt_codon:
            i = 0
        elif ref_codon[0] + replacement + ref_codon[-1] == alt_codon:
            i = 1
        elif ref_codon[:2] + replacement == alt_codon:
            i = 2
        else:
            i = -1
        if i == -1:
            data['alt_nuc'][idx] = row['ref_nuc']
            data['ref_nuc'][idx] = replacement
            # print(data.loc[idx])
            ct+=1
            # print(idx)

    data.to_csv("new_data.csv", mode='a', header=False)
    print(k)