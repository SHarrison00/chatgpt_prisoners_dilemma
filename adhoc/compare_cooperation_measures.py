import itertools

# generate all possible sequences of length 10 with the characters "H" and "T"
hum_sequences = itertools.product(["C", "B"], repeat=10)
# convert the sequences to strings and store them in a set to eliminate duplicates
hum_sequences = ["".join(seq) for seq in hum_sequences]
# gen "Tit-For-Tat" computer seq
com_sequences = []
for i in range(0, len(hum_sequences)):
    com_sequences.append("C" + hum_sequences[i][0:-1])
# make seq into tuples,
tup_sequences = []
for i in range(0, len(hum_sequences)):
    tup_sequences.append(tuple([hum_sequences[i], com_sequences[i]]))

# set scores
T, R, P, S = 10, 6, 2, 0
assert(T > R > P > S)
def comb_score_for_given_seq(tuple_seq, T, R, P, S):
    hum_seq = tuple_seq[0]
    com_seq = tuple_seq[1]
    comb_score = 0
    for i in range(0, len(hum_seq)):
        outcome = hum_seq[i] + com_seq[i]
        if outcome == "CC":
            comb_score += R+R
        elif outcome == "CB":
            comb_score += T+S
        elif outcome == "BC":
            comb_score += S+T
        elif outcome == "BB":
            comb_score += P+P
    return comb_score
def num_hum_coops_for_given_seq(tuple_seq):
    hum_seq = tuple_seq[0]
    return hum_seq.count("C")

# comb score for each seq
comb_score_seq = []
for tuple_seq in tup_sequences:
    comb_score_seq.append(comb_score_for_given_seq(tuple_seq, T, R, P, S))
# num hum coops for each seq
num_hum_coops_seq = []
for tuple_seq in tup_sequences:
    num_hum_coops_seq.append(num_hum_coops_for_given_seq(tuple_seq))

print(tup_sequences)
print(comb_score_seq)
print(num_hum_coops_seq)

import matplotlib.pyplot as plt

# create the scatterplot
plt.scatter(num_hum_coops_seq, comb_score_seq)

# add labels and title
plt.xlabel("C_h = Number of Human Cooperations")
plt.ylabel("Y_i = Combined Final Score")
plt.title("Distribution for all possible 1024 'Tit-for-Tat' sequences\n" + f"T={T}, R={R}, P={P}, S={S} ")

# show the plot
plt.grid()
plt.show()