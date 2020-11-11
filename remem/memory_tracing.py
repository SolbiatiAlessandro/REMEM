from functools import wraps
import tracemalloc
import statsd
import logging

def statsd_counter(name, value):
    client = statsd.StatsClient('127.0.0.1', 8125)
    client.incr(name, value)

def memory_trace(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        tracemalloc.start()
        res = func(*args, **kwargs)
        current_memory, memory_peak = tracemalloc.get_traced_memory()
        statsd_counter('remem.malloc.peak', memory_peak)
        statsd_counter('remem.malloc.curr', current_memory)
        logging.warning("memory_trace: {} {}".format(current_memory, memory_peak))
        return res
    return wrapper