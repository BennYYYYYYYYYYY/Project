import requests
import pandas as pd
import os
from datetime import datetime, timedelta

# API 參數
api_key = ""
base_url = "https://newsapi.org/v2/everything"
result_csv = "news_urls.csv"
search_query = "AI AND ESG"


# 時間參數
# start_date = "2024-12-04"  # 設定抓取的起始時間（新到舊）

def fetch_news_by_start_date(start_date):
    """
    按起始日期抓取新聞，每次返回最多 100 條。
    """
    current_date = datetime.strptime(start_date, "%Y-%m-%d") #  string parse time: 將字串解析成 datetime object
    all_news = []

    params = {
        "apiKey": api_key,
        "q": search_query,
        "sortBy": "publishedAt",
        "pageSize": 100,  # 每次返回最多 100 條
        "from": (current_date - timedelta(days=5)).strftime("%Y-%m-%d"),
        "to": current_date.strftime("%Y-%m-%d"),
    }

    response = requests.get(base_url, params=params)
    if response.status_code != 200:
        print(f"API 請求失敗，狀態碼：{response.status_code}, 錯誤訊息：{response.json()}")
        return []

    data = response.json()
    articles = data.get("articles", []) # 用來安全地從字典中取值，避免 KeyError
    print(f"成功抓取 {len(articles)} 條新聞，起始時間：{params['from']} 至 {params['to']}") # 

    # 提取需要的數據
    all_news.extend([{"url": article["url"], "published_at": article["publishedAt"]} for article in articles])

    return all_news

def save_to_csv(news_data):
    """
    將新聞數據保存到 CSV 文件，避免重複。
    """
    if os.path.exists(result_csv):
        existing_data = pd.read_csv(result_csv)
        existing_urls = set(existing_data["url"].tolist())
    else:
        existing_urls = set()

    # 過濾新數據
    new_data = [item for item in news_data if item["url"] not in existing_urls]
    if new_data:
        df_new = pd.DataFrame(new_data)
        if os.path.exists(result_csv):
            df_new.to_csv(result_csv, mode="a", header=False, index=False)
        else:
            df_new.to_csv(result_csv, index=False)
        print(f"已新增 {len(new_data)} 條新的新聞 URL 至 {result_csv}")
    else:
        print("未找到新的新聞 URL，無需更新。")

def main(start_date):
    """
    主函數，從指定起始時間抓取新聞並保存。
    """
    print(f"開始抓取新聞，起始時間：{start_date}")
    news = fetch_news_by_start_date(start_date)
    if news:
        save_to_csv(news)
    print("抓取完成！")

if __name__ == "__main__":
    main()
