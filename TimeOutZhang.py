#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from functools import wraps
import traceback
from addLogtoFile import addLogFile
import multiprocessing
import time


class TimeoutException(Exception):
    pass


# ✅ 将这个函数定义在最外面，避免 pickle 问题
def _target_func(queue, func, args, kwargs):
    try:
        result = func(*args, **kwargs)
        queue.put((True, result))
    except Exception as e:
        queue.put((False, e))


def timeout(seconds):
    def decorator(func):
        def wrapper(*args, **kwargs):
            queue = multiprocessing.Queue()
            process = multiprocessing.Process(
                target=_target_func, args=(queue, func, args, kwargs)
            )
            process.start()
            process.join(seconds)

            if process.is_alive():
                process.terminate()
                process.join()
                raise TimeoutException(
                    f"Function '{func.__name__}' timed out after {seconds} seconds."
                )

            if not queue.empty():
                success, outcome = queue.get()
                if success:
                    return outcome
                else:
                    raise outcome
            else:
                raise TimeoutException(
                    f"Function '{func.__name__}' failed with no result."
                )

        return wrapper

    return decorator


def task_retry(max_retry_count: int = 5, time_interval: int = 2):
    """
    任务重试装饰器
    Args:
        max_retry_count: 最大重试次数 默认5次
        time_interval: 每次重试间隔 默认2s
    """

    def _task_retry(task_func):

        @wraps(task_func)
        def wrapper(*args, **kwargs):
            # 函数循环重试
            for retry_count in range(max_retry_count):
                infoStr = f"execute count {retry_count + 1}"
                addLogFile("info", infoStr)
                try:
                    task_result = task_func(*args, **kwargs)
                    return task_result
                except Exception as e:
                    addLogFile("err", traceback.format_exc())
                    time.sleep(time_interval)

        return wrapper

    return _task_retry
