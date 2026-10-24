"""Narzędzia pomocnicze używane przez moduły projektu."""

import time
from typing import Callable


def operation_duration(any_func: Callable):
    """Dekorator mierzący i wypisujący czas wykonania funkcji."""

    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = any_func(*args, **kwargs)
        end_time = time.time()
        print(f'Metoda [\033[91m{any_func.__name__}\033[0m] trwała: \033[92m{end_time - start_time}\033[0m secs')
        return result

    return wrapper
