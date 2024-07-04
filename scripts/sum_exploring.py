import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from spa.core import spa
from spa.properties import ThresholdProperty

# Define the file path to the CSV file
file_path = "data/counts.csv"  

# Read the CSV file into a DataFrame
df = pd.read_csv(file_path)

# Process the 'sum_list' column to convert it from a string to a list of integers
df['sum_list'] = df['sum_list'].apply(lambda x: [int(i) for i in x.split(';')])

def max_second_max_diff(lst):
    sorted_list = sorted(lst, reverse=True)
    return sorted_list[0] - sorted_list[1]

def median_diff(lst):
    sorted_list = sorted(lst, reverse=True)
    return sorted_list[0] - (sorted_list[7] + sorted_list[8]) / 2

def second_greatest(lst):
    sorted_list = sorted(lst, reverse=True)
    return sorted_list[1]

df['max_diff'] = df['sum_list'].apply(max_second_max_diff)
df['median_diff'] = df['sum_list'].apply(median_diff)
df['second_greatest'] = df['sum_list'].apply(second_greatest)

correct_guess_second_greatest = df[df['is_correct'] == True]['second_greatest'].tolist()
incorrect_guess_second_greatest = df[df['is_correct'] == False]['second_greatest'].tolist()

n_values = 500
# Only look at first 500 values of each
correct_guess_second_greatest = correct_guess_second_greatest[:n_values]
incorrect_guess_second_greatest = incorrect_guess_second_greatest[:n_values]

proportion = 0.8
conf = 0.9

result_correct = spa(correct_guess_second_greatest, ThresholdProperty(op='<'), prob_threshold=proportion, confidence=conf)
result_incorrect = spa(incorrect_guess_second_greatest, ThresholdProperty(op='<'), prob_threshold=proportion, confidence=conf)

low_correct = result_correct.confidence_interval.low
high_correct = result_correct.confidence_interval.high
low_incorrect = result_incorrect.confidence_interval.low
high_incorrect = result_incorrect.confidence_interval.high

custom_labels = ["Correct\nGuesses", "Incorrect\nGuesses"]

plt.figure(figsize=(8, 6))
plt.title(f"Measurement Score for Second Best Guess for half-byte based on\n{n_values} guesses each, 500 AES samples each guess\n spa prop={proportion}, conf={conf}")
plt.errorbar([(low_correct + high_correct) / 2], [0.3], xerr=[[(high_correct - low_correct) / 2]], fmt='o', label='Correct Guesses', color='green')
plt.errorbar([(low_incorrect + high_incorrect) / 2], [0.7], xerr=[[(high_incorrect - low_incorrect) / 2]], fmt='o', label='Incorrect Guesses', color='red')
plt.xlabel("Measurement Score of Second Best Guess")
plt.yticks([0.3, 0.7], custom_labels)
plt.ylim(0, 1)
# plt.xlim(3500, 5000)
plt.legend()

plt.savefig(f"figures/second_greatest_{proportion}prop_{conf}conf.png")
