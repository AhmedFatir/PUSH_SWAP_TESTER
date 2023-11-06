# PUSH_SWAP_TESTER

This testing script has been created to automate the testing of the `push_swap` project.
It generates random number sequences, executes them through the `push_swap` program, and then verifies the results using the `checker_Mac` utility.
The purpose of this script is to ensure that the sorting algorithm works as expected.
If any of the tests fail, the script will create a `log.txt` file where you can find the generated numbers of the failed tests.

if you are using a Linux environment you should change `checker_Mac` to `checker_linux` 
## Prerequisites

Before you run the tester, you need to have Python 3 installed on your system.

## Setups

```bash 
1. cd "PATH_TO_YOUR_PUSH_SWAP_REPOSITORY"
```
```bash 
2. git clone https://github.com/AhmedFatir/PUSH_SWAP_TESTER.git
```
```bash 
3. cd PUSH_SWAP_TESTER
```
```bash
4. python3 tester.py "num_numbers" "num_tests" 
```
`example:`
```bash
python3 tester.py 100 50
```
`or just if you need help:`
```bash
python3 tester.py -h
```
