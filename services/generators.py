import random as rd
import uuid


def new_uuid() -> str:
  return str(uuid.UUID(int=rd.randint(0, 2 ** 128)))
