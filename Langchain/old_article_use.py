import pandas as pd
import os
import chardet
import json
import time
import re

# 確定 txt 檔案 encoding 
def dect_encoding(file):
    with open(file, "rb") as f:
            rawdata = f.read()
            result = chardet.detect(rawdata)
    return result["encoding"]

# 使用對應的 encoding 
def read_txt_with_exactly_encoding(file):
    with open(file, "r", encoding=dect_encoding(file)) as f:
        text = f.read()
    return text

# 防止 LLM return 格式有問題
def extract_json(text: str):
    pattern = re.compile(r'({.*})', re.DOTALL)
    match = pattern.search(text)
    if match:
        json_str = match.group(1)
        return json_str
    else:
        text


# 將所有 txt 檔案餵入模型，並記錄結果。
def article_run(answer_list, model_name: str, chain, input_folder, prompt_topic: str, output_file, file_start: int, sleep_time: int):
    for file in range(len(os.listdir(input_folder))-file_start+1): 
        file_with_right_sequence = str(file_start)+".txt"
        file_use = os.path.join(input_folder, file_with_right_sequence)
        
        try:  
            text = read_txt_with_exactly_encoding(file_use)
            result = chain.invoke({"value":text})
            result_content = json.loads(extract_json(result))
            print(f'{file_with_right_sequence}: {result_content["thinking_process"], result_content["number"]}')
            number_answer = result_content["number"]
            answer_list.append(number_answer)
        except Exception as e:
            print("【出事】 請將 if_bug_happen_change_answer_list_to_this_one 的結果丟回去重跑")
            print(f"Exception:{e}, Response:{result}")
            return answer_list 
            
        time.sleep(sleep_time)
        file_start += 1
        print(answer_list)

    topic_list = ['Readability', 'Subjectivity', 'GreenWashing', 'Ambiguity', 'Timeliness']
    for topic in topic_list:
        if prompt_topic == topic:
            column_name = model_name+"_"+topic.lower()
        else:
            pass
    
    file = output_file
    df = pd.read_excel(file)
    df[column_name] = answer_list
    
    df.to_excel(file, index=False)
    print(f"{column_name} 完成")
    df
    return answer_list



