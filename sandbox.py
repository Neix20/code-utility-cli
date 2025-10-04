import time

from pathlib import Path

def main():
    start_time = time.time()

    input = Path("datakit.txt")
    print(input)

    end_time = time.time() - start_time
    print(f"Time Taken: {end_time:.2f} seconds")

if __name__ == "__main__":
    main()