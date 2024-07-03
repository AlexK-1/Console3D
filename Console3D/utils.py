from typing import Union, Any, Callable, Dict, NoReturn, Iterable, Tuple, Sequence
import numpy as np
import time
from .config import debug


def minmax(value: Union[float, int], min_: Union[float, int], max_: Union[float, int]) -> Union[float, int]:
    """Ограничение числа value сверху и снизу числами min_ и max_"""
    return max(min(value, max_), min_)

def max_(*args):
    result = []
    for i in range(len(args[0])):
        a = []
        for j in range(len(args)):
            a.append(args[j][i])
        result.append(max(a))
    return result

def log(name: str):
    def inner_decorator(fn):
        def wrapper(*args, **kwargs):
            if debug:
                start_time = time.time()
                result =  fn(*args, **kwargs)
                print(f"{name.capitalize()}: {time.time()-start_time}")
                return result
            return fn(*args, **kwargs)
        return wrapper
    return inner_decorator
