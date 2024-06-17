# 与 train/queue_manager.py 结构类似
import threading
from queue import Queue
from audio_transform.transformer import transform_voice
from utils.http_client import post_request

class TaskQueue:
  # ... (代码与 train/queue_manager.py 相同)

  def process_queue(self):
    while True:
      task = self.queue.get()
      task_id = task['task_id']
      audio_url = task['audio_url']
      model_url = task['model_url']
      store_url = task['store_url']
      language = task.get('language')

      try:
        # 执行音频变声
        result = transform_voice(task_id, audio_url, model_url, store_url, language)
        post_request(
          f'http://127.0.0.1:8080/clone/taskComplete',
          data={
            'taskId': task_id,
            **result
          }
        )
      except Exception as e:
        post_request(
          f'http://127.0.0.1:8080/clone/taskFail',
          data={
            'taskId': task_id,
            'message': str(e)
          }
        )