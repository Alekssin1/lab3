import timeit
import os
f = open("numbers.txt", "w")
while (os.path.getsize('numbers.txt')/(1024*1024)) < 50:
    f.write('123456789012344124124214214124214\n')

test = """
with open("numbers.txt", "r") as file:
    my_lines = file.readlines()
    s=0
    for i in my_lines:
        if i.strip().isdigit():
            s+=int(i.strip())
    """
print(timeit.timeit(test, number=10))

test = """
with open("numbers.txt") as f:
    s=0
    for line in f:
        if line.strip().isdigit():
            s+=int(line.strip())
"""
print(timeit.timeit(test, number=10))

test = """
with open("numbers.txt") as f:
    s=0
    s = sum(int(i.strip()) for i in f if i.strip().isdigit())
"""
print(timeit.timeit(test, number=10))
