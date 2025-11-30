import time
from concurrent.futures import ProcessPoolExecutor, as_completed
import pandas as pd
from tqdm import tqdm


def slow_square(x: int) -> int:
    """
    Demo CPU-ish function that:
    - Sleeps for a bit (simulating work that takes time)
    - Returns x squared

    With ProcessPoolExecutor this would normally be something CPU-heavy
    (e.g., big numeric loop, image processing, etc.).
    """
    sleep_time = 6 - x  # different sleep times so tasks finish out of order
    time.sleep(sleep_time)
    return x * x


def run_in_processes(values):
    """
    Run slow_square(x) concurrently using ProcessPoolExecutor,
    track progress with tqdm, and map results back to original input order.
    """
    # Preallocate results so we can store outputs by original index
    results = [None] * len(values)

    # Use ProcessPoolExecutor to run tasks in separate processes.
    # Good for CPU-bound work since each process gets its own Python interpreter.
    with ProcessPoolExecutor(max_workers=5) as ex:

        # Submit all tasks and map:
        # Future -> original index in `values`
        future_to_index = {
            ex.submit(slow_square, val): idx
            for idx, val in enumerate(values)
        }

        # Progress bar for total number of tasks
        pbar = tqdm(total=len(values), desc="Processing (process pool)")

        try:
            # Iterate futures in COMPLETION ORDER (fastest tasks first)
            for future in as_completed(future_to_index):
                idx = future_to_index[future]

                try:
                    # Get the result from the worker process
                    result = future.result()
                except Exception as e:
                    # If something went wrong in the child process
                    print(f"Task {idx} failed: {e}")
                    result = None

                # Store result back in its correct position
                results[idx] = result

                # Advance the progress bar for each completed task
                pbar.update(1)
        finally:
            # Make sure the bar is always closed cleanly
            pbar.close()

    # Build DataFrame mapping each input to its corresponding output
    return pd.DataFrame({"input": values, "output": results})


if __name__ == "__main__":
    # On Windows and some environments, this guard is REQUIRED for ProcessPoolExecutor
    # so that child processes can safely import this module.
    values = [1, 2, 3, 4, 5]

    df_results = run_in_processes(values)

    print("\nFinal results:")
    print(df_results)
