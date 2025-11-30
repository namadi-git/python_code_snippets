import time
from concurrent.futures import ThreadPoolExecutor, as_completed, TimeoutError
import pandas as pd
from tqdm import tqdm


def slow_square(x: int) -> int:
    """
    Demo function that takes different times to complete based on x.
    Larger x = shorter sleep, so tasks intentionally finish out of order.
    """
    sleep_time = 6 - x
    time.sleep(sleep_time)
    return x * x


def run_in_threads(values, time_limit):
    """
    Run slow_square(x) concurrently using ThreadPoolExecutor,
    track progress with tqdm, and map results back to the original input order.
    """
    # Preallocate list so we can place results using original indices
    results = [None] * len(values)

    # Use ThreadPoolExecutor to run tasks in parallel
    with ThreadPoolExecutor(max_workers=5) as ex:

        # Submit all tasks at once and store mapping:
        # Future -> original index in `values`
        # This lets us restore correct ordering later
        future_to_index = {
            ex.submit(slow_square, val): idx
            for idx, val in enumerate(values)
        }

        # Create tqdm progress bar manually so we can control when it closes
        pbar = tqdm(total=len(values), desc="Processing")

        try:
            # Iterate over futures *as they complete* (not in submission order)
            for future in as_completed(future_to_index):

                # Get the index in the original input list
                idx = future_to_index[future]

                try:
                    # Retrieve actual result from the completed task
                    result = future.result(timeout=time_limit)
                    
                except TimeoutError:
                    # If the worker took too long
                    print(f"Task {idx} failed: TIMEOUT (>{time_limit}s)")

                except Exception as e:
                    # If the task raised an exception inside the worker thread
                    print(f"Task {idx} failed: {e}")
                    result = None

                # Place the result back into its original position
                results[idx] = result

                # Update progress bar after each completed task
                pbar.update(1)

        finally:
            # Ensures the tqdm bar is always cleaned up,
            # even if an exception occurs during processing
            pbar.close()

    # Convert aligned input/output into a DataFrame
    return pd.DataFrame({"input": values, "output": results})


if __name__ == "__main__":
    values = [1, 2, 3, 4, 5]

    # Run the threaded workflow
    df_results = run_in_threads(values, time_limit=3)

    print("\nFinal results:")
    print(df_results)
