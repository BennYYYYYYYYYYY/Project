import os 
import pandas as pd
import re
import json
import time

def extract_json(text: str):
    pattern = re.compile(r'({.*})', re.DOTALL)
    match = pattern.search(text)
    if match:
        text = match.group(1)
    else:
        pass
    return text


# 避免 '''JSON{{}}'''，只抓 {}
def extract_json_2(text: str):
    pattern_2 = re.compile(r'\{[\s\S]*?\}')
    match_2 =  pattern_2.search(text)
    if match_2:
        text = match_2.group()
    else:
        pass
    return text


def sentiment_esg_run(model_name: str, chain, input_folder, prompt_topic: str, file_start: int, sleep_time: int):     
    for _,file in enumerate (os.listdir(input_folder)):
        file_with_right_sequence = str(file_start)+(os.path.splitext(file)[1])
        file_xlsx = os.path.join(input_folder, file_with_right_sequence)
        df = pd.read_excel(file_xlsx)
        
        number_answer_list = [] # 新 column 資料

        if "use_sentence" in df.columns.to_list():
            df.drop(columns=["use_sentence"], inplace=True)
        else:
            pass    

        for value in (df["sentence"]):
            result = chain.invoke({"value":value})
            
            # OpenAI SDK 格式與 Ollama 不一樣，處理這部分
            try:
                result = result.content
            except:
                pass

            # 有時會有缺後括號的情況
            if not result.strip().endswith("}"):
                result += "}"
                
            try:
                result = json.loads(extract_json(result))
                print(result["thinking_process"], result["number"])
                answer = result["number"]
                number_answer_list.append(answer)
            except Exception as e:
                print("出事拉~~~~~~~~", result, e)

        if prompt_topic == "Sentiment":
            column_name = model_name+"_sentiment"
        else:
            column_name = model_name+"_ESG"


        df[column_name] = number_answer_list
        try:
            df.to_excel(file_xlsx, index=False)
            print(f"檔案: {file_with_right_sequence} 完成")
        except Exception as e:
            print(f"檔案: {file_with_right_sequence} 出大事 {e}")
            
        file_start += 1
        time.sleep(sleep_time)



from prompt_use import llms_prompt_few_shot


def sentiment_esg_run_few_shot_new(model_name: str, llm, df_few_shot, input_folder, prompt_topic: str, file_start: int, sleep_time: int):     
    for _, file in enumerate(os.listdir(input_folder)):
        file_with_right_sequence = str(file_start)+(os.path.splitext(file)[1])
        file_xlsx = os.path.join(input_folder, file_with_right_sequence)
        df = pd.read_excel(file_xlsx)
        
        number_answer_list = []  # 新 column 資料 

        for sentence in df["sentence"]:
            try:
                # 每次重新 few-shot 抽樣 
                prompt = llms_prompt_few_shot(prompt_topic, df_few_shot)
                prompt_text = prompt.format(value=sentence)
                result = llm.invoke(prompt_text)
                # print(prompt_text)

                if hasattr(result, "content"):
                    result = result.content

                result = json.loads(extract_json(result))
                print(result["number"])
                number_answer_list.append(result["number"])

            except Exception as e:
                print("出事拉~~~~~~~~", sentence, e)
                number_answer_list.append("ERROR")

        if prompt_topic == "Sentiment":
            column_name = model_name + "_few_shot_sentiment"
        else:
            column_name = model_name + "_few_shot_ESG"

        df[column_name] = number_answer_list
        try:
            df.to_excel(file_xlsx, index=False)
            print(f" {file_with_right_sequence} 完成")
        except Exception as e:
            print(f"{file_with_right_sequence} 寫入錯誤：, {e}")
            
        file_start += 1
        time.sleep(sleep_time)



def sentiment_esg_run_zero_shot(model_name: str, chain, input_folder, prompt_topic: str, file_start: int, sleep_time: int):     
    for _,file in enumerate (os.listdir(input_folder)):
        file_with_right_sequence = str(file_start)+(os.path.splitext(file)[1])
        file_xlsx = os.path.join(input_folder, file_with_right_sequence)
        df = pd.read_excel(file_xlsx)
        
        number_answer_list = [] # 新 column 資料

        for value in (df["sentence"]):
            result = chain.invoke({"value":value})
            
            # OpenAI SDK 格式與 Ollama 不一樣，處理這部分
            if hasattr(result, "content"):
                result = result.content

            # 有時會有缺後括號的情況
            if not result.strip().endswith("}"):
                result += "}"
                
            try:
                result = json.loads(extract_json_2(extract_json(result)))
                print(result["number"])
                answer = result["number"]
                number_answer_list.append(answer)
            except Exception as e:
                print("出事拉~~~~~~~~", result, e)
                number_answer_list.append("ERROR")

        if prompt_topic == "Sentiment":
            column_name = model_name+"_zero_shot_sentiment"
        else:
            column_name = model_name+"_zero_shot_ESG"

        df[column_name] = number_answer_list
        try:
            df.to_excel(file_xlsx, index=False)
            print(f"檔案: {file_with_right_sequence} 完成")
        except Exception as e:
            print(f"檔案: {file_with_right_sequence} 出大事 {e}")
            
        file_start += 1
        time.sleep(sleep_time)