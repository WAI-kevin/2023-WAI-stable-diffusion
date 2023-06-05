#######################################################
#######################################################
## 파일 명 : stable_diffusion_PromptengEngineering.py
## 작성 일 : 2023년 05월 22일
## 작성 자 : SILVERBEEN
## INPUT : RAW KOREAN TEXT
## OUTPUT : ENGLISH TEXT LIST (PROMPT)
#### prompt rule
#### 전체적인 작성 규칙 : 구분자를 , 로 (ex. 예쁜 고양이가 케이크를 먹는다., 케이크는 초코 케이크, 옆에는 사탕을 먹는 여자아이가 있다.)
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
    # ".", "!", "?", "," 를 제외한 특수문자 제거 ('"#$%&\'()*+-/:;<=>@[\\]^_`{|}~')
    remove_text = string.punctuation
    remove_text = remove_text.replace(".", "").replace(",", "").replace("!", "").replace("?", "")

    clean_korean_text_Consonants = re.sub(pattern='([ㄱ-ㅎㅏ-ㅣ])+', repl=' ', string=korean_text)  # 자음,모음 제거
    clean_korean_text_enter = re.sub(pattern='\n', repl=' ', string=clean_korean_text_Consonants)  # \n 제거
    clean_korean_text_url = re.sub(pattern='(http|ftp|https)://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', repl=' ', string=clean_korean_text_enter)  # URL 제거
    new_korean_text_email = re.sub(pattern='([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)', repl=' ', string=clean_korean_text_url)  # E-mail제거
    new_korean_text = ''.join([k for k in new_korean_text_email if k not in remove_text])
    new_korean_text_count = new_korean_text.split(",")
    

    if (len(new_korean_text)<=10) | (len(new_korean_text_count) <= 2) :
        line_logging("[ Please write in more detail. ]")
    else :
        line_logging("="*20," korean_cleaning Function FINISH ","="*20)
    return new_korean_text

## google translator API 함수

def translator_ko_en (new_korean_text : str,select_parts_of_speech : list)  -> list :
    line_logging("="*20," translator_ko_en Function START ","="*20)
    translator = Translator()
    result = translator.translate(new_korean_text, src='ko', dest='en')
    english_text = result.text.split(",")

    line_logging("="*20," translator_ko_en Function FINISH ","="*20)
    return english_text


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
    import string
    from googletrans import Translator

    text = "예쁜 고양이가 케이크를 먹는다., 케이크는 초코 케이크, 옆에는 사탕을 먹는 여자아이가 있다."
    c1 = ["35mm, sharp", "low poly 3d render"]
    c2 = ["Pablo Picasso", "Van Gogh", "Da Vinci"]
    c3 = ["ultra wide-angle", "wide-angle", "aerial view", "massive scale"]

    new_korean_text = korean_cleaning(text)
    prompt_text = translator_ko_en(new_korean_text, select_parts_of_speech)
    result_text = category_append(prompt_text, c1, c2, c3)


except Exception as e :
    print(e)







