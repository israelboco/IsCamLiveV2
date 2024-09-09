import threading
import time

class ThreadManager:
    def __init__(self):
        self.threads = []
        self.stop_event = threading.Event()

    def start_thread(self, target, *args):
        thread = threading.Thread(target=target, args=args)
        thread.start()
        self.threads.append(thread)

    def stop_all_threads(self):
        self.stop_event.set()
        for thread in self.threads:
            thread.join()

def worker(stop_event, thread_id):
    while not stop_event.is_set():
        print(f"Thread {thread_id} is running...")
        time.sleep(1)
    print(f"Thread {thread_id} is stopping...")
