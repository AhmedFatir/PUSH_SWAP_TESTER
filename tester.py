# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    tester.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: afatir <afatir@student.42.fr>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/11/06 11:56:13 by afatir            #+#    #+#              #
#    Updated: 2023/11/06 13:51:24 by afatir           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import argparse
import subprocess
import random
import os
import random
import time

RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
MAGENTA = '\033[95m'
RESET = '\033[0m'

def parse_arguments():
    parser = argparse.ArgumentParser(description='\033[92mpush_swap Tester\033[0m')
    parser.add_argument('num_numbers', type=int, help='Number of random numbers to generate')
    parser.add_argument('num_tests', type=int, help='Number of tests to perform')
    return parser.parse_args()

def compile_push_swap():
    subprocess.run(['make'], cwd='../')
    if os.path.isfile('log.txt'):   # Remove log.txt file if it exists
        os.remove('log.txt')

def generate_numbers(num_numbers):
    if num_numbers > 1000:  # The range -500 to 500 can only have 1001 unique numbers
        raise ValueError("Cannot generate more than 1001 unique numbers in the range -500 to 500.")
    
    numbers = random.sample(range(-500, 501), num_numbers)
    
    
    while numbers == sorted(numbers):   # Ensure numbers are not already sorted
        random.shuffle(numbers)
    
    return [str(num) for num in numbers]

def test_push_swap(numbers):
    command = ['../push_swap'] + numbers
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    operations = result.stdout.strip().split('\n')
    error_output = result.stderr.strip()
    return operations, error_output

def check_sort(numbers, operations):
    checker_command = ['./checker_Mac'] + numbers
    checker_input = '\n'.join(operations) + '\n'
    result = subprocess.run(checker_command, input=checker_input, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    is_correct = result.stdout.strip() == 'OK'
    error_output = result.stderr.strip()
    return is_correct, len(operations), error_output

def assign_points(num_operations):
    # Update these thresholds according to your project's rubric
    if num_operations < 700: return 5
    if num_operations < 900: return 4
    if num_operations < 1100: return 3
    if num_operations < 1300: return 2
    return 1

def log_failed_sequence(numbers):
    with open('log.txt', 'a') as log_file:
        log_file.write(' '.join(numbers) + '\n')

def print_color(text, color):
    print(f"{color}{text}{RESET}")

def main():
    args = parse_arguments()
    
    compile_push_swap()
    
    lowest_score = 5  # Start with the highest points possible
    total_instructions = 0
    max_instructions = 0
    min_instructions = float('inf')

    for test_num in range(1, args.num_tests + 1):
        time.sleep(0.005)
        numbers = generate_numbers(args.num_numbers)
        operations, push_swap_error = test_push_swap(numbers)
        if push_swap_error:
            log_failed_sequence(numbers)
            print_color(f"{test_num}\tError\t\t{push_swap_error}", RED)
            lowest_score = 0
            continue

        is_correct, num_operations, checker_error = check_sort(numbers, operations)
        if checker_error or not is_correct:
            log_failed_sequence(numbers)
            print_color(f"{test_num}\tError\t\t{checker_error}", RED)
            lowest_score = 0
            continue
        
        points = assign_points(num_operations)
        lowest_score = min(lowest_score, points) if is_correct else 0
        
        total_instructions += num_operations
        max_instructions = max(max_instructions, num_operations)
        min_instructions = min(min_instructions, num_operations)

        test_result = 'OK' if is_correct else 'KO'
        test_color = GREEN if test_result == 'OK' else RED
        print_color(f"{test_num}\t{num_operations}\t{points} POINTS\t{test_result}", test_color)
    
    average_instructions = total_instructions // args.num_tests if args.num_tests else 0
    print_color(f"\nMAX Instruction\t\t{max_instructions}", YELLOW)
    print_color(f"AVERAGE Instruction\t{average_instructions}", YELLOW)
    print_color(f"MIN Instruction\t\t{min_instructions}", YELLOW)
    print_color(f"YOU GOT {lowest_score} POINTS\n", MAGENTA)

    final_message = "ALL TESTS PASTS GOOD" if lowest_score == 5 else "(NOT ALL) ALL TESTS PASTS GOOD"
    print_color(final_message, RED if lowest_score < 5 else GREEN)

if __name__ == "__main__":
    main()
