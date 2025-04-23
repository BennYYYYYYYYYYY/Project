# Master Thesis

本專案為我的碩士論文研究開發儲存庫，主題聚焦於 **運用自然語言處理演算法與生成式 AI 模型，分析 ESG 新聞內容對股市異常報酬的影響**。  
透過結合深度學習（Bi-LSTM、BERT、FinBERT、Further-pretrain FinBERT）、Generative AI（ChatGPT4o、Claude 3.7 Sonnet、Grok3、DeepSeek-V3、Gemma3-1B、LLaMA 3.2-1B）與事件研究法，進行演算法評測，以及驗證文字探勘變數與市場的關聯性。

---
📁 langchain  
使用 LangChain 封裝各類生成式 AI 模型（ChatGPT, Claude, Grok 等），進行 ESG 新聞的零樣本 / 少樣本 / CoT 推理分析。  
模組化設計每個模型對應的 Prompt 邏輯與輸出格式，支援 JSON 解析、結果結構統一化、錯誤排除等。  
實作自動化流程，包含：few-shot 樣本更新、模型綁定、invoke 呼叫與結果儲存。

---

📁 Training_Model  
實作 ESG 相關新聞的分類模型訓練流程，涵蓋：
- LSTM/Bi-LSTM 模型架構與超參數設置
- Hugging Face 上微調 BERT 與 FinBERT 模型
- Tokenizer 前處理、Dataset 建立與 DataLoader 載入優化
- TensorBoard 視覺化訓練進度與模型比較
強調可重複性與模組化邏輯設計，支援後續實驗組合快速切換。
---
📁 Event_Study  
實作事件研究法相關流程，依據經典文獻設計估計期與事件期分析邏輯。
- Yahoo Finance API 擷取股價資料（含處理休市日補值）
- 市場模型 / 常態模型計算預期報酬與異常報酬（AR/CAR）
- 統計檢定與結果視覺化（t-test, CAR bar chart）
流程強調時間對齊、資料完整性與財務理論一致性。
---
📁 Testing_Data_process  
針對 ESG 新聞資料進行清洗與結構化處理，包含：
- 去除重複與空白段落、自動標號、正規化句子
- 對應原始新聞與句子標註資料結構對齊
- 結合研究者標註與模型預測標籤（支援多模型比較）
特別著重於半自動化資料前處理流程，提升模型輸入資料品質。
---
📁 Result_post_process 
統整所有模型輸出結果與後處理分析，包含：
- 模型輸出匯整：合併 GenAI 與分類模型預測結果
- 評估指標計算（accuracy, F1, confusion matrix 等）
- ESG 維度分數的文章層級聚合與回歸資料表建立
- 對應股價事件資料進行橫斷面回歸前的整合處理
強調資料一致性、格式統一與結果可複用性。

