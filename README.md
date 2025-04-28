# Master Thesis

**NLP 演算法與生成式 AI 模型評測，分析 ESG 新聞內容對市場異常報酬影響**。  
透過結合深度學習（Bi-LSTM)、Transformer 架構 (BERT、FinBERT、Further-pretrain FinBERT）、Generative AI（ChatGPT4o、Claude 3.7 Sonnet、Grok3、DeepSeek-V3、Gemma3-1B、LLaMA 3.2-1B）與事件研究法，進行演算法評測，以及驗證文字探勘變數與市場的關聯性。

---
## 📁 Langchain  
建構 ESG 新聞分析的生成式 AI 推理流程，透過 LangChain 框架封裝多種 LLMs，包含：
- **雲端模型**：OpenAI、Anthropic、DeepSeek、XAI 等
- **地端模型**：整合 Ollama 架設的本地語言模型，LLaMA、Gemma3 小參數模型
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
- `Datasets` 載入、切分、轉換格式, `AutoTokenizer` 斷詞處理
- `AutoModelForSequenceClassification`，設定分類層輸出維度
- `Trainer` 完成訓練流程管理, DataCollatorWithPadding` 動態 padding
- `TrainingArguments` 設定 batch size、learning rate、logging 頻率與模型儲存條件
- `compute_metrics` 評估模型在 validation set 的 accuracy、F1-score、precision 與 recall

Bi-LSTM 模型建構  
- 自建 Bi-LSTM 雙向長短期記憶模型架構，支援多分類輸出與句子級分類
- 包含 Embedding 層、雙向 LSTM 隱藏層、Dropout 抑制 overfitting、Linear 分類層



---
## 📁 Event_Study  
股價資料擷取與處理
- `yfinance` 套件自動下載個股與 S&P500 歷史收盤價資料 (Auto_adjusted CLOSE)
- 每日報酬率 `.pct_change()`，補上第一天缺值

異常報酬計算邏輯
- 建立 Market Model 預測期望報酬, 估計期回歸個股報酬與市場報酬
- OLS 擬合模型並應用至事件期，推算預期報酬後計算 Abnormal Return（AR）
- 累積異常報酬（CAR）為 `event_window` 區間內 AR 加總，最終回傳完整分析表格

事件期間對齊與資料結構整理 
- 將模型預測結果與股價報酬資料進行對齊
- 建立含 ticker、事件時間、估計期/事件期股價、報酬、模型預測值的 DataFrame

---
## 📁 Utils_Experiment  
支援性處理
- 針對文章與句子進行 token 統計與輸入長度管理，支援 chunk 切割策略與模型輸入上限的設定，確保在實際生成階段不會出錯。
- 設計與記錄不同系統提示（system prompt）以利 prompt 策略調整，並比對不同模型的回應差異。
- 統計推論階段各模型的 token 使用數量與成本，建立估算邏輯，為模型選擇提供資源與效率依據。
- 輔助進行句子清洗、缺值偵測與欄位一致性檢查，確保模型訓練與分析資料的基本完整性。



---

## 📁 Testing_Data_process  
整體流程以 `pandas` 為主軸，進行大量資料欄位整理、句子切分、標註合併與分類結果整併等等。
- 對原始新聞進行句子切分與編碼，建立清晰的段落層級結構（句子編號、新聞 ID 對應、段落對齊）
- 整合 researcher 標註與多個 NLP 模型的預測結果，處理欄位對應、資料去重與欄位重構
- 檢查分類一致性與模型結果差異，對出現衝突或不一致的樣本進行標記與記錄
- 清理標點錯誤、空值欄位、無效資料等，確保每筆資料在格式與內容上皆符合輸入標準
- 將所有處理結果整併為標準格式的 dataframe，為後續訓練與分析模組提供統一資料接口
  
---

## 📁 Result_post_process
整體以 `pandas` 以及統計操作為主，結果整併與格式標準化 
- 將各模型輸出整合成一份 dataframe，支援句子層級與文章層級分析。
- 建立統一欄位命名規則與欄位順序，讓所有模型結果具備可比性。
- 對句子分數做加權平均或簡單平均，建立新聞層級變數供回歸使用。
- 整合新聞與事件研究模組產生的 CAR 結果，產出最終回歸分析資料表。
  
統計分析與迴歸準備  
- 建立多個回歸變數，整理為 regression-ready 格式。
- OLS 執行橫斷面回歸分析，分析各模型預測變數對 CAR 的解釋力與顯著性。
- 將回歸結果與統計量輸出為表格，供論文撰寫與圖表繪製使用。

