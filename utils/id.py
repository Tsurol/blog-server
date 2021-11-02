import random
import string
from uuid import uuid1


def id_generator(size=8, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def uid_gen():
    return uuid1().hex


if __name__ == '__main__':
    # test
    print(uid_gen())
