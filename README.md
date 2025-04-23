# Master Thesis

**自然語言處理演算法與生成式 AI 模型評測，分析 ESG 新聞內容對市場異常報酬影響**。  
透過結合深度學習（Bi-LSTM、BERT、FinBERT、Further-pretrain FinBERT）、Generative AI（ChatGPT4o、Claude 3.7 Sonnet、Grok3、DeepSeek-V3、Gemma3-1B、LLaMA 3.2-1B）與事件研究法，進行演算法評測，以及驗證文字探勘變數與市場的關聯性。

---
## 📁 Langchain  
建構 ESG 新聞分析的生成式 AI 推理流程，透過 LangChain 框架封裝多種 LLMs，包含：
- **雲端模型**：OpenAI、Anthropic、DeepSeek、XAI 等
- **地端模型**：整合 Ollama 架設的本地語言模型，提升本地運算與資料保密性
- 利用 `PromptTemplate` 與 `FewShotPromptTemplate` 設計統一化的提示詞結構，自動化生成輸入格式  
- 模型綁定、推理呼叫、自動解析 JSON 輸出、錯誤處理
- 彈性支援 Zero-shot、Few-shot 與 Chain-of-thought Prompt Egineering
- 多模型結果輸出格式統一，方便後續比較分析與統整處理

---

## 📁 Training_Model  
訓練資料處理
- 情緒（Positive / Neutral / Negative)、ESG（E / S / G / None）
- 資料前處理、隨機抽樣與整合

Hugging Face 進行微調，包括：
- `Datasets` 載入、切分、轉換格式, `AutoTokenizer` 對文本進行斷詞處理
- `AutoModelForSequenceClassification`（如 BERT、FinBERT），依任務設定分類層輸出維度
- `Trainer` 完成訓練流程管理, DataCollatorWithPadding` 動態 padding
- `TrainingArguments` 設定 batch size、learning rate、logging 頻率與模型儲存條件
- `compute_metrics` 評估模型在 validation set 的 accuracy、F1-score、precision 與 recall

Bi-LSTM 模型建構  
- 自建 Bi-LSTM 雙向長短期記憶模型架構，支援多分類輸出與句子級分類
- 包含 Embedding 層、雙向 LSTM 隱藏層、Dropout 抑制 overfitting、Linear 分類層
- 支援 PyTorch 訓練流程與自定義 loss 計算


---
## 📁 Event_Study  
實作事件研究法相關流程，依據經典文獻設計估計期與事件期分析邏輯。
- Yahoo Finance API 擷取股價資料（含處理休市日補值）
- 市場模型 / 常態模型計算預期報酬與異常報酬（AR/CAR）
- 統計檢定與結果視覺化（t-test, CAR bar chart）
流程強調時間對齊、資料完整性與財務理論一致性。
---
## 📁 Testing_Data_process  
針對 ESG 新聞資料進行清洗與結構化處理，包含：
- 去除重複與空白段落、自動標號、正規化句子
- 對應原始新聞與句子標註資料結構對齊
- 結合研究者標註與模型預測標籤（支援多模型比較）
特別著重於半自動化資料前處理流程，提升模型輸入資料品質。
---
## 📁 Result_post_process 
統整所有模型輸出結果與後處理分析，包含：
- 模型輸出匯整：合併 GenAI 與分類模型預測結果
- 評估指標計算（accuracy, F1, confusion matrix 等）
- ESG 維度分數的文章層級聚合與回歸資料表建立
- 對應股價事件資料進行橫斷面回歸前的整合處理
強調資料一致性、格式統一與結果可複用性。

