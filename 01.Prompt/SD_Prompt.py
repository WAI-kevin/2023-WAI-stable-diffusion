#######################################################
#######################################################
## 파일 명 : stable_diffusion_PromptengEngineering.py
## 작성 일 : 2023년 05월 22일
## 작성 자 : SILVERBEEN
## INPUT : RAW KOREAN TEXT
## OUTPUT : ENGLISH TEXT LIST (PROMPT)
#######################################################
#######################################################
## log 찍어주는 함수
def line_logging( *messages):

    today = datetime.datetime.today()
    log_time = today.strftime('[%Y/%m/%d %H:%M:%S]')
    log = []
    for message in messages:
        log.append(str(message))
    print(log_time + '::' + ' '.join(log) + '')
    sys.stdout.flush()


## text 전처리 함수
## input data : korean_text = 전처리가 되지 않은 한국어
## output data : return new_korean_text_00 = 전처리가 완료된 한국어
### pykospacing 설치를 위한 git 설치: pip install git+https://github.com/haven-jeon/PyKoSpacing.git , tensorflow==2.9.3
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

## google translator API 함수
## 명사 형태
## NN(명사, 단수형), NNS(명사, 복수형), NNP(고유명사, 단수형), NNPS(고유명사, 복수형),
## 동사 형태
## VB(동사, 원형), VBD(동사, 과거형), VBG(동사, 현재분사), VBN(동사, 과거분사)
## 형용사 형태
## JJ(형용사), JJR(형용사, 비교급), JJS(형용사, 최상급)
## 전치사
## IN (전치사)
## 부사
## ADV (부사)
import requests
## pip install googletrans==3.1.0a0
def translator_ko_en (new_korean_text : str,select_parts_of_speech : list)  -> list :
    line_logging("="*20," translator_ko_en Function START ","="*20)
    translator = Translator()
    result = translator.translate(new_korean_text, src='ko', dest='en')
    english_text = result.text
    print(new_korean_text)
    print("="*20)
    print(english_text)
    tagged_list = pos_tag(word_tokenize(english_text))
    final_english_text = [word[0] for word in tagged_list if word[1] in select_parts_of_speech]

    line_logging("="*20," translator_ko_en Function FINISH ","="*20)
    return final_english_text


## c1 = ["35mm", "sharp", "low poly 3d render"] 과 같은 형태의 input일 경우
def category_append (prompt_text:"list", c1 : "list", c2 : "list", c3 : "list") -> list :
    prompt_text.extend(c1)
    prompt_text.extend(c2)
    prompt_text.extend(c3)
    return prompt_text


try :
    import datetime
    import sys
    import re
    import sys
    import subprocess
    from googletrans import Translator
    import nltk
    from nltk.tokenize import word_tokenize
    from nltk.tag import pos_tag
    from pykospacing import Spacing

    text = "안녕하세,요. - d-wg- ㅎㅎㅎ 제   이름은 피곤한 은색콩입니다. 집 좀   보내주세요. 저 내일부터 회사    안나옵니다.^^ 메롱 바보. 안녕하세요. 메롱. 메롱."
    c1 = ["35mm, sharp", "low poly 3d render"]
    c2 = ["Pablo Picasso", "Van Gogh", "Da Vinci"]
    c3 = ["ultra wide-angle", "wide-angle", "aerial view", "massive scale"]

    select_parts_of_speech = ["NN", "NNS", "NNP", "NNPS", "VB", "VBD", "VBG", "VBN", "JJ", "JJR", "JJS", "ADV"]
    new_korean_text = korean_cleaning(text)
    prompt_text = translator_ko_en(new_korean_text, select_parts_of_speech)
    result_text = category_append(prompt_text, c1, c2, c3)


except Exception as e :
    print(e)







