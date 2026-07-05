import random
import string
import time


class CourierHelper:
    @staticmethod
    def generate_random_string(length=10):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for _ in range(length))
    
    @staticmethod
    def generate_unique_login():
        timestamp = str(int(time.time() * 1000))[-8:]
        random_part = CourierHelper.generate_random_string(8)
        return f"{random_part}_{timestamp}"