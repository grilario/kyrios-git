import random

from os import path
from uuid import uuid4


def generateID(length=12):
    caracteres = 'ABCDFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'

    id = ''.join(random.choice(caracteres) for i in range(length))
    return id


def generateNameFile(instance, filename):
    return '{0}{1}'.format(uuid4().hex, path.splitext(filename)[1])


def renameFileWithUUID(instance, filename):
    return '{0}_{1}'.format(uuid4().hex, filename)
