import string
import random


def generate_referral_code(size=6, chars=string.ascii_uppercase):
    return ''.join(random.choice(chars) for _ in range(size))
