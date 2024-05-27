# proxy_spider

## 环境需求

python>=3.8（低版本尚未测试）

第三方库直接根据`requirements.txt`安装，指令如下

```bash
pip install -r requirements.txt
```

## 运行

### 代理爬取

目前支持解析的网站：

1、站大爷

2、快代理

3、云代理    

直接运行`proxy_pool.py`即可，具体实现以下几个功能：

1、日志配置

2、爬取进度条展示

3、爬取数据保存(可选)

### 代理存活检测

直接运行`proxy_test.py`脚本即可，其中默认设置检测的目标网址为`http://www.baidu.com`，检测超时时间可修改，默认设置为5秒。可以根据最后展示的表格评估之前爬取的代理网址的质量

## 结果展示

### 代理爬取

爬取过程截图如下

<img src="https://cdn.jsdelivr.net/gh/lucky-xiaobai/CTFPicture/img/image-20240524130526170.png" alt="image-20240524130526170" style="zoom:80%;" />

日志截图如下

<img src="https://cdn.jsdelivr.net/gh/lucky-xiaobai/CTFPicture/img/image-20240524130601224.png" alt="image-20240524130601224" style="zoom:80%;" />



### 代理存活检测

<img src="https://cdn.jsdelivr.net/gh/lucky-xiaobai/CTFPicture/img/image-20240524131358238.png" alt="image-20240524131358238" style="zoom:80%;" />
