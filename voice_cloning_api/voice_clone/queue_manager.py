# 与 train/queue_manager.py 结构类似
import threading
from queue import Queue
from voice_clone.cloner import clone_voice
from utils.http_client import post_request

class TaskQueue:
  # ... (代码与 train/queue_manager.py 相同)

  def process_queue(self):
    while True:
      task = self.queue.get()
      task_id = task['task_id']
      model_url = task['model_url']
      text = task['text']
      store_url = task['store_url']
      language = task.get('language')

      try:
        # 执行语音克隆
        result = clone_voice(task_id, model_url, text, store_url, language)
        post_request(
          f'http://127.0.0.1:8080/voiceClone/taskComplete',
          data={
            'taskId': task_id,
            **result
          }
        )
      except Exception as e:
        post_request(
          f'http://127.0.0.1:8080/voiceClone/taskFail',
          data={
            'taskId': task_id,
            'message': str(e)
          }
        )