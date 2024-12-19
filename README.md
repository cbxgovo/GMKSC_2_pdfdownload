

使用前请确保已经安装asyncio、pyppeteer等第三方库以及chromium！！！

chromium下载地址：
https://download-chromium.appspot.com/

如果你能打开的话可直接滑到官网下载地址最下面找到对应的下载，因为版本问题，自行下载可能需要修改代码中chromium对应的版本号

当然这里提供一个百度网盘链接，是代码中对应的版本:

链接：https://pan.baidu.com/s/1ek2ExkqzVf0BSyESoGwPpw?pwd=1234

提取码：1234

下载后请将文件解压后放到get_pdf_form_cnki.py所在的文件夹同一路径下。

activate PDFParser

运行方式：hello_cnki-master\dois.txt 贴入需要下载的文献的题目，一行一个

执行：python get_pdf_from_cnki.py

说明：get_pdf_from_cnki.py 中的87和102行用于下载期刊文献；对应的下面的代码行用于下载学位论文[因为页面的元素不一样 使用的时候按照文献的类型进行代码的注释和释放]

执行：python get_pdf_from_cnki.py

hello_cnki-master\dois.txt ：用于放需要下载的文献的题目

hello_cnki-master\dois_success.txt：文献成功下载的题目会自动进行记录

hello_cnki-master\dois_false.txt：文献下载失败的题目会自动进行记录

pip freeze > requirements.txt

pip install -r requirements.txt

---

参考开源仓库：

[知网文献半自动下载: 通过DOI从知网批量半自动下载对应论文（仅限知网上能够找到的论文） (gitee.com)](https://gitee.com/zhong_huiqi/hello_cnki)

一些问题：

- 30篇计数停止是全部可下的情况 没考虑有搜不到的
- 如何自动通过跳过滑块验证

# 知网文献半自动下载

#### 介绍

通过DOI从知网批量半自动下载对应论文（仅限知网上能够找到的论文）

#### 文档说明

1. dois.txt中隔行存放doi,可修改为自己的doi
2. dois_down.txt会在程序运行时同步 [成功抓取文献] 的doi，并且每次运行会将之前的清空，当然也可以自行更改代码
3. get_pdf_form_cnki.py为主程序

#### 使用说明

使用前请确保已经安装asyncio、pyppeteer等第三方库以及chromium！！！

chromium下载地址：
https://download-chromium.appspot.com/

如果你能打开的话可直接滑到官网下载地址最下面找到对应的下载，因为版本问题，自行下载可能需要修改代码中chromium对应的版本号

当然这里提供一个百度网盘链接，是代码中对应的版本:

链接：https://pan.baidu.com/s/1ek2ExkqzVf0BSyESoGwPpw?pwd=1234

提取码：1234

下载后请将文件解压后放到get_pdf_form_cnki.py所在的文件夹同一路径下。

当前时间为2024年1月27日
