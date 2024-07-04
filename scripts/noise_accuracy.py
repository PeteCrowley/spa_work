import matplotlib.pyplot as plt
import pandas
import numpy

data = pandas.read_csv('data/noise_accuracy.csv')
plt.title("Average Number of Noise Accesses vs Success Rate")
plt.xlabel("Average Number of Noise Accesses per Prime Probe Attack")
plt.ylabel("Success Rate (Number of Correct Bytes / 16)")
plt.scatter(data['average number of noise'], data[' success rate'])
plt.savefig("figures/noise_vs_success_rate.png")
