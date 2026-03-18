import math

def is_prime(n):

    if n < 2:
        return False

    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False

    return True

def prime_sum(start, end):

    total = 0

    for i in range(start, end):
        if is_prime(i):
            total += i

    return total

