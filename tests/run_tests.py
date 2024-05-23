import subprocess

test_cases = [
    ("test1.txt", "YES: 1"),
    ("test2.txt", "NO"),
    ("test3.txt", "YES: 1"),
    ("test4.txt", "NO"),
    ("test5.txt", "YES: 1"),
    ("test6.txt", "YES: 1"),
    ("test7.txt", "YES: 1"),
    ("test8.txt", "YES: 1"),
    # ("test_cases/test9.txt", "NO"),
    ("test10.txt", "NO")
    # ("test9.txt", "NO") # most comprehensive test case involving 392 details
]

for test_file, expected_output in test_cases:
    result = subprocess.run(["python3", "../main.py", test_file, "TT"], capture_output=True, text=True)

    output = result.stdout.strip()
    test = output.split("\n")[-1]
    print(f"Test {test_file}: {'PASS' if test == expected_output else 'FAIL'}")
    if output != expected_output:
        print(f"  Expected: {expected_output}")
        print(f"  Got: {output}")
        print()