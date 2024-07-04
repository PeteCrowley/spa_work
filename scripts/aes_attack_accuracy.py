import numpy as np
from spa.core import spa
from spa.properties import ThresholdProperty
import pandas as pd
import matplotlib.pyplot as plt

std_devs = np.linspace(100_000, 10_000_000, 6)

def generate_accuracy_output():
    # Read in data
    data = pd.read_csv('data/AESPrimeProbe.csv')
    true_window = data[data['from_victim/from_noise'] == 'from_victim']
    correct_sets = set(true_window.set)   # Find set of true victim accesses

    def get_captured_sets(start_cycle, end_cycle):
        return set(data[(data['time'] >= start_cycle) & (data['time'] <= end_cycle)].set)

    def get_accuracy(start_cycle, end_cycle):
        # This is definitely wrong
        captured_sets = get_captured_sets(start_cycle, end_cycle)
        correct_captures = captured_sets.intersection(correct_sets)
        num_captured_correct = len(correct_captures)
        num_captured_wrong = len(captured_sets) - num_captured_correct
        num_missed = len(correct_sets) - num_captured_correct
        return num_captured_correct / (num_captured_correct + num_captured_wrong + num_missed)
    

    mean_start = min(true_window['time'])
    mean_end = max(true_window['time'])

    num_trials_per_variance = 50

    for variance in std_devs:
        accuracies = []
        out_file = open(f"data/aes_accuracy_results_{variance}.txt", "w")
        out_file.write("start,end,accuracy,tag\n")
        for _ in range(num_trials_per_variance):
            start = np.random.normal(mean_start, variance)
            end = np.random.normal(mean_end, variance)
            accuracies.append(get_accuracy(start, end))
            out_file.write(f"{start},{end},{get_accuracy(start, end)},accuracy\n")
    
plt.xlabel("Accuracy")
plt.ylabel("Std. Deviation of Window Start/End")
plt.title("Effect of Variance of Timing Window on Accuracy of AES Attack")

for variance in std_devs:
    data = list(pd.read_csv(f"data/aes_accuracy_results_{variance}.txt").accuracy)
    proportion = 0.9
    confidence = 0.9
    result = spa(data, ThresholdProperty(), prob_threshold=proportion, confidence=confidence)
    low = result.confidence_interval.low
    high = result.confidence_interval.high
    plt.errorbar([(low + high) / 2], [variance], xerr=[[(high - low) / 2]], fmt='o')

plt.yticks(std_devs)
plt.savefig("figures/aes_attack_accuracy_vs_stddev.png")


