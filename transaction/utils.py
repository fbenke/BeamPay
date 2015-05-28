import random


def generate_reference_number():
    return str(random.randint(10000, 999999))


class TransactionException(Exception):
    pass
