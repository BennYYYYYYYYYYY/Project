import praw  # Python Reddit API Wrapper
import csv
import os

# 設定 Reddit API，初始化 praw.Reddit 實例
reddit = praw.Reddit(
    client_id='',       # Reddit API 的 client_id
    client_secret='',  # Reddit API 的 client_secret
    user_agent='', # 識別用戶端的 user_agent
)

# Subreddit 與關鍵字
subreddit = reddit.subreddit('EsgInvesting')  # 指定目標 Subreddit
keywords = ['ESG', 'AI']  # 搜尋的關鍵字列表
min_score = 10  # 設定最低分數過濾條件

# 儲存的 CSV 檔案名稱
csv_file = "filtered_posts.csv"

# 檢查是否已存在 CSV 檔案，若無則建立並寫入標題列
if not os.path.exists(csv_file):
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['id', 'title', 'score', 'created_utc', 'url', 'content'])
        writer.writeheader()  # 寫入標題列

# 載入已儲存的文章 ID，避免重複儲存
existing_ids = set()  # 使用集合儲存已存在的文章 ID
with open(csv_file, mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)  # 讀取 CSV 檔案
    for row in reader:
        existing_ids.add(row['id'])  # 將每個文章的 ID 加入集合

# 搜尋符合條件的貼文
results = []
subreddit = reddit.subreddit("all")
for submission in subreddit.search(query="ESG AI", limit=100):  # 使用搜尋 API 抓取包含 "ESG AI" 的貼文
    if submission.id in existing_ids:
        continue  # 如果文章 ID 已存在，跳過該文章

    # 確保標題和內文同時包含所有關鍵字
    title = submission.title.lower()  # 將標題轉為小寫以便搜尋
    selftext = submission.selftext.lower()  # 將內文轉為小寫以便搜尋
    combined_text = title + " " + selftext  # 合併標題與內文
    if all(keyword.lower() in combined_text for keyword in keywords):  # 檢查所有關鍵字是否存在
        if submission.score >= min_score :  # 確保分數達標
            results.append({
                'id': submission.id,  # 文章 ID
                'title': submission.title,  # 文章標題
                'score': submission.score,  # 文章分數
                'created_utc': submission.created_utc,  # 文章發表的時間戳
                'url': submission.url,  # 文章的 URL
                'content': submission.selftext  # 文章的內文
            })

# 將結果儲存到 CSV 檔案
if results:  # 如果有新文章符合條件
    with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['id', 'title', 'score', 'created_utc', 'url', 'content'])
        for post in results:
            writer.writerow(post)  # 將文章寫入 CSV 檔案

# 輸出結果到終端機
for post in results:
    print(f"Title: {post['title']}")
    print(f"Score: {post['score']}")
    print(f"URL: {post['url']}")
    print(f"Content: {post['content']}")
    print("-" * 50)  # 分隔線

print(f"共儲存 {len(results)} 篇文章到 {csv_file}")  # 輸出儲存的文章數量
