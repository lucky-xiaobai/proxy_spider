import requests
from tqdm import tqdm
from prettytable import PrettyTable


# url = 'http://www.baidu.com'

# proxies = {
#     'http': 'http://222.174.178.122:4999',
#     'https': 'https://222.174.178.122:4999'
# }
# try:
#     response = requests.get(url, proxies=proxies, timeout=5)
#     if response.status_code == 200:
#         print('代理IP可用:', proxies)
# except:
#     print('代理IP不可用:', proxies)


def url_test(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print('本地ip可以访问该url:{}'.format(url))
            return 1
    except:
        print('本地ip不可以访问该url:{}'.format(url))
        print('请重新设置合适的url进行测试')
        return 0


def proxy_info(file_name):
    table = PrettyTable(['ip:port'])
    print('{}文件中的信息如下'.format(file_name))
    with open(file_name, 'r', encoding='utf-8') as f:
        text = f.readlines()
        for i in text:
            table.add_row([i[:-1]])
        print(table)


def proxy_test(url, file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        text = f.readlines()
        proxies_alive = list()
        proxies_dead = list()
        for proxy in tqdm(text, desc='ip存活检测'):
            proxies = {
                'http': 'http://{}'.format(proxy[:-1]),
                'https': 'https://{}'.format(proxy[:-1])
            }
            # print(proxies)
            try:
                response = requests.get(
                    url, proxies=proxies, timeout=5)       # timeout=1
                if response.status_code == 200:
                    proxies_alive.append(proxy[:-1])
            except:
                proxies_dead.append(proxy[:-1])
        if len(proxies_alive) != 0:
            print('存活代理ip如下:')
            table = PrettyTable(['存活代理 ip:port'])
            for i in proxies_alive:
                table.add_row([i[:-1]])
            print(table)
        else:
            print('暂无存活代理')


if __name__ == '__main__':
    test_url = 'http://www.baidu.com'
    file_name = 'proxy_pool.txt'
    if url_test(test_url) == 1:
        proxy_info(file_name)
        proxy_test(test_url, file_name)
    exit()
