## Objectives:

Develop a memory management simulator to simulate various Page Replacement Algorithms: First In First Out (FIFO), Least Recently Used (LRU), Least Frequency Used (LFU), and Optimal algorithms.

---

## Requirements:

1. **Programming Language & Structure**:
    - Implement the simulator using classes and data structures in any chosen programming language.

2. **User-Friendly Interface**:
    - Create an intuitive interface allowing users to:
        - Input parameters: Sequence of page references, frames in physical memory, and other relevant settings.
        - Visualizations or output mechanisms: Display progression of page replacements and the physical memory state at each step for better comprehension.
        - Logging: Record statistics (e.g., page hits, faults) to facilitate analysis and algorithm comparison.

---

## Program Output:

1. **Page Replacement Log**:
    - Detailed log of each page replacement action: indicating replaced and newly brought pages into physical memory.

2. **Memory State Visualization**:
    - Visual representation illustrating memory state after each replacement: display pages in physical memory and their states (e.g., recently used, frequency counts).

3. **Performance Metrics**:
    - Clear presentation of key metrics like page hit percentage, fault percentage, and other relevant statistics.

4. **Summary Statistics**:
    - Aggregate statistics summarizing the overall performance of each page replacement algorithm.

## Sequence Input Format:

**Number of Page References**:
- Number of page references in the sequence. 
<br>

**Sequence of Page References**:
<br>

- Sequence of page references (e.g., 1 2 3 4 1 2 5 1 2 3).
<br>

**Number of Frames in Physical Memory**:
<br>

- Number of frames in physical memory.

**Example:**
```
10 (number of page references)
1 2 3 4 1 2 5 1 2 3 (sequence of page references)
3 (number of frames in physical memory)
```

