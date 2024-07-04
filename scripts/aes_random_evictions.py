import pandas
import numpy as np
import random
from spa.core import spa
from spa.dataclasses import SPAResult
from spa.properties import ThresholdProperty
import matplotlib.pyplot as plt
import os

num_logs = 20
successes = []


def count_noise_acceses(data):
    return len(data[data['attacker/noise'] == 'noise'])

def find_overlap_time(data, ind):
    target_set = data['set'][ind]
    for i in range(ind+1,len(data['time'])):
        if data['set'][i] == target_set and data['victim/attack'][i] == "attack":
            return data['time'][i] - data['time'][ind]
    return None

def get_number_of_overlap(data, ind):
    target_set = data['set'][ind]
    count = 0
    # start_point = ind + 1
    start_point = 0
    for i in range(start_point,len(data['time'])):
        if data['set'][i] == target_set and data['attacker/noise'][i] == 'noise':
            count += 1
    return count

def get_time_til_next_noise(data, ind):
    for i in range(ind+1, len(data['time'])):
        if data['attacker/noise'][i] == 'noise':
            return data['time'][i] - data['time'][ind]
    return None

def pre_process_data_for_cycles() -> list[list[int]]:
    """
    Turn from list of accesses and times to number of accesses from noise after attacker
    """
    for i in range(1, num_logs+1):
        number_of_noise_overlaps = []
        try:
            data = pandas.read_csv(f'data/second_aes_logs/Exec_mt_filter_{i}_success.csv')
            successes.append(True)
        except FileNotFoundError:
            data = pandas.read_csv(f'data/second_aes_logs/Exec_mt_filter_{i}_fail.csv')
            successes.append(False)
        for t in range(len(data['time'])):
            if data['attacker/noise'][t] != 'noise':
                continue
            else:
                time_til_noise = get_time_til_next_noise(data, t)
                if time_til_noise is not  None:
                    number_of_noise_overlaps.append(time_til_noise)
            
        with open(f'data/NoiseCycles{i}.txt', 'w') as file:
            for num in number_of_noise_overlaps:
                file.write(f"{num}\n")

def pre_process_data_for_overlap() -> list[list[int]]:
    """
    Turn from list of accesses and times to number of accesses from noise after attacker
    """
    for i in range(1, num_logs+1):
        number_of_noise_overlaps = []
        try:
            data = pandas.read_csv(f'data/second_aes_logs/Exec_mt_filter_{i}_success.csv')
            successes.append(True)
        except FileNotFoundError:
            data = pandas.read_csv(f'data/second_aes_logs/Exec_mt_filter_{i}_fail.csv')
            successes.append(False)
        for t in range(len(data['time'])):
            if data['attacker/noise'][t] != 'attacker':
                continue
            else:
                num_overlap = get_number_of_overlap(data, t)
                number_of_noise_overlaps.append(num_overlap)
            
        with open(f'data/OverlapNumbers{i}.txt', 'w') as file:
            for num in number_of_noise_overlaps:
                file.write(f"{num}\n")


def create_confidence_intervals(prop) -> list[int, int]:
    confidence_intervals = []
    for i in range(1, num_logs + 1):
        file = f'data/NoiseCycles{i}.txt'
        # file = f'data/OverlapNumbers{i}.txt'
        overlap_times = [int(line.strip()) for line in open(file)]
        confidence = 0.9
        result = spa(overlap_times, ThresholdProperty(op='<'), prob_threshold=prop, confidence=confidence)
        print(result.confidence_interval.low, result.confidence_interval.high)
        # print(result.result_detail)
        confidence_intervals.append((result.confidence_interval.low, result.confidence_interval.high))
    return confidence_intervals


def plot_confidence_intervals(confidence_intervals: list[tuple[int]], prop):
    plt.title(f"Cycles Between Each Noise Access\nProp={prop}, Conf = 0.9 (Green Success, Red Failure)")
    plt.xlabel("Number of Cycles")
    # plt.title(f"Number of Noise Overlap For Attack Access\nProp={prop}, Conf = 0.9 (Green Success, Red Failure)")
    # plt.xlabel("Number of Overlaps")
    plt.ylabel("Trial Number")
    for i in range(len(confidence_intervals)):
        color = 'green' if successes[i] else 'red'
        low, high = confidence_intervals[i]
        plt.errorbar([(low + high) / 2], [i], xerr=[[(high - low) / 2]], fmt='o', color=color)
    plt.savefig("figures/aes_random_evictions_cycles.png")
    # plt.savefig(f"figures/aes_random_evictions_overlap.png")


def plot_average_conf_intervals(confidence_intervals: list[tuple[int]], prop):
    success_high = 0
    succes_low = 0
    failure_high = 0
    failure_low = 0
    success_count = 0
    for i in range(len(confidence_intervals)):
        low, high = confidence_intervals[i]
        if successes[i]:
            success_high += high
            succes_low += low
            success_count += 1
        else:
            failure_high += high
            failure_low += low
    success_high /= success_count
    succes_low /= success_count
    failure_high /= num_logs - success_count
    failure_low /= num_logs - success_count
    plt.clf()
    plt.title(f"Average Confidence Intervals for Time Between Noise (Green Success, Red Failure), Prop={prop}")
    plt.xlabel("Cycles Between Noise Accesses")
    # plt.title(f"Average Number of Noise Overlap For Attack Access\nProp={prop}, Conf = 0.9 (Green Success, Red Failure)")
    # plt.xlabel("Number of Overlaps")
    plt.errorbar([(succes_low + success_high) / 2], [0], xerr=[[(success_high - succes_low) / 2]], fmt='o', color='green')
    plt.errorbar([(failure_low + failure_high) / 2], [1], xerr=[[(failure_high - failure_low) / 2]], fmt='o', color='red')
    # plt.savefig(f"figures/aes_random_evictions_overlap_avg.png")
    plt.savefig(f"figures/aes_random_evictions_cycles_avg.png")


def specific_values():
    
    noise_counts = []
    for i in range(1, num_logs+1):
        try:
            data = pandas.read_csv(f'data/second_aes_logs/Exec_mt_filter_{i}_success.csv')
            successes.append(True)
        except FileNotFoundError:
            data = pandas.read_csv(f'data/second_aes_logs/Exec_mt_filter_{i}_fail.csv')
            successes.append(False)
        count = count_noise_acceses(data)
        plt.plot(count, i, color='green' if successes[i-1] else 'red', marker='o')
    plt.title("Number of Noise Accesses For Each Trial (Green Success, Red Failure)")
    plt.xlabel("Number of Noise Accesses")
    plt.ylabel("Trial Number")
    plt.savefig("figures/aes_random_evictions_noise_counts.png")
    



if __name__ == "__main__":
    specific_values()
    # prop = 0.3
    # confidence_intervals = create_confidence_intervals(prop)
    # print("Confideince Intervals Calculated")
    # # for prop in [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]:
    # #     confidence_intervals = create_confidence_intervals(prop)
    # plot_confidence_intervals(confidence_intervals, prop)
    # plot_average_conf_intervals(confidence_intervals, prop)


