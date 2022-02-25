from secrets import choice

alphabet = """0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~"""


def create(length=30):
    password = "".join(choice(alphabet) for _ in range(30))
    return password
