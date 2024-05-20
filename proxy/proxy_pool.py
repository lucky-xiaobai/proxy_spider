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


# 站大爷
def proxy_zdaye(page_num):  # 传入爬取的页数
    # url格式                                                               # 构造请求头
    url_pattern = 'https://www.zdaye.com/free/{}/'
    collect_proxies = []
    logger.info('primary domain name:www.zdaye.com')
    for index in tqdm(range(1, page_num+1), desc='progress'):
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


# 快代理
def proxy_kuaidaili(page_num):
    collect_proxies = list()
    url_pattern = ['https://www.kuaidaili.com/free/inha/{}',
                   'https://free.kuaidaili.com/free/intr/{}']
    logger.info('primary domain name:www.kuaidaili.com')
    for index in tqdm(range(1, page_num+1), desc='progress'):
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


# 云代理
def proxy_ip3366(page_num):
    collect_proxies = list()
    url_pattern = 'http://www.ip3366.net/free/?stype=1&page={}'
    logger.info('primary domain name:http://www.ip3366.net/')
    for index in tqdm(range(1, page_num+1), desc='progress'):
        url = url_pattern.format(index)
        try:
            response = requests.get(url=url, headers=headers, proxies=proxies)
            bs = BeautifulSoup(response.content, 'html.parser')
            # 查找table标签内的tr标签
            for row in bs.find_all('tr'):
                cols = row.find_all('td')
                if len(cols) >= 2:
                    proxy = cols[0].text+':'+cols[1].text
                    # 加入代理列表中
                    collect_proxies.append(proxy)
                    # logger.info(proxy)
            time.sleep(1)
        except:
            print('failed to fetch')
    return collect_proxies


def proxy_website_info(proxy_website):
    table = PrettyTable(['id', 'Free Proxy Sites'])
    for i in range(len(proxy_website)):
        table.add_row([i+1, proxy_website[i]])
    print(table)


def proxies_info(collect_proxies):
    while True:
        option = input('Whether to view the crawled data(y/n,default as y):')
        if option == 'Y' or option == 'y' or option == '':      # 直接回车默认为y
            table = PrettyTable(['collect_proxies(ip:port)'])
            for i in collect_proxies:
                table.add_row([i])
            print(table)
            break
        elif option == 'N' or option == 'n':
            break
        else:
            print('The input format is wrong, please re-enter')


def save2txt(proxies, file_name):
    while True:
        option = input('Whether to save the crawled data(y/n,default as n):')
        if option == 'Y' or option == 'y':
            if os.path.exists(file_name):
                with open(file_name, 'w') as f:
                    f.truncate(0)  # 清空文本内容
            with open(file_name, 'a+', encoding='utf-8') as f:                      # 将获取到的代理ip存入txt文件
                print('proxy data will be stored in {}'.format(file_name))
                for proxy in proxies[:]:
                    f.write('{}\n'.format(proxy))
            break
        elif option == 'N' or option == 'n' or option == '':
            break
        else:
            print('The input format is wrong, please re-enter')


if __name__ == '__main__':
    proxies_list = list()
    file_name = 'proxy_pool.txt'
    proxy_website = ['站大爷', '快代理', '云代理']
    note_id = list()
    while True:
        proxy_website_info(proxy_website)
        op = input('input id(quit with \'q\',default as n):')
        if op == 'q' or op == '':       # 直接回车默认为q
            break
        try:
            page_num = int(input('input page_num:'))    # 输入爬取的页数
        except:
            print('The input format is wrong,default set page_num as 1')
            page_num = 1
        proxy_list = list()
        if op == '1':
            proxy_list = proxy_zdaye(page_num)
        elif op == '2':
            proxy_list = proxy_kuaidaili(page_num)
        elif op == '3':
            proxy_list = proxy_ip3366(page_num)
        else:
            print('The input format is wrong, please re-enter')
        if len(proxy_list) != 0:
            for proxy in proxy_list:
                if proxy in proxies_list:       # 如果有跳过
                    continue
                proxies_list.append(proxy)
    if len(proxies_list) != 0:
        proxies_info(proxies_list)              # 查看爬取数据
        save2txt(proxies_list, file_name)       # save to txt
    else:
        print('proxies_list is null')
