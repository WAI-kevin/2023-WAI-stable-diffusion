import datetime
import re
import sys
import subprocess
from googletrans import Translator
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

import base64
import torch
from torch import autocast
from PIL import Image
from random import randint
from io import BytesIO

import os
import argparse







def line_logging(*messages):
    today = datetime.datetime.today()
    log_time = today.strftime('[%Y/%m/%d %H:%M:%S]')
    log = []
    for message in messages:
        log.append(str(message))
    print(log_time + '::' + ' '.join(log) + '')
    sys.stdout.flush()
    



def korean_cleaning (korean_text : str) -> str :

    line_logging("="*20," korean_cleaning Function START ","="*20)

    new_korean_text_00 = re.sub(pattern='([ㄱ-ㅎㅏ-ㅣ])+', repl=' ', string=korean_text)  # 자음,모음 제거
    new_korean_text_00 = re.sub(pattern='\n', repl=' ', string=new_korean_text_00)  # \n 제거
    new_korean_text_00 = re.sub(pattern='[^ㄱ-ㅎㅏ-ㅣ가-힣a-zA-Z0-9\s\.\?!]', repl=' ',
                                string=new_korean_text_00)  # 한글, 영문, 숫자, 구두점을 제외한 모든 문자를 제거하는 정규표현식

    new_korean_text_00 = re.sub(pattern='(http|ftp|https)://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', repl=' ', string=new_korean_text_00)  # URL 제거
    new_korean_text_00 = re.sub(pattern='([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)', repl=' ', string=new_korean_text_00)  # E-mail제거
    new_korean_text_count = new_korean_text_00.split(" ")
    new_korean_text_00 = new_korean_text_00.replace(" ", ". ")

    #spacing = Spacing()
    #kospacing_sent = spacing(new_korean_text_00)

    if (len(new_korean_text_00)<=10) | (len(new_korean_text_count) <= 2) :
        line_logging("[ Please write in more detail. ]")
    else :
        line_logging("="*20," korean_cleaning Function FINISH ","="*20)
    return new_korean_text_00



def translator_ko_en(new_korean_text : str,select_parts_of_speech : list)  -> list :
    line_logging("="*20," translator_ko_en Function START ","="*20)
    translator = Translator()
    result = translator.translate(new_korean_text, src='ko', dest='en')
    english_text = result.text
    tagged_list = pos_tag(word_tokenize(english_text))
    final_english_text = [word[0] for word in tagged_list if word[1] in select_parts_of_speech]

    line_logging("="*20," translator_ko_en Function FINISH ","="*20)
    return final_english_text


def category_append (prompt_text:"list", c1 : "list", c2 : "list", c3 : "list") -> list :
    prompt_text.extend(c1)
    prompt_text.extend(c2)
    prompt_text.extend(c3)
    return prompt_text


####### Text To Image #######
def sd_texttoimg_pipeline():
    from accelerate import Accelerator
    from diffusers import StableDiffusionPipeline
    
    line_logging("="*20," sd_texttoimg_pipeline Function START ","="*20)
    
    device = "cuda"
    accelerator = Accelerator()
    device = accelerator.device

    model_id = "runwayml/stable-diffusion-v1-5"
    pipe = StableDiffusionPipeline.from_pretrained(
        model_id,
        revision = 'fp16', 
        torch_dtype = torch.float16,
    ).to(device)
    line_logging("="*20," sd_texttoimg_pipeline Function FINISH ","="*20)
    return pipe


def sd_texttoimg_function(pipe, prompt : str, seed : str):
    
    line_logging("="*20," sd_texttoimg_function Function START ","="*20)
    device = "cuda"

    if seed == "":
        seed_no = randint(1, 999999999)
    else:
        seed_no = int(seed)

    generator = torch.Generator(device=device).manual_seed(seed_no)
    with autocast(device):
        image = pipe(prompt=prompt, generator=generator)['images'][0]

    line_logging("="*20," sd_texttoimg_function Function FINISH ","="*20)
    line_logging("="*20," texttoimg // prompt : ", prompt, "seed : ", seed_no ,"="*20)

    return image








class ClsProcess:
    
    def __init__(self):
        self.result = 0

    def preprocess(self, text):
        nltk.download('punkt')
        nltk.download('averaged_perceptron_tagger')

        self.select_parts_of_speech = ["NN", "NNS", "NNP", "NNPS", "VB", "VBD", "VBG", "VBN", "JJ", "JJR", "JJS"]
        new_korean_text = korean_cleaning(text)
        result_text = translator_ko_en(new_korean_text, self.select_parts_of_speech)
        return result_text
    
    def text_to_image(self, prompt, seed):
        def encode_image_to_base64(image):
            buffered = BytesIO()
            image.save(buffered, format="png")  # 이미지를 PNG 형식으로 저장
            encoded_image = base64.b64encode(buffered.getvalue()).decode("utf-8")
            return encoded_image
        try:
            image = sd_texttoimg_function(self.pipe_t2i, prompt, seed)
        except:
            self.pipe_t2i = sd_texttoimg_pipeline()
            image = sd_texttoimg_function(self.pipe_t2i, prompt, seed)
        encoded_image = encode_image_to_base64(image)
        return encoded_image
