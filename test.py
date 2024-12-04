from main import answer
import coverage
import random
from datetime import datetime
import sys


class Fuzzer:
    @staticmethod
    def update_seed():
        random.seed(datetime.now().timestamp())

    @staticmethod
    def generate_data(num):
        if random.randint(-sys.maxsize, sys.maxsize) % 2 == 0:
            ans = [random.randint(-sys.maxsize, sys.maxsize) for i in range(num)]
        else:
            ans = [chr(random.randint(32, 100)) for i in range(num)]
        return ans

def analysis():
    fuzzer = Fuzzer()
    fuzzer.update_seed()
    cov = coverage.Coverage()
    cov.exclude("test.py")
    cov.start()
    for i in range(1000):
        assert answer(fuzzer.generate_data(1))
    cov.stop()
    cov.report()
    # fuzzer.report()

analysis()