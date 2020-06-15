import json
import random
from io import StringIO
import sys
import threading


# authored by: https://github.com/joeyespo/
# link to source: https://github.com/joeyespo/py-getch/tree/master/getch
try:
    from msvcrt import getch
except ImportError:
    def getch():
        """
        Gets a single character from STDIO.
        """
        import sys
        import tty
        import termios
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            return sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)


def read_natural_or_none():
    print("Enter N:")
    try:
        n = int(input())
        if n <= 0:
            n = None
    except ValueError:
        n = None
    return n


def set_up_for_source(filename):
    with open(filename, "rb") as json_file:
        data = json.load(json_file)
    # TODO (won't be implemented) validate json
    return data


def evaluate(choice_map):
    keys = []
    values = []
    for i in choice_map:
        keys.append(i)
        values.append(float(eval(choice_map[i])))
    return random.choices(population=keys, weights=values, k=1)[0]


def threaded_function():
    c = 0
    # TODO: include all symbols for keyboard layout
    while c != bytearray("q", "utf-8"):
        c = getch()


def generate_from_file(filename, n):
    data = set_up_for_source(filename)
    if n == 2:
        return 0
    source = data["source"]
    switches = data["switches"]
    models = data["models"]
    source_count = len(source)
    if n:
        for i in range(n):
            switch_name = source[i % source_count]
            switch = switches[switch_name]
            model = models[evaluate(switch)]
            output = evaluate(model)
            print(output)
    else:
        i = 0
        t = threading.Thread(target=threaded_function)
        t.start()
        while t.is_alive():
            switch_name = source[i % source_count]
            switch = switches[switch_name]
            model = models[evaluate(switch)]
            output = evaluate(model)
            print(output)
            i += 1


def count_subsequence_probability(filename, n):
    print("Enter subsequence a1,...,ak:")
    substr = input()
    subsequence = "".join(substr.split(" "))
    # intercept stdout in 'out' variable
    out = StringIO()
    sys.stdout = out
    generate_from_file(filename, n)
    # restore stdout
    sys.stdout = sys.__stdout__
    sequence = "".join(out.getvalue().split("\n"))
    sequence = "".join(sequence.split(" "))
    count = 0
    for i in range(len(sequence) - len(substr) + 1):
        j = 0
        while j < len(substr) and sequence[i+j] == substr[j]:
            j += 1
        if j == len(substr):
            count += 1
    print("Probability is", count/(len(sequence) - len(substr) + 1))
    return 0


def main():
    filename = "example2.json"
    print("You've started discrete source modeling app")
    print("Enter 1 for sequence for source from file")
    print("Enter 2 for probability count of subsequence")
    i = int(input())
    if i == 1:
        n = read_natural_or_none()
        generate_from_file(filename, n)
    elif i == 2:
        n = read_natural_or_none()
        count_subsequence_probability(filename, n)
    else:
        print("Try again")


if __name__ == "__main__":
    main()
