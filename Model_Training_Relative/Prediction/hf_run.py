import torch
import pandas as pd
import os
from tqdm.auto import tqdm

def hf_classification_run(model_name: str, variavle_name: str, model, tokenizer, input_folder, file_start: int):    
    # Inference mode
    model.eval() 
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)

    # Sorted with correct order
    file_list = sorted(os.listdir(input_folder), key=lambda x: int(x.split('.')[0]))
    file_list = file_list[file_start-1:]

    # Iterate every file by number
    for file_name in tqdm(file_list, desc="畢業畢業!!!!衝鴨!!!", leave=True):
        file_use = os.path.join(input_folder, file_name)
        number_answer_list = [] 

        df = pd.read_excel(file_use)
        sentences = df["sentence"].tolist()

        # Processing data with a batch size
        batch = 16
        for i in range(0, len(sentences), batch):
            batch_sentences = sentences[i:i+batch]

            inputs = tokenizer(batch_sentences, padding=True, truncation=True, max_length=128, return_tensors="pt")
            # move Tensor to the device that model use
            inputs = {k: v.to(device) for k, v in inputs.items()} 

            with torch.no_grad():
                outputs = model(**inputs)
                logits = outputs.logits
                prediction = torch.argmax(logits, dim=1)
                # move tensor from GPU back to CPU
                number_answer_list.extend(prediction.cpu().tolist())

        df[model_name+"_"+variavle_name] = number_answer_list

        try:
            df.to_excel(file_use, index=False)
        except Exception as e:
            tqdm.write(f"檔案: {file_name} 出事 {e}")
            
        file_start += 1
        

