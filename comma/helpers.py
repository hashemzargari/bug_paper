import random

def generate_random_string(length=6):
    string = 'abcdefghijklmnopqrstuwxyz1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    str_len = len(string)
    a_list = [string[random.randrange(0, str_len + 1)] for _ in range(length)]
    return ''.join(a_list)
