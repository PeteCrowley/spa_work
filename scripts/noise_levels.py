import matplotlib.pyplot as plt
import numpy as np
from spa.core import spa
from spa.properties import ThresholdProperty

# Load the data
noise_levels = [1, 2, 3, 4, 5]
proportion = 0.8
confidence = 0.9
for noise_level in noise_levels:
    data = [float(line.rstrip()) for line in open(f"data/noise_levels/{noise_level}.txt")]
    result = spa(data, ThresholdProperty(op='<'), prob_threshold=proportion, confidence=confidence)
    low = result.confidence_interval.low
    high = result.confidence_interval.high
    plt.errorbar([(low + high) / 2], [noise_level], xerr=[[(high - low) / 2]], fmt='o')

plt.title(f"Noise Level vs Attack Effectiveness, prop = {proportion}, conf = {confidence},\nbased on about 20 attacks at each noise level")
plt.xlabel("Accuracy (Percent of bytes correct)")
plt.ylabel("Noise Level")
plt.yticks(noise_levels)
plt.savefig(f"figures/aes_noise_level_accuracy_{proportion}prop.png")