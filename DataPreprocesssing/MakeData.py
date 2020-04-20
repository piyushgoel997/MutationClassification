import pandas as pd

uniprot = open("FinalData/uniprot_sprot.fasta").read()

id = ""
seq = ""
sequences = {}
for line in uniprot.split("\n"):
    if len(line) > 0 and line[0] == ">":
        if id is not "":
            sequences[id] = seq
        id = line.split("|")[1]
        seq = ""
    else:
        seq += line

########################################################

mutations = pd.read_csv("FinalData/with_uniprot_ids.csv")

ref_seqs = []
errata = []
for _, row in mutations.iterrows():
    id = row["UNIPROT_ACCESSION"]
    if id.count("-") > 0:
        id = id.split("-")[0]
    if (id in sequences and (sequences[id][row["SEQ_NO"] - 1 - 25: row["SEQ_NO"] + 25].count("U") == 0 and
                             sequences[id][row["SEQ_NO"] - 1 - 25: row["SEQ_NO"] + 25].count("O") == 0)) and \
            not (len(sequences[id][row["SEQ_NO"] - 1 - 25: row["SEQ_NO"] + 25]) < 51 or sequences[id][row["SEQ_NO"] - 1]
                 != row["REF_AA"]):
        ref_seqs.append(sequences[id][row["SEQ_NO"] - 1 - 25: row["SEQ_NO"] + 25])
    else:
        ref_seqs.append("")
        errata.append(id)

mutations["REF_SEQ"] = ref_seqs
mutations = mutations[mutations["REF_SEQ"] != ""]
# mutations = mutations[mutations["REF_SEQ"] != r".*U.*"]
mutations.to_csv("FinalData/final_data.csv")
