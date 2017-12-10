import math
import time
import sys
import os

FILE = "primes_list.txt"

def header():
    header = """
                   _____  _____  __ __  __ _____  _____
   2 3 5 7 2 3 5  |     \|     \|  |  \/  |     |/     \  2 3 5 7 2 3 5
   5 7 2 3 5 7 2  |   |  |   |  |  |      |   __|   \__/  5 7 2 3 5 7 2
   2 3 5 7 2 3 5  |    _/|     /|  |      |   __|\__   \  2 3 5 7 2 3 5
   5 7 2 3 5 7 2  |   |  |     \|  |  ||  |     |/  \   | 5 7 2 3 5 7 2
   2 3 5 7 2 3 5  |___|  |___\__|__|__||__|_____|\_____/  2 3 5 7 2 3 5
               """
    print(header)

def enable(topic):
    # Disable or enable the given option
    print("\n{0}?\n0: Disabled\n1: Enabled".format(topic))
    while True:
        print("{0} select: ".format(topic), end="")
        try:
            select = int(input())
            if select in range(2):
                return select
        except ValueError:
            pass

def main():
    # Variables
    last_prime_found = 2
    skip_third = -1
    skip_fifth = -2

    # Intro greetings
    print("Let's generate primes efficiently.")

    # Select timing
    timing = enable("Time tracking")

    # Select if starting anew
    if not os.path.isfile(FILE):
        print("Existing primes list not found. Starting fresh.")
        freshstart = True
    else:
        freshstart = enable("Start fresh")

    # Start from last found prime and adjust for cal
    if not freshstart:
        count = 0
        try:
            with open(FILE, "r") as prime_read:
                for p in prime_read.readlines():
                    count += 1
                    last_prime_found = int(p)
        except ValueError:
            print("Non-integer value found on Line {0} of {1}. Exiting...".format(count, FILE))
            sys.exit(1)
        except FileNotFoundError:
            print("{0} not found. Exiting...".format(FILE))
            sys.exit(1)

        mod_six = last_prime_found % 6
        if mod_six == 1:
            skip_third = 0
            prime_start = last_prime_found + 4
        if mod_six == 5:
            skip_third = 1
            prime_start = last_prime_found + 2

    print("\nStarting prime generation at {0}".format(last_prime_found))
    while True:
        print("Set an integer upper limit for primes -- ", end="")
        try:
            prime_cap = int(input())
            if prime_cap <= last_prime_found:
                print("Upper limit must be greater than {0}".format(last_prime_found))
                raise ValueError()
            print("Upper limit set to {0}".format(prime_cap))
            break
        except ValueError:
            print("Please provide a valid integer.\n")

    input("\nPress ENTER to begin.\n")

    if timing:
        start = time.time()

    # Auto-insert 2 for a new list
    if freshstart:
        with open(FILE, "w") as f:
            f.write('2\n')
            print(2)
        prime_start = 3

    for find_p in range(prime_start, prime_cap + 1, 2):
        is_prime = True
        if skip_third == 2 or skip_fifth == 4:
            skip_third = (skip_third + 1) % 3
            skip_fifth = (skip_fifth + 1) % 5
            continue
        with open(FILE, "r") as prime_read:
            with open(FILE, "a") as prime_write:
                for p in prime_read.readlines():
                    try:
                        p = int(p)
                    except ValueError:
                        sys.exit(1)
                    if p > math.sqrt(find_p):
                        break
                    if find_p % p == 0:
                        is_prime = False
                        break
                if is_prime:
                    prime_write.write(str(find_p) + '\n')
                    print(find_p)
        skip_third += 1
        skip_fifth += 1

    if timing:
        end = time.time()
        print("\nPrime generation completed. This process took %5.3f seconds" % (end - start))

    view = enable("View results")
    if view:
        os.startfile(FILE)

if __name__ == "__main__":
    os.system('cls')
    header()
    main()
