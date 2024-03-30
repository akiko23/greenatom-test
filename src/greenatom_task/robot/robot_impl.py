import argparse
import sys
import time

parser = argparse.ArgumentParser()
parser.add_argument("--start", "-s", type=int, default=0, help="number to start counting from")

args = parser.parse_args(sys.argv[1:])
counter = args.start

while True:
    print(counter)
    time.sleep(1)
    counter += 1
