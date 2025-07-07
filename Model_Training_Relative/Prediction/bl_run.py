import pandas as pd
import os
import numpy as np
from tqdm.auto import tqdm
from tensorflow.keras.preprocessing.sequence import pad_sequences


def bi_lstm_classification_run(variavle_name: str, model, tokenizer, input_folder: str, file_start: int):
    # Sorted with correct order
    file_list = sorted(os.listdir(input_folder), key=lambda x: int(x.split('.')[0]))
    file_list = file_list[file_start-1:]

    # Iterate every file by number
    for file_name in tqdm(file_list, desc="畢業畢業!!!!衝鴨!!!"):
        file_use = os.path.join(input_folder, file_name)

        df = pd.read_excel(file_use)
        sentences = df["sentence"].tolist()

        # predict() 自帶 batch_size，為內部處理參數，回傳結果一定為輸入長度，不會因為 batch 而改變回傳長相 shape = (input_num, classification_num)
        sequences = tokenizer.texts_to_sequences(sentences)
        X = pad_sequences(sequences, maxlen=128, padding='post', truncating='post')

        predictions = model.predict(X, batch_size=16)
        predicted_classes = np.argmax(predictions, axis=1)

        df["Bi_LSTM_"+variavle_name] = predicted_classes

        try:
            df.to_excel(file_use, index=False)
        except Exception as e:
            tqdm.write(f"檔案: {file_name} 出大事啦！！！！！！！！ {e}")
            
        file_start += 1



    