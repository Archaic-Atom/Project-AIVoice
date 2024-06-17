from flask import Flask, request, jsonify

app = Flask(__name__)

"""
模型微调训练
"""

from train.queue_manager import TaskQueue
from train.trainer import train_model

task_queue = TaskQueue()  # 初始化任务队列

@app.route('/train/createTask', methods=['POST'])
def create_train_task():
  """
  创建模型微调训练任务
  """
  data = request.get_json()
  task_id = data.get('taskId')
  sound_path = data.get('sound')
  store_url = data.get('storeUrl')

  # TODO: 校验参数

  # 创建训练任务并加入队列
  task = {
    'task_id': task_id,
    'sound_path': sound_path,
    'store_url': store_url
  }
  task_queue.enqueue(task)

  # 返回任务创建成功信息
  return jsonify({
    'taskId': task_id,
    'status': 1,
    'message': 'Task created successfully'
  })


"""
音频模型应用
"""

from voice_clone.queue_manager import TaskQueue as VoiceCloneTaskQueue

voice_clone_task_queue = VoiceCloneTaskQueue()  # 初始化语音克隆任务队列

@app.route('/voiceClone/createVoiceCloneTask', methods=['POST'])
def create_voice_clone_task():
  """
  创建语音克隆任务
  """
  data = request.get_json()
  task_id = data.get('taskId')
  model_url = data.get('modelUrl')
  text = data.get('text')
  store_url = data.get('storeUrl')
  language = data.get('language')

  # TODO: 校验参数

  # 创建任务并加入队列
  task = {
    'task_id': task_id,
    'model_url': model_url,
    'text': text,
    'store_url': store_url,
    'language': language
  }
  voice_clone_task_queue.enqueue(task)

  # 返回任务创建成功信息
  return jsonify({
    'taskId': task_id,
    'status': 1,
    'message': 'Voice clone task created successfully'
  })


"""
音频变声
"""

from audio_transform.queue_manager import TaskQueue as AudioTransformTaskQueue

audio_transform_task_queue = AudioTransformTaskQueue()  # 初始化音频变声任务队列

@app.route('/clone/createCloneTask', methods=['POST'])
def create_clone_task():
  """
  创建音频变声任务
  """
  data = request.get_json()
  task_id = data.get('taskId')
  audio_url = data.get('audioUrl')
  model_url = data.get('modelUrl')
  store_url = data.get('storeUrl')
  language = data.get('language')

  # TODO: 校验参数

  # 创建任务并加入队列
  task = {
    'task_id': task_id,
    'audio_url': audio_url,
    'model_url': model_url,
    'store_url': store_url,
    'language': language
  }
  audio_transform_task_queue.enqueue(task)

  # 返回任务创建成功信息
  return jsonify({
    'taskId': task_id,
    'status': 1,
    'message': 'Voice transform task created successfully'
  })


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8081)