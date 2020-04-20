def process_element(element):
    seen = False
    out = ""
    for line in element.split("\n"):
        if not seen and line.count("Description") > 0:
            seen = True
            out += line + "\n"
        elif line.count("ClinVarSet") > 0 or (line.count("<SequenceLocation") > 0 and line.count("GRCh38") > 0):
            out += line + "\n"
    return out


buffer = []


def process_element2(element):
    out = ""
    for line in element.split("\n"):
        if line.count("<SequenceLocation") > 0:
            if line.count("start") > 0:
                start = line.split("start=\"")[1].split("\"")[0]
                stop = line.split("stop=\"")[1].split("\"")[0]
                if start == stop:
                    out += line + "\n"
        else:
            out += line + "\n"

    return out


def process_element3(element):
    out = ""
    for line in element.split("\n"):
        if line.count("<SequenceLocation") > 0:
            if line.count("referenceAlleleVCF=\"") > 0:
                a = line.split("referenceAlleleVCF=\"")[1].split("\"")[0]
                b = line.split("alternateAlleleVCF=\"")[1].split("\"")[0]
                if len(a) == 1 and len(b) == 1:
                    out += line + "\n"
        else:
            out += line + "\n"

    return out


with open("iter8", encoding='utf8') as f:
    element = ""
    ct = 0
    for line in f:
        element += line
        if line[:2] == "</":
            # buffer.append(process_element3(element))
            if element.count("<SequenceLocation") > 1:
                # buffer.append(element)
                print(element)
            ct += 1
            element = ""
    print(ct)


# f = open("iter8", 'w')
# for line in buffer:
#     f.write(line + "\n")
# f.close()

# with open("iter8", encoding='utf8') as f:
#     element = ""
#     desc = {}
#     for line in f:
#         if line.count("Description") > 0:
#             l = line[19:-15]
#             if l in desc:
#                 desc[l] += 1
#             else:
#                 desc[l] = 1
#     print(desc)
#     print(len(desc))


############ final before using chr data
def process(element):
    out = ""
    lines = element.split("\n")

    desc = lines[1][19:-14]
    allowed_desc = ("pathogenic", "pathogenic/likely pathogenic", "likely pathogenic", "benign", "benign/likely benign",
                    "likely benign")
    if desc.lower() not in allowed_desc:
        # print(desc)
        return ""

    i = 2
    seqs = []
    while lines[i][:2] != "</":
        assembly = get_attr(lines[i], "SequenceLocation Assembly")
        assembly_accession_version = get_attr(lines[i], "AssemblyAccessionVersion")
        chr = get_attr(lines[i], "Chr")
        accession = get_attr(lines[i], "Accession")
        pos = get_attr(lines[i], "start")
        ref = get_attr(lines[i], "referenceAlleleVCF")
        alt = get_attr(lines[i], "alternateAlleleVCF")
        seqs.append(
            assembly + "," + assembly_accession_version + "," +
            accession + "," + chr + "," + pos + "," + ref + "," + alt)
        i += 1

    for idx, s in enumerate(seqs):
        out += lines[0][16:-2] + ":" + str(idx + 1) + ","
        out += desc + ","
        out += s + "\n"

    return out


def get_attr(line, attr):
    return line.split(str(attr) + "=\"")[1].split("\"")[0]


buffer = []
with open("iter8", encoding='utf8') as f:
    element = ""
    for line in f:
        element += line
        if line[:2] == "</":
            buffer.append(process(element.strip()))
            element = ""

f = open("pre_final", 'w')
f.write("id:idx,description,assembly,assembly_accession_version,accession,chr,pos,ref,alt\n")
for line in buffer:
    f.write(line)
f.close()
