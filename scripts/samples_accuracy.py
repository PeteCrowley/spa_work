import matplotlib.pyplot as plt
import numpy as np
from spa.core import spa
from spa.properties import ThresholdProperty

# Load the data
num_samples_list = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
proportion = 0.2
confidence = 0.9
for num_samples in num_samples_list:
    data = [int(line.rstrip()) for line in open(f"data/number_of_samples/{num_samples}.txt")]
    result = spa(data, ThresholdProperty(op='<'), prob_threshold=proportion, confidence=confidence)
    low = result.confidence_interval.low
    high = result.confidence_interval.high
    plt.errorbar([(low + high) / 2], [num_samples], xerr=[[(high - low) / 2]], fmt='o')

plt.title(f"Number of Samples vs Attack Effectiveness, prop = {proportion}, conf = {confidence},\nbased on 50 attacks at each number of samples")
plt.xlabel("Number of Correct Half-Bytes")
plt.ylabel("Number of Samples of AES Encryptions")
plt.yticks(num_samples_list)
plt.savefig(f"figures/aes_samples_accuracy_{proportion}prop.png")