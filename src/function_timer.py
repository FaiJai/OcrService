import time
import functools
from logging_service import logger


def debug_timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if __debug__:  # Only runs when Python is not in optimization mode (-O flag)
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            end_time = time.perf_counter()
            logger.debug(f"{func.__name__} took {end_time - start_time:.4f} seconds")
            print(f"{func.__name__} took {end_time - start_time:.4f} seconds")
            return result
        return func(*args, **kwargs)

    return wrapper
