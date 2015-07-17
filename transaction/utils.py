import random


def generate_reference_number():
    return str(random.randint(10000, 999999))


def round_amount(amount):
    return float(int(amount * 100)) / 100


class TransactionException(Exception):
    pass
