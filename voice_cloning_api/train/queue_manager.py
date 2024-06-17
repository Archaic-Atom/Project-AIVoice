import threading
from queue import Queue
from train.trainer import train_model
from utils.http_client import post_request

class TaskQueue:
  def __init__(self):
    self.queue = Queue()
    self.lock = threading.Lock()
    self.worker_thread = threading.Thread(target=self.process_queue, daemon=True)
    self.worker_thread.start()

  def enqueue(self, task):
    with self.lock:
      self.queue.put(task)

  def process_queue(self):
    while True:
      task = self.queue.get()
      task_id = task['task_id']
      sound_path = task['sound_path']
      store_url = task['store_url']

      try:
        # 执行模型训练
        result = train_model(task_id, sound_path, store_url)
        post_request(
          f'http://127.0.0.1:8080/train/taskComplete',
          data={
            'taskId': task_id,
            **result
          }
        )
      except Exception as e:
        post_request(
          f'http://127.0.0.1:8080/train/taskFail',
          data={
            'taskId': task_id,
            'message': str(e)
          }
        )