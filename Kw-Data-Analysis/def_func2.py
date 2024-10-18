import pandas as pd
from pathlib import Path

def get_from_folder(folder_path):
    pathlib_Path_object = Path(folder_path)  # return Path object
    # .iterdir() 遍歷 Path object 路徑下的所有項目(包括檔案和子資料夾)。返回的 f 為 Path object(即為路徑)，若不須path可用 f.name。
    file_list = [f for f in pathlib_Path_object.iterdir() if f.is_file()]
    return file_list


def read_excel(path):
    data = pd.ExcelFile(path)
    df = data.parse(sheet_name=1)

    df = df.loc[:,['关键词', '点击量', '平均体量']]
    df.rename(columns={'关键词':"Keyword", '点击量':"Clicks", '平均体量':"Avg_Volume"}, inplace=True)

    df["Clicks"] = df["Clicks"].apply(lambda x: 0 if not isinstance(x, int) else x)
    df["Avg_Volume"] = df["Avg_Volume"].apply(lambda x: 0 if not isinstance(x, int) else x)

    df["Avg_Volume"] = df["Avg_Volume"].apply(lambda x: float(x))
    df["Clicks"] = df["Clicks"].apply(lambda x: float(x))

    df["CTR"] = (df["Clicks"] / df["Avg_Volume"]).apply(lambda x: round(x*100, 1))
    df.loc[df['Avg_Volume'].apply(lambda x: x == 0.0), 'CTR'] = 0.0

    df.sort_values(by="CTR", ascending=False, inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df



def group_by_kw(kw_list, df):
    if isinstance(kw_list, str):
        kw_list = [kw_list] 
        pattern = '|'.join(kw_list)

    yes_df = df.loc[df['Keyword'].str.contains(pattern, na=False, regex=True)]
    no_df = df.loc[~df['Keyword'].str.contains(pattern, na=False, regex=True)]

    yes_df.reset_index(drop=True, inplace=True)
    yes_df.loc[:, "CTR"] = yes_df["CTR"].apply(lambda x: str(x) + '%')
    no_df.reset_index(drop=True, inplace=True)
    no_df.loc[:, "CTR"] = no_df["CTR"].apply(lambda x: str(x) + '%')
    
    return yes_df, no_df



def organic_yes_to_excel(df, brandname):
    try:
        with pd.ExcelWriter(f"Organic_Yes_Brandname_CTR.xlsx", mode='a') as writer:
            df.to_excel(writer, sheet_name=brandname, index=False)
    except FileNotFoundError:
        print("No file existed, Creating a new file right away...")
        df.to_excel(f"Organic_Yes_Brandname_CTR.xlsx", sheet_name=brandname, index=False)
    else:
        print("processing...")



def organic_no_to_excel(df, brandname):
    try:
        with pd.ExcelWriter(f"Organic_No_Brandname_CTR.xlsx", mode='a') as writer:
            df.to_excel(writer, sheet_name=brandname, index=False)
    except FileNotFoundError:
        print("No file existed, Creating a new file right away...")
        df.to_excel(f"Organic_No_Brandname_CTR.xlsx", sheet_name=brandname, index=False)
    else:
        print("processing..")



def paid_yes_to_excel(df, brandname):
    try:
        with pd.ExcelWriter(f"Paid_Yes_Brandname_CTR.xlsx", mode='a') as writer:
            df.to_excel(writer, sheet_name=brandname, index=False)
    except FileNotFoundError:
        print("No file existed, Creating a new file right away...")
        df.to_excel(f"Paid_Yes_Brandname_CTR.xlsx", sheet_name=brandname, index=False)
    else:
        print("processing...")



def paid_no_to_excel(df, brandname):
    try:
        with pd.ExcelWriter(f"Paid_No_Brandname_CTR.xlsx", mode='a') as writer:
            df.to_excel(writer, sheet_name=brandname, index=False)
    except FileNotFoundError:
        print("No file existed, Creating a new file right away...")
        df.to_excel(f"Paid_No_Brandname_CTR.xlsx", sheet_name=brandname, index=False)
    else:
        print("processing..")






def organic_data_analysis(folder_path, brandname_list):
    path_list = get_from_folder(folder_path)    
    for path, brandname in zip(path_list, brandname_list):
        df = read_excel(path)
        yes_df, no_df = group_by_kw(brandname, df)
        organic_yes_to_excel(yes_df, brandname)
        organic_no_to_excel(no_df, brandname)  
    print("Done!!!!")


def paid_data_analysis(folder_path, brandname_list):
    path_list = get_from_folder(folder_path)
    for path, brandname in zip(path_list, brandname_list):
        df = read_excel(path)
        yes_df, no_df = group_by_kw(brandname, df)
        paid_yes_to_excel(yes_df, brandname)
        paid_no_to_excel(no_df, brandname)
    print("Done!!!!")

