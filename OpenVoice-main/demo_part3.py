#!/usr/bin/env python
# coding: utf-8

# ## Multi-Accent and Multi-Lingual Voice Clone Demo with MeloTTS

# In[ ]:


import os
import torch
from openvoice import se_extractor
from openvoice.api import ToneColorConverter


# ### Initialization
# 
# In this example, we will use the checkpoints from OpenVoiceV2. OpenVoiceV2 is trained with more aggressive augmentations and thus demonstrate better robustness in some cases.

# In[ ]:


ckpt_converter = 'checkpoints_v2/converter'
device = "cuda:0" if torch.cuda.is_available() else "cpu"
output_dir = 'outputs_spanish'

tone_color_converter = ToneColorConverter(f'{ckpt_converter}/config.json', device=device)
tone_color_converter.load_ckpt(f'{ckpt_converter}/checkpoint.pth')

os.makedirs(output_dir, exist_ok=True)


# ### Obtain Tone Color Embedding
# We only extract the tone color embedding for the target speaker. The source tone color embeddings can be directly loaded from `checkpoints_v2/ses` folder.

# In[ ]:



reference_speaker = 'resources/spanish_1.wav' # This is the voice you want to clone
target_se, audio_name = se_extractor.get_se(reference_speaker, tone_color_converter, vad=True)


# #### Use MeloTTS as Base Speakers
# 
# MeloTTS is a high-quality multi-lingual text-to-speech library by @MyShell.ai, supporting languages including English (American, British, Indian, Australian, Default), Spanish, French, Chinese, Japanese, Korean. In the following example, we will use the models in MeloTTS as the base speakers. 

# In[ ]:


from melo.api import TTS

texts = {
    'EN': "Did you ever hear a folk tale about a giant turtle?",  # The newest English base speaker model
    'EN': "Did you ever hear a folk tale about a giant turtle?",
    'ES': "El resplandor del sol acaricia las olas, pintando el cielo con una paleta deslumbrante",
    # 'ES': "Estoy llegando al umbral de la composición.",
    'FR': "La lueur dorée du soleil caresse les vagues, peignant le ciel d'une palette éblouissante.",
    # 'ZH': "在这次vacation中，我们计划去Paris欣赏埃菲尔铁塔和卢浮宫的美景。",
    'ZH': "信息工程学院是指拥有信息工程（或者计算机工程、电子信息等相关专业）教育和研究方向的学院或学部",
    'JP': "彼は毎朝ジョギングをして体を健康に保っています。",
    'KR': "안녕하세요! 오늘은 날씨가 정말 좋네요.",
}


src_path = f'{output_dir}/tmp.wav'

# Speed is adjustable
speed = 1.0

for language, text in texts.items():
    model = TTS(language=language,use_hf=False, device=device)
    speaker_ids = model.hps.data.spk2id

    for speaker_key in speaker_ids.keys():
        speaker_id = speaker_ids[speaker_key]
        speaker_key = speaker_key.lower().replace('_', '-')
        
        source_se = torch.load(f'checkpoints_v2/base_speakers/ses/{speaker_key}.pth', map_location=device)
        model.tts_to_file(text, speaker_id, src_path, speed=speed)
        save_path = f'{output_dir}/output_v2_{speaker_key}.wav'

        # Run the tone color converter
        encode_message = "@MyShell"
        tone_color_converter.convert(
            audio_src_path=src_path, 
            src_se=source_se, 
            tgt_se=target_se, 
            output_path=save_path,
            message=encode_message)

