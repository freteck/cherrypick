import numpy as np
import time
import multiprocessing
from multiprocessing import Pool

def generate_data(size_mb):
    num_elements = (size_mb * 1024 * 1024) // 8  # 8 bytes per float64
    data = np.random.rand(num_elements)
    return data

def matrix_multiply(size):
    A = np.random.rand(size, size)
    B = np.random.rand(size, size)
    return np.dot(A, B)

def sort_large_dataset(data):
    return np.sort(data)

def parallel_matrix_mult(core_id):
    matrix_multiply(1000)
    return f"Core {core_id} done"

def main():
    print("Generating Data...")
    data = generate_data(300)  # Simulate 500MB dataset

    print("Sorting Data...")
    start = time.time()
    sorted_data = sort_large_dataset(data)
    print("Matrix Multiplication...")
    matrix_multiply(1000)  # 1000x1000 matrix
    
    print("Running Parallel Matrix Multiplications...")
    with Pool(processes=multiprocessing.cpu_count()) as pool:
        results = pool.map(parallel_matrix_mult, range(multiprocessing.cpu_count()))
    print("\n".join(results))
    print(f"Total Time: {time.time() - start:.2f} seconds")

if __name__ == "__main__":
    main()

