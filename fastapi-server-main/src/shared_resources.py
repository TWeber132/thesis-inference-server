# shared_resources.py
import threading

_results = {}
_results_lock = threading.Lock()

_model_lock = threading.Lock()
_model_cache = {
    'model_name': None,
    'model': None
}


def set_result(task_id, value):
    with _results_lock:
        _results[task_id] = value


def get_result(task_id):
    with _results_lock:
        return _results.get(task_id, None)
