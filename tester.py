import sys
import os
import subprocess
import random
import argparse

# Constants for colors
BOLD = '\033[1m'
ENDC = '\033[0m'
BLUE = '\033[94m'
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
CYAN = '\033[36m'
BG_GREEN = '\033[42m'
BG_RED = '\033[101m'
BG_DEFAULT = '\033[49m'

def bold(text):
    return f"{BOLD}{text}{ENDC}"

def check_makefile():
    result = subprocess.run(["make", "-s", "-C", "../"], capture_output=True, text=True)
    if result.returncode != 0:
        print("MAKEFILE ERROR")
        sys.exit(1)

def check_push_swap():
    if not os.path.exists("../push_swap"):
        print("push_swap not found check your Makefile")
        sys.exit(1)

def get_points(size, instructions):
    if size == 100:
        if instructions < 701:
            return f"{BG_GREEN}5 POINT{BG_DEFAULT}"
        elif instructions < 901:
            return f"{BG_GREEN}4 POINT{BG_DEFAULT}"
        elif instructions < 1101:
            return f"{BG_GREEN}3 POINT{BG_DEFAULT}"
        elif instructions < 1301:
            return f"{BG_GREEN}2 POINT{BG_DEFAULT}"
        elif instructions < 1501:
            return f"{BG_GREEN}1 POINT{BG_DEFAULT}"
    elif size == 500:
        if instructions < 5501:
            return f"{BG_GREEN}5 POINT{BG_DEFAULT}"
        elif instructions < 7001:
            return f"{BG_GREEN}4 POINT{BG_DEFAULT}"
        elif instructions < 8501:
            return f"{BG_GREEN}3 POINT{BG_DEFAULT}"
        elif instructions < 10001:
            return f"{BG_GREEN}2 POINT{BG_DEFAULT}"
        elif instructions < 11501:
            return f"{BG_GREEN}1 POINT{BG_DEFAULT}"
    elif size == 3:
        return f"{BG_GREEN}5 POINT{BG_DEFAULT}" if instructions < 4 else f"{BG_RED}0 POINT{BG_DEFAULT}"
    elif size == 5:
        return f"{BG_GREEN}5 POINT{BG_DEFAULT}" if instructions < 13 else f"{BG_RED}0 POINT{BG_DEFAULT}"
    else:
        return f"{BG_GREEN}5 POINT{BG_DEFAULT}"
    return f"{BG_RED}0 POINT{BG_DEFAULT}"

def run_single_test(size_of_stack, i):
    numbers = list(range(1, size_of_stack + 1))
    random.shuffle(numbers)
    arg = " ".join(map(str, numbers))

    push_swap_result = subprocess.run(["../push_swap"] + arg.split(), capture_output=True, text=True)
    instructions = len(push_swap_result.stdout.splitlines())

    checker_cmd = ["./utils/checker_Mac" if sys.platform == "darwin" else "./utils/checker_linux"] + arg.split()
    checker_result = subprocess.run(checker_cmd, input=push_swap_result.stdout, capture_output=True, text=True)
    check = checker_result.stdout.strip()

    if not check:
        print("ERROR")
        sys.exit(1)

    points = get_points(size_of_stack, instructions)

    if check == "OK":
        print(f"{CYAN}{i + 1}{ENDC}\t{instructions}\t {bold(points)}\t{GREEN}{check}{ENDC}")
    else:
        points = f"{BG_RED}0 POINT{BG_DEFAULT}"
        print(f"{CYAN}{i + 1}{ENDC}\t{instructions}\t {bold(points)}\t{RED}{check}{ENDC}")

    return instructions, check, arg

def run_tests(size_of_stack, number_of_tests):
    best = 0
    min_instructions = 10000
    is_ok = "Ok"

    with open("log.txt", "w") as log_file:
        for i in range(number_of_tests):
            instructions, check, arg = run_single_test(size_of_stack, i)

            if check == "KO":
                log_file.write(f"{i + 1} -- {arg}\n")
                is_ok = "KO"

            best = max(best, instructions)
            min_instructions = min(min_instructions, instructions)

    return best, min_instructions, is_ok

def print_results(best, min_instructions, is_ok, size_of_stack):
    print(f"\n{bold(YELLOW + 'MAX Instruction' + ENDC)} {best}")
    print(f"{YELLOW}AVERAGE Instruction{ENDC} {(best + min_instructions) // 2}")
    print(f"{YELLOW}MIN Instruction{ENDC} {min_instructions}")

    final_points = get_points(size_of_stack, best)
    if is_ok == "KO":
        print(f"\n      {BG_RED}{bold('NOT ALL INSTRUCTION WORK WITH ')}{ENDC}{BG_RED}Ok{BG_DEFAULT}")
        print(f"\n           {BG_RED}{bold('CHECK THE LOG FILE')}{ENDC}{BG_RED}{BG_DEFAULT}\n")
    else:
        print(f"{YELLOW}YOU GOT {ENDC}{bold(final_points)}\n")
        print(f"      {BG_GREEN}{bold('ALL INSTRUCTION WORK WITH OK')}{BG_DEFAULT}\n")

    if os.path.getsize("log.txt") == 0:
        os.remove("log.txt")
    else:
        print(bold('Check the log file "log.txt" for details on failed tests.\n'))

def main():
    parser = argparse.ArgumentParser(description="Run push_swap tests")
    parser.add_argument("size_of_stack", type=int, help="Size of the stack")
    parser.add_argument("number_of_tests", type=int, help="Number of tests to run")
    args = parser.parse_args()

    check_makefile()
    check_push_swap()

    best, min_instructions, is_ok = run_tests(args.size_of_stack, args.number_of_tests)
    print_results(best, min_instructions, is_ok, args.size_of_stack)

if __name__ == "__main__":
    main()