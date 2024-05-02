from typing import Union, Any, Callable, Dict, NoReturn, Iterable, Tuple, Sequence
import numpy as np


def minmax(value: Union[float, int], min_: Union[float, int], max_: Union[float, int]) -> Union[float, int]:
    """Ограничение числа value сверху и снизу числами min_ и max_"""
    return max(min(value, max_), min_)
