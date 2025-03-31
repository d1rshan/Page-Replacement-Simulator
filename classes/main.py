import fifo as f
import lfu as lf
import lru as lr
import hybrid as h
import input_taker as i
import os
import matplotlib.pyplot as plt
import numpy as np
import time
from tabulate import tabulate

test = i.SequenceTaker("temp")

def clear():
    return os.system('cls' if os.name == 'nt' else 'clear')

def menu():
    print('+-----------------------------------------+')
    print('|--- * Page Replacement Simulation * ---|')
    print('+-----------------------------------------+')
    print("[1] FIFO  - First In First Out")
    print("[2] LRU   - Least Recently Used")
    print("[3] LFU   - Least Frequently Used")
    print("[4] Hybrid - Our Optimal Implementation")
    print("[5] Compare All Algorithms")
    print("\n[0] Exit")
    print()

def execute_algorithm(algorithm):
    input_path = "input.txt"
    test.retake_sequence(input_path)
    
    start_time = time.time()
    if algorithm == "FIFO":
        instance = f.FIFO(test.sequence, test.frames, test.process_count)
    elif algorithm == "LRU":
        instance = lr.LRU(test.sequence, test.frames, test.process_count)
    elif algorithm == "LFU":
        instance = lf.LFU(test.sequence, test.frames, test.process_count)
    elif algorithm == "Hybrid":
        instance = h.Hybrid(test.sequence, test.frames, test.process_count)
    end_time = time.time()
    
    exec_time = end_time - start_time
    return instance, exec_time

def compare_algorithms():
    algorithms = ["FIFO", "LRU", "LFU", "Hybrid"]
    fault_rates, hit_rates, efficiencies, exec_times = [], [], [], []
    
    results = []
    for algo in algorithms:
        instance, exec_time = execute_algorithm(algo)
        fault_rate = instance.get_page_fault_rate() * 100
        hit_rate = instance.get_page_hit_rate() * 100
        efficiency = hit_rate / fault_rate if fault_rate != 0 else float('inf')
        
        fault_rates.append(fault_rate)
        hit_rates.append(hit_rate)
        efficiencies.append(efficiency)
        exec_times.append(exec_time)
        
        results.append([algo, f"{fault_rate:.2f}%", f"{hit_rate:.2f}%", f"{efficiency:.2f}", f"{exec_time:.5f}s"])
    
    print("\nComparison Table:\n")
    print(tabulate(results, headers=["Algorithm", "Fault Rate", "Hit Rate", "Efficiency", "Time Taken"], tablefmt="fancy_grid"))
    
    x = np.arange(len(algorithms))
    width = 0.35
    
    # Hit Rate vs Fault Rate Graph
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(x - width/2, fault_rates, width, label='Fault Rate (%)')
    ax.bar(x + width/2, hit_rates, width, label='Hit Rate (%)')
    ax.set_ylabel('Percentage')
    ax.set_title('Page Replacement - Hit vs Fault Rate')
    ax.set_xticks(x)
    ax.set_xticklabels(algorithms)
    ax.legend()
    plt.show()
    
    # Efficiency Graph
    plt.figure(figsize=(8, 5))
    plt.bar(algorithms, efficiencies, color='green')
    plt.xlabel('Algorithms')
    plt.ylabel('Efficiency (Hit Rate / Fault Rate)')
    plt.title('Algorithm Efficiency Comparison')
    plt.show()
    
    # Execution Time Graph
    plt.figure(figsize=(8, 5))
    plt.bar(algorithms, exec_times, color='orange')
    plt.xlabel('Algorithms')
    plt.ylabel('Execution Time (seconds)')
    plt.title('Execution Time Comparison')
    plt.show()

def main():
    algorithms = {
        "1": "FIFO",
        "2": "LRU",
        "3": "LFU",
        "4": "Hybrid"
    }
    
    while True:
        clear()
        menu()
        choice = input("Enter choice: ")
        print()
        
        if choice == "0":
            clear()
            print("Exiting...")
            return
        elif choice == "5":
            clear()
            compare_algorithms()
            input("\nPress Enter to return to the menu...")
            continue
        
        algorithm = algorithms.get(choice)
        if algorithm:
            try:
                clear()
                execute_algorithm(algorithm)
                input("\nPress Enter to return to the menu...")
            except Exception as e:
                clear()
                print(f"An error occurred: {str(e)}")
                input("\nPress Enter to continue...")
        else:
            clear()
            print("Invalid input. Please choose a valid option.")
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
