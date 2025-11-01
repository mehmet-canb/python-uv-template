"""Example benchmark script with timing.

This file demonstrates how to write performance benchmarks and metric-based
evaluation scripts, particularly useful for AI/ML workflows.
Shows how to import and benchmark functions from the app package.
"""

import time
from typing import Any

from app.main import add_numbers, calculate_factorial, greet


def benchmark_function(func: Any, *args: Any, **kwargs: Any) -> tuple[Any, float]:
    """Benchmark a function and return its result and execution time.

    Uses time.perf_counter for high-resolution timing. The provided args and kwargs
    are passed directly to the function being benchmarked.

    Parameters:
        - func(Any): The function to benchmark
        - *args(Any): Positional arguments to pass to the function
        - **kwargs(Any): Keyword arguments to pass to the function

    Returns:
        - tuple[Any, float]: A tuple of (result, execution_time_in_seconds)
    """
    start_time = time.perf_counter()
    result = func(*args, **kwargs)
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    return result, execution_time


def main() -> None:
    """Run benchmark examples.

    Demonstrates various benchmarking approaches for the app package functions.

    Returns:
        - None: This function doesn't return anything
    """
    print("=" * 60)
    print("Example Benchmark Script")
    print("=" * 60)

    # Benchmark 1: Greet function (string operations)
    print("\nBenchmark 1: Greet Function")
    print("-" * 60)
    iterations = 100_000
    start = time.perf_counter()
    for i in range(iterations):
        greet("Benchmark")
    end = time.perf_counter()
    total_time = end - start
    print(f"Iterations: {iterations:,}")
    print(f"Total time: {total_time:.6f}s")
    print(f"Time per call: {(total_time / iterations) * 1_000_000:.3f}μs")

    # Benchmark 2: Add numbers function
    print("\nBenchmark 2: Add Numbers Function")
    print("-" * 60)
    iterations = 1_000_000
    start = time.perf_counter()
    for i in range(iterations):
        add_numbers(i, i + 1)
    end = time.perf_counter()
    total_time = end - start
    print(f"Iterations: {iterations:,}")
    print(f"Total time: {total_time:.6f}s")
    print(f"Time per call: {(total_time / iterations) * 1_000_000:.3f}μs")

    # Benchmark 3: Factorial calculation (computational)
    print("\nBenchmark 3: Factorial Calculation")
    print("-" * 60)
    for n in [10, 50, 100, 200]:
        result, exec_time = benchmark_function(calculate_factorial, n)
        print(
            f"factorial({n:3d}) = {len(str(result))} digits |"
            f" Time: {exec_time * 1_000_000:.3f}μs"
        )

    # Benchmark 4: String vs integer operations
    print("\nBenchmark 4: Operation Comparison")
    print("-" * 60)

    def string_operations(n: int) -> None:
        for i in range(n):
            _ = greet(f"User{i}")

    def math_operations(n: int) -> None:
        for i in range(n):
            _ = add_numbers(i, i * 2)

    n = 10_000
    _, time1 = benchmark_function(string_operations, n)
    _, time2 = benchmark_function(math_operations, n)

    print(f"String operations ({n:,} calls): {time1:.6f}s")
    print(f"Math operations ({n:,} calls):   {time2:.6f}s")
    print(f"Ratio: {time1 / time2:.2f}x")

    print("\n" + "=" * 60)
    print("Benchmark complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
