import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import time
import os
import logging
from logging.handlers import RotatingFileHandler
from prettytable import PrettyTable

# 配置日志
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(message)s')   # 配置日志记录器
logger = logging.getLogger('User_record')                   # 获取 Logger 对象
file_handler = RotatingFileHandler('run.log', mode='a', encoding='utf-8')
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
file_handler.setFormatter(formatter)                        # 创建日志格式器
logger.addHandler(file_handler)     # 将 FileHandler 添加到 Logger 对象中

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.1'
}
proxies = {
    'http': 'http://127.0.0.1:7890',
    'https': 'http://127.0.0.1:7890',
}           # 根据你自己设置的代理端口而定


def proxy_zdaye(page_num):  # 传入爬取的页数
    # url格式                                                               # 构造请求头
    url_pattern = 'https://www.zdaye.com/free/{}/'
    collect_proxies = []
    logger.info('爬取代理网站主域名:www.zdaye.com')
    for index in tqdm(range(1, page_num+1), desc='爬取进度'):
        url = url_pattern.format(index)
        try:                                                                # 尝试访问url，站大爷网站检测代理，不能使用代理
            response = requests.get(url=url, headers=headers)
            bs = BeautifulSoup(response.content, 'html.parser')
            # 查找table标签内的tr标签
            for row in bs.find_all('tr'):
                cols = row.find_all('td')
                if len(cols) >= 2:                                          # 代理ip判定
                    proxy = cols[0].text+':'+cols[1].text
                    # 加入代理列表中
                    collect_proxies.append(proxy)
                    # print(proxy)
            time.sleep(1)
        except:
            print('failed to fetch')
    return collect_proxies


def proxy_kuaidaili(page_num):
    collect_proxies = list()
    url_pattern = ['https://www.kuaidaili.com/free/inha/{}',
                   'https://free.kuaidaili.com/free/intr/{}']
    logger.info('爬取代理网站主域名:www.kuaidaili.com')
    for index in tqdm(range(1, page_num+1), desc='爬取进度'):
        for p in url_pattern:
            url = p.format(index)
            # logger.info('url:{}'.format(url))
            try:
                # 本地有代理可以添加proxies=proxies，没有需删去
                res = requests.get(url, headers=headers, proxies=proxies)
                if res.status_code != 200:
                    logger.info('it is blocked')
                    continue
                bs = BeautifulSoup(res.content, 'html.parser')
                # print(bs)
                scripts = bs.find_all('script')
                proxies_content = list()
                for script in scripts:
                    script_content = script.text
                    if 'fpsList' not in script_content:
                        continue
                    start_index = script_content.find(
                        'fpsList = [')+len('fpsList = ')
                    end_index = script_content.find('];')+1
                    proxies_content = eval(
                        script_content[start_index:end_index])
                    for i in proxies_content:
                        proxy = i['ip']+':'+i['port']
                        collect_proxies.append(proxy)
                time.sleep(1)
            except:
                logger.error('failed to fetch')
    return collect_proxies


def save2txt(proxies, file_name):
    with open(file_name, 'a+', encoding='utf-8') as f:                      # 将获取到的代理ip存入txt文件
        print('代理数据将存入文件{}中'.format(file_name))
        for proxy in proxies[:]:
            f.write('{}\n'.format(proxy))
    return


def proxies_info(collect_proxies):
    table = PrettyTable(['collect_proxies(ip:port)'])
    for i in collect_proxies:
        table.add_row([i])
    print(table)


if __name__ == '__main__':
    proxy_list = list()
    proxies_list = list()
    page_num = 3
    file_name = 'proxy_pool.txt'
    flag = True
    proxy_list = proxy_zdaye(page_num)
    if len(proxy_list) != 0:
        proxies_list += proxy_list
    proxy_list = proxy_kuaidaili(page_num)
    if len(proxy_list) != 0:
        proxies_list += proxy_list
    # 查看爬取数据
    while flag:
        option = input('是否查看爬取的数据(y/n):')
        if option == 'Y' or option == 'y':
            proxies_info(proxies_list)
            flag = False
        elif option == 'N' or option == 'n':
            flag = False
        else:
            print('The input format is wrong, please re-enter')
    # 保存
    flag = True
    while flag:
        option = input('是否保存爬取的数据(y/n):')
        if option == 'Y' or option == 'y':
            if os.path.exists(file_name):
                with open(file_name, 'w') as f:
                    f.truncate(0)  # 清空文本内容
            save2txt(proxies_list, file_name)
            flag = False
        elif option == 'N' or option == 'n':
            flag = False
        else:
            print('The input format is wrong, please re-enter')
