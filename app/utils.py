import numpy as np
import base64
from typing import Union


def floats_to_b64(arr):
    b = np.asarray(arr, dtype=np.float32).tobytes()
    return base64.b64encode(b).decode("ascii")


def any_to_floats(val: Union[bytes, bytearray, str]):
    if isinstance(val, (bytes, bytearray)):
        buf = bytes(val)
    elif isinstance(val, str):
        buf = base64.b64decode(val)
    else:
        raise TypeError(f"Unsupported embedding type: {type(val)}")
    return np.frombuffer(buf, dtype=np.float32)


def cosine(a, b):
    a = np.asarray(a, dtype=np.float32)
    b = np.asarray(b, dtype=np.float32)
    an = a / (np.linalg.norm(a) + 1e-8)
    bn = b / (np.linalg.norm(b) + 1e-8)
    return float(np.dot(an, bn))
