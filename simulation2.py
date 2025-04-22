import pandas as pd
import numpy as np
from multiprocessing import Pool, cpu_count
import time
import os

ROWS_PER_BATCH = 250_000  # Adjust to stay within memory limits
NUM_BATCHES = 4           # Total ~1M rows
COLS = 20                 # Lower column count for low RAM

def generate_data(rows, cols):
    return pd.DataFrame(np.random.rand(rows, cols))

def process_chunk(chunk):
    # Simulate heavier CPU work
    for _ in range(5):
        chunk = np.sqrt(np.abs(chunk) + 1e-6)
        chunk = np.log(chunk + 1e-6)
    return chunk.sum().sum()  # Simulate aggregation

def run_pipeline():
    print(f"CPU cores available: {cpu_count()}")
    start = time.time()
    results = []

    with Pool(cpu_count()) as pool:
        for i in range(NUM_BATCHES):
            print(f"Processing batch {i+1}/{NUM_BATCHES}")
            df = generate_data(ROWS_PER_BATCH, COLS)
            chunks = np.array_split(df.values, cpu_count())
            batch_results = pool.map(process_chunk, chunks)
            results.append(sum(batch_results))

    print("Pipeline complete.")
    print("Aggregate Result:", sum(results))
    print("Time taken:", round(time.time() - start, 2), "seconds")

if __name__ == "__main__":
    run_pipeline()

