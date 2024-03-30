import argparse
import sys
import time

parser = argparse.ArgumentParser()
parser.add_argument("--start", "-s", type=int, default=0, help="number to start counting from")

args = parser.parse_args(sys.argv[1:])
counter = args.start

with open("robot_logs", "w") as f:
    pass

while True:
    with open("robot_logs", mode="a") as f:
        print(counter, end='', file=f)
    print(counter)
    time.sleep(1)
    counter += 1
