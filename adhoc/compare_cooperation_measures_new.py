import numpy as np
import pandas as pd
import itertools
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns

# Generate all possible sequences
def generate_sequences(N):
    # Generate all possible human sequences of length N, converting the sequences to strings and store in a list
    hum_sequences = itertools.product(["C", "B"], repeat=N)
    hum_sequences = ["".join(seq) for seq in hum_sequences]

    # Generate "Tit-For-Tat" computer sequences
    comp_tft_sequences = []
    for i in range(0, len(hum_sequences)):
        comp_tft_sequences.append("C" + hum_sequences[i][0:-1])

    # Generate "Tit-For-Tat" computer sequences
    comp_tftt_sequences = []
    for i in range(0, len(hum_sequences)):
        comp_tftt_sequences.append("B" + hum_sequences[i][0:-1])

    # # Generate "Tit-For-Two-Tat" computer sequences (we build these sequence-by-sequence)
    # comp_tftt_sequences = []
    # for j in range(0, len(hum_sequences)):
    #     hum_sequence = hum_sequences[j]
    #     comp_tftt_sequence = ["C"]
    #     for i in range(2, len(hum_sequence)+1):
    #         # If the human has betrayed twice in a row: retaliate
    #         if hum_sequence[(i-3):(i-1)] == "BB":
    #             comp_tftt_sequence.append("B")
    #         else: comp_tftt_sequence.append("C")
    #     comp_tftt_sequences.append("".join(comp_tftt_sequence))

    # Make a sequence of tuples,
    tup_sequences = []
    for i in range(0, len(hum_sequences)):
        # In each tuple the order is: 1. Human sequence, 2. Corresponding TFT seq., 3. Corresponding TFTT seq.
        tup_sequences.append(tuple([hum_sequences[i], comp_tft_sequences[i], comp_tftt_sequences[i]]))
    return tup_sequences
# Function that does "what it says on the tin"
def calculate_coop_measures(N, T, R, P, S):
    assert (T > R > P > S)
    assert (2*R > T + S)
    # Generate all possible sequences
    tup_sequences = generate_sequences(N)
    # Initialise columns to store possible game sequences and measures
    hum_seq_col, com_seq_col, strategy_col, comb_score_col, hum_coop_col = [], [], [], [], []

    for i in range(0, len(tup_sequences)):
        # Initialise sequences
        tuple_seq = tup_sequences[i]
        hum_seq = tuple_seq[0]
        com_tft_seq = tuple_seq[1]
        com_tftt_seq = tuple_seq[2]

        # For each computer sequence (strategy)
        for index, com_seq in enumerate([com_tft_seq, com_tftt_seq]):
            comb_score = 0
            for j in range(1, len(hum_seq)):

                outcome = hum_seq[j] + com_seq[j]
                if outcome == "CC":
                    comb_score += R+R
                elif outcome == "CB":
                    comb_score += T+S
                elif outcome == "BC":
                    comb_score += S+T
                elif outcome == "BB":
                    comb_score += P+P
            # Append to columns
            hum_seq_col.append(hum_seq)
            com_seq_col.append(com_seq)
            strategy_col.append("TFT-Coop start" if index == 0 else "TFT-Betray start")
            comb_score_col.append(comb_score)
            hum_coop_col.append(hum_seq.count("C"))

    # Convert all games into a DataFrame
    return pd.DataFrame({'human_sequence': hum_seq_col, 'computer_sequence': com_seq_col,
                                 'strategy': strategy_col, 'combined_score': comb_score_col,
                                 'human_cooperations': hum_coop_col})

# Initialise how many subplots
fig, axes = plt.subplots(1, 2, figsize=(15, 5))

# Left-hand-side plot
N, T, R, P, S = 10, 8, 5, 0, -2
df_all_games = calculate_coop_measures(N, T, R, P, S)
axes[0].set_xlim(df_all_games["combined_score"].min(), df_all_games["combined_score"].max())
sns.stripplot(ax=axes[0], data = df_all_games, x = 'human_cooperations', y = 'combined_score', hue = 'strategy', jitter=True).set(title=f"N={N},\nT={T}, R={R}, P={P}, S={S} ")

# Right-hand-side plot
N, T, R, P, S = 10, 8, 5, 0, -2
df_all_games = calculate_coop_measures(N, T, R, P, S)
axes[1].set_xlim(df_all_games["combined_score"].min(), df_all_games["combined_score"].max())
sns.stripplot(ax=axes[1], data = df_all_games, x = 'human_cooperations', y = 'combined_score', hue = 'strategy', jitter=True).set(title=f"N={N},\nT={T}, R={R}, P={P}, S={S} ")

# Show results
plt.show()