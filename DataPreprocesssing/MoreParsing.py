import pandas as pd

data = pd.read_csv("New Folder/results0.tsv", sep="\t")
for i in range(1, 10):
    d = pd.read_csv("New folder/results" + str(i) + ".tsv", sep="\t")
    data = pd.concat([data, d], ignore_index=True)

data = data[["CHROMOSOME", "COORDS", "CODON_CHANGE"]]
data = data[data["CODON_CHANGE"] != "-"]
data.to_csv("last_pre_final")

pf = pd.read_csv("pre_final")
data = pd.read_csv("last_pre_final")

idx = 0
description = []
alt = []
for _, row in pf.iterrows():
    if idx >= len(data):
        print(row)
    elif data.loc[idx]['CHROMOSOME'] == row['chr'] and data.loc[idx]['COORDS'] == row['pos']:
        description.append(row['description'])
        description.append(row['alt'])
        idx += 1

data['DESC'] = description
data['ALT'] = alt
data.to_csv("Separate/last_last_pre_final")

####################################################################

import pandas as pd

data = pd.read_csv("ClinVar/New Folder/results0.tsv", sep="\t")
for i in range(1, 10):
    d = pd.read_csv("ClinVar/New folder/results" + str(i) + ".tsv", sep="\t")
    data = pd.concat([data, d], ignore_index=True)

data = data[["SEQ_NO", "UNIPROT_ACCESSION", "AA_CHANGE", "CHROMOSOME", "COORDS"]]
with_desc = pd.read_csv("ClinVar/pre_final")[["chr", "pos", "description"]]

idx = 0
description = []
for _, row in with_desc.iterrows():
    if idx > len(data):
        break
    elif data.loc[idx]['CHROMOSOME'] == row['chr'] and data.loc[idx]["COORDS"] == row['pos']:
        description.append(row['description'])
        idx += 1

data["DESCRIPTION"] = description
data = data[["SEQ_NO", "UNIPROT_ACCESSION", "AA_CHANGE", "DESCRIPTION"]]
data = data[data["AA_CHANGE"] != "-"]

ref = []
alt = []

for _, row in data.iterrows():
    ref.append(row["AA_CHANGE"].split("/")[0])
    alt.append(row["AA_CHANGE"].split("/")[1])

data["REF_AA"] = ref
data["ALT_AA"] = alt
data = data[["SEQ_NO", "UNIPROT_ACCESSION", "REF_AA", "ALT_AA", "DESCRIPTION"]]
data = data[data["ALT_AA"] != "*"]

data.to_csv("with_uniprot_ids.csv", index=False)