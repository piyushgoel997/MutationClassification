import time

############ set vars

data_file_path = "uniprot_sprot.dat"
start_time = time.time()

############ actual work

f = open(data_file_path)
content = f.read()
print("Time taken to read the contents of the file " + str(time.time() - start_time))

c_time = time.time()
ct = 0
muts = 0
tm = 0
num_humans = 0
buffer = []
for entry in content.split("\n//\n"):
    ct += 1
    temp = entry.count("VARIANT")
    human = entry.count("HUMAN")
    if human > 0:
        num_humans += 1
        if temp > 0:
            muts += 1
            buffer.append(entry)
        tm += temp

human_muts = open("human_seqs.dat", 'w')
for entry in buffer:
    human_muts.write(entry + "\n//\n")
human_muts.close()

print("Total entries = " + str(ct))
print("Entries with humans " + str(num_humans))
print("Entries with humans and mutations = " + str(muts))
print("Number of human mutations = " + str(tm))
print("Time taken to go through all the entries = " + str(time.time() - c_time))

###########################


human_muts = open("human_seqs.dat", 'r').read()
buffer = []
keep = ("ID", "FT", "SQ", "//", "  ")
for line in human_muts.split("\n"):
    if line[:2] in keep:
        buffer.append(line)

cleaned_data = open("human_seqs2.dat", 'w')
for line in buffer:
    cleaned_data.write(line + "\n")

cleaned_data.close()

###########################

cleaned_data = open("human_seqs2.dat", 'r').read().split("\n")
buffer = []

add = False
for line in cleaned_data:
    if line[0:2] == "ID" or line[0:2] == "//":
        buffer.append(line)
    if add:
        if line[0:5] != "     " and line[0:6] != "FT    ":
            add = False
        else:
            buffer.append(line[5:])
    if line[0:12] == "FT   VARIANT" or line[0:2] == "SQ":
        add = True
        buffer.append(line[5:])

next_iter = open("human_seqs3.dat", 'w')
for line in buffer:
    next_iter.write(line + "\n")
next_iter.close()


#############################################
def process_var(var):
    l = ""
    l += var[0].split("         ")[1] + ","
    l += var[1].strip()[7:13].replace(" ", "") + ","
    lines = ""
    for v in var[1:]:
        lines += v.strip() + " "
    if lines.count("(") > 0:
        l += lines.split("(")[1].split(")")[0]
    l += ","
    l += var[-1].strip()[5:-1]
    return l


def process_seq(seq):
    op = ""
    for line in seq[1:]:
        op += line.strip()
    return op.replace(" ", "")


def format_entry(id, vars, seq):
    op = ""
    op += id + ",["
    for v in vars:
        op += v + ","
    op += "],"
    op += seq
    return op


cleaned_data = open("human_seqs3.dat", 'r').read().split("\n//\n")
buffer = []

for entry in cleaned_data:
    if len(entry) == 0:
        break
    lines = entry.split("\n")
    #### process id
    id = lines[0].split("   ")[1]

    #### process variants
    i = 1
    vars = []
    while lines[i][0] == 'V':
        j = i + 1
        while lines[j][0] == ' ':
            j += 1
        vars.append(process_var(lines[i:j]))
        i = j

    #### process sequence
    seq = process_seq(lines[i:])

    buffer.append(format_entry(id, vars, seq))

next_iter = open("human_seqs4.dat", 'w')
for line in buffer:
    next_iter.write(line + "\n")
next_iter.close()
