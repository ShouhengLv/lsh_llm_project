import time
from functools import wraps

def retry_on_exception(max_retries=3, delay=2):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(1, max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"[重试中] 第 {attempt} 次失败：{e}")
                    last_error = e
                    time.sleep(delay)
            raise RuntimeError(f"[重试失败] 尝试了 {max_retries} 次仍未成功: {last_error}")
        return wrapper
    return decorator
