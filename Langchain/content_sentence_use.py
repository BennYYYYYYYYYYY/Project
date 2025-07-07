import os 
import pandas as pd
import re
import json
import time

# 避免 '''JSON{} 的格式，只抓 {}
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


def content_sentence_run(model_name: str, chain, input_folder, prompt_topic: str, file_start: int, sleep_time: int):     
    for file in range(len(os.listdir(input_folder))-file_start+1):
        file_name = str(file_start)+".xlsx"
        file_use = os.path.join(input_folder, file_name)

        df = pd.read_excel(file_use)
        number_answer_list = [] # 新 column 資料

        for value in (df["sentence"]):
            result = chain.invoke({"value":value})
            
            # OpenAI SDK 格式轉換
            try:
                result = result.content
            except:
                pass
                
            # # 處理 '''JSON {}''' 情況
            # result = extract_json(result)


            # 處理 {} 沒括起來的情況
            if not result.strip().endswith("}"):
                    result += "}"

            try:
                result = json.loads(extract_json_2(extract_json(result)))
                print(result["thinking_process"], result["number"])
                number_answer = result["number"]
                number_answer_list.append(number_answer)
            except Exception as e:
                print(e, "------",result)

        topic_list = ['Readability', 'Subjectivity', 'GreenWashing', 'Ambiguity', 'Timeliness']
        for topic in topic_list:
            if prompt_topic == topic:
                column_name = model_name+"_"+topic.lower()
            else:
                pass
        
        df[column_name] = number_answer_list
        


        try:
            df.to_excel(file_use, index=False)
            print(f"檔案: {file_name} 完成")
        except Exception as e:
            print(f"檔案: {file_name} 出大事 {e}")
            
        file_start += 1
        time.sleep(sleep_time)
    
