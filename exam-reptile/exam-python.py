import requests  
from bs4 import BeautifulSoup  
import pandas as pd  
import time  

# 获取网页源代码  
def get_html(url):  
    try:  
        response = requests.get(url, timeout=30)  
        response.encoding = 'gb2312'  
        return response.text  
    except Exception as e:  
        print(f"获取失败: {e}")  
        return None  

# 分析网页结构，提取数据  
def parse_html(html):  
    soup = BeautifulSoup(html, 'lxml')  
    tr_list = soup.find_all('tr', attrs={'bgcolor': '#FFFFFF'})  
    houses = []  

    for tr in tr_list:  
        house = {}  
        tds = tr.find_all('td')  

        # 打印当前行的 tds 存在性和数量，便于调试  
        print(f"当前行包含的 td 元素数量: {len(tds)}")  
        for idx, td in enumerate(tds):  
            print(f"td[{idx}]: {td}")  

        # 确保 td 元素个数足够  
        if len(tds) < 7:  
            continue  # 跳过没有足够数据的行  

        house["详细地址"] = tds[0].find('a').string.strip() if tds[0].find('a') else ""  
        house["详情链接"] = 'https://www.lgfdcw.com/cs/' + tds[0].find('a')['href'] if tds[0].find('a') else ""  
        house['房型'] = tds[2].string.strip() if tds[2] and tds[2].string else ""  
        house['户型'] = tds[3].string.strip() if tds[3] and tds[3].string else ""  
        house['面积'] = tds[4].string.strip()[:-2] + '平方米' if tds[4] and tds[4].string else ""  
        house['出售价格'] = tds[5].string.strip() if tds[5] and tds[5].string else ""  
        house['登记时间'] = tds[6].string.strip() if tds[6] and tds[6].string else ""  

        houses.append(house)  

    return houses

# 保存数据，CSV文件  
def save_to_csv(houseList, timestamp):  
    data = pd.DataFrame(houseList, columns=['详细地址', "详情链接", '房型', '户型', '面积', '出售价格', '登记时间', '修改时间戳'])  
    data['修改时间戳'] = timestamp  # 添加时间戳列  
    # 修改文件保存路径  
    data.to_csv(r'C:\Users\17462\Desktop\exam-python\hangzhou_housing_data.csv', index=False, encoding='utf-8-sig')  
    print("数据已保存为 C:\\Users\\17462\\Desktop\\exam-python\\hangzhou_housing_data.csv")  

# 主函数  
def main():  
    base_url = "https://www.lgfdcw.com/cs/"  
    all_houses = []  
    
    # 设定抓取页面的数量  
    for page in range(1, 6):  # 假设目标是抓取前5页  
        print(f"正在抓取第 {page} 页数据...")  
        html = get_html(f"{base_url}?page={page}")  # 拼接URL，进行分页  
        if html:  
            houses = parse_html(html)  
            all_houses.extend(houses)  
            time.sleep(1)  # 等待1秒以避免请求过快  
        
        if len(all_houses) >= 100:  # 如果已有100条数据，停止抓取  
            break  
    
    # 获取网站修改时间戳  
    timestamp = pd.Timestamp.now()  

    # 保存数据  
    save_to_csv(all_houses[:100], timestamp)  # 只保存前100条数据  

if __name__ == "__main__":  
    main()