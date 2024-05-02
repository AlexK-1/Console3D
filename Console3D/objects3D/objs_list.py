from typing import Union, Any, Callable, Dict, NoReturn, Iterable, Tuple, Sequence


light_objects: list = []    # список источников освещения
figures_objects: list = []  # список отображаемых фигур
camera_object = []          # камера, через которую видит пользователь; камера должна быть только одна,
#                             но я вынужден использовать список из-за проблем с глобальными переменными
