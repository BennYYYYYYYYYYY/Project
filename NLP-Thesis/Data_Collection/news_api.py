import requests  
import pandas as pd 
import os

# API Endpoint
# Top Headlines (頭條新聞)，用於拉取最新的頭條新聞，支援篩選語言、來源和國家等：https://newsapi.org/v2/top-headlines 
# Everything (全文搜尋)，用於搜尋任意新聞文章，支援更細粒度的控制，例如日期範圍、排序方式等: https://newsapi.org/v2/everything
# Sources (新聞來源)，獲取支持的新聞來源列表: https://newsapi.org/v2/sources


# 通用參數
# apiKey:	API 授權密鑰，用於驗證請求。	your_api_key_here	必填，註冊後獲取。
# pageSize:	每頁返回的結果數量，預設為 20。	5, 10, 100	最大值為 100。
# page:	指定要檢索的頁數。	1, 2, 3	與 pageSize 結合使用進行分頁操作。


# Top Headlines 專屬參數: 
# country: 指定新聞來源的國家。	us（美國）, tw（台灣）,	不可與 sources 同時使用。
# category: 篩選新聞類別。	business, technology,	不可與 sources 同時使用。
# sources: 指定具體的新聞來源。	bbc-news, cnn,	與 country 或 category 互斥。


# Everything 專屬參數
# q: 全文關鍵字檢索。	Apple, climate change,	支援邏輯操作符（如 AND, OR）。
# qInTitle: 只在標題中搜索關鍵字。	Bitcoin, AI,	僅搜索標題中的關鍵字，範圍較 q 更窄。
# from: 搜尋的開始日期（ISO 格式）。	2023-12-01,	僅適用於 everything，範圍不能超過 30 天。
# to: 搜尋的結束日期（ISO 格式）。	2023-12-10,	與 from 搭配使用進行範圍限制。
# sortBy: 排序方式。	relevancy, popularity,	默認為 relevancy（相關性排序）。


# Sources 專屬參數
# language:	篩選新聞來源的語言。	en, zh, es	僅適用於 sources 端點。
# country:	篩選新聞來源的國家。	us, tw, jp	與 category 可同時使用。
# category:	篩選新聞來源的類別。	technology, health	僅適用於 sources 端點。


api_key = ""  
base_url = ""  
search_query = "AI AND ESG"
result_csv = "news_urls.csv"

headers = {
    "User-Agent": ""
}

def fetch_news_urls(page):
    """從 News API 拉取新聞資料，返回 URL 清單"""
    params = {
        "apiKey": api_key,  
        "q": search_query,  
        "sortBy": "publishedAt",  # 按發布時間排序（默認新到舊）
        "pageSize": 100,  # 每頁返回最多 100 條
        "page": page,  # 當前分頁頁碼
    }

    response = requests.get(base_url, params=params, headers=headers)  # 發送 API 請求
    if response.status_code != 200:  
        print(f"API 請求失敗，狀態碼: {response.status_code}")
        print(response.text)
        return []
    
    data = response.json()  
    articles = data.get("articles", [])  # 可用資訊
    total_results = data.get("totalResults", 0) 
    print(total_results)
    urls = [{"url": article["url"], "published_at": article["publishedAt"]} for article in articles]  # 提取 URL 和發布時間
    return urls # list with dict

def save_to_csv(news_data):
    """將新的新聞 URL 和發布時間儲存到 CSV"""
    if os.path.exists(result_csv):  
        existing_data = pd.read_csv(result_csv) 
        existing_urls = set(existing_data["url"].tolist()) 
    else:
        existing_urls = set() 

    # 過濾出尚未儲存的數據
    new_data = [item for item in news_data if item["url"] not in existing_urls]

    if new_data:  # 如果有新的數據
        df_new = pd.DataFrame(new_data) 
        if os.path.exists(result_csv):  # 如果文件已存在
            df_new.to_csv(result_csv, mode="a", header=False, index=False)  # 以追加模式寫入，不加表頭
        else:
            df_new.to_csv(result_csv, index=False)  # 如果文件不存在，創建新文件
        print(f"已新增 {len(new_data)} 條新的新聞 URL 至 {result_csv}")
    else:
        print("未找到新的新聞 URL，無需更新。")



def main(page):
    """主函數，負責抓取單頁資料並存儲"""
    print(f"正在抓取第 {page} 頁的新聞...")
    news = fetch_news_urls(page)  # 抓取當前頁面的數據
    if news:  # 如果有數據
        save_to_csv(news)  # 保存數據到 CSV
    else:
        print("沒有抓取到任何數據，請檢查 API 請求或參數。")
    print(f"第 {page} 頁抓取完成，程式結束。")



# 確定csv中是否有重複url
def check_duplicates_in_csv(csv_file):
    """檢查 CSV 文件中的重複 URL
    Args:
        csv_file (str): CSV 文件的名稱
    Returns:
        bool: 是否有重複 URL
    """
    if not os.path.exists(csv_file):  # 如果文件不存在，提示用戶
        print(f"{csv_file} 文件不存在。")
        return False
    
    # 讀取 CSV 文件
    data = pd.read_csv(csv_file)

    # 檢查是否有重複 URL
    duplicate_count = data.duplicated(subset="url").sum()  # 檢查 DataFrame 中是否存在重複的值，返回一個布林值的 Series，與 DataFrame 的行數相同。 如果某行是重複的，對應的值為 True；否則為 False。
    if duplicate_count > 0:
        print(f"檔案中存在 {duplicate_count} 個重複的 URL。")
        print(len(data))
    else:
        print("檔案中沒有重複的 URL。")
        print(len(data))


