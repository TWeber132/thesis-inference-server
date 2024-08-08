# process_manager.py
import queue
import threading

from processes.process import process_np_array

_processing_lock = threading.Lock()
_is_processing = False
_process_queue = queue.Queue()


def process():
    while not _process_queue.empty():
        task_type, byte_data, task_id = _process_queue.get()
        if task_type in ["process_np_array"]:
            process_np_array(byte_data, task_id)
        else:
            raise ValueError(f"Unknown task type {task_type}")
    stop_processing()


def start_processing_if_not_started(background_tasks):
    global _is_processing
    with _processing_lock:
        if not _is_processing:
            _is_processing = True
            background_tasks.add_task(process)


def stop_processing():
    global _is_processing
    with _processing_lock:
        _is_processing = False
