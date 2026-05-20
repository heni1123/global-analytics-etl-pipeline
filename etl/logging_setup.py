import logging
import time
from typing import Callable

def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("pipeline.log"),
            logging.StreamHandler()
        ]
    )

def retry_on_failure(max_retries: int, delay: float) -> Callable:
    def decorator(func: Callable) -> Callable:
        async def wrapper(*args, **kwargs) -> None:
            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    logging.error(f"Error in {func.__name__}: {e}. Attempt {attempt + 1} of {max_retries}.")
                    if attempt < max_retries - 1:
                        time.sleep(delay)
                    else:
                        logging.critical(f"Max retries reached for {func.__name__}.")
                        raise
        return wrapper
    return decorator

setup_logging()