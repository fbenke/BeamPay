import random
import math


def generate_reference_number():
    return str(random.randint(10000, 999999))


def round_amount(amount):
    return float(math.ceil(amount * 100)) / 100


class TransactionException(Exception):
    pass
