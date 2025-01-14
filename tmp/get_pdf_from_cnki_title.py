#++++ 作者：@钟慧奇
#++++ 联系方式：QQ2857839127，邮箱huiqi2001@qq.com
#++++ 用途：通过DOI到知网下载对应论文（仅限知网上能够找到的论文）
#++++ 注意：请确保已经安装asyncio、pyppeteer等第三方库以及chromium！！！
#++++ 2024年1月23日

import asyncio
import pyppeteer as pyp
import time

#为page添加反反爬措施
async def antiAntiSpider(page):
    await page.setUserAgent("Mazilla/5.0 (Windows NT 10.0; Win64; x64) \
        AppleWebKit/537.36 (KHTML,like Gecko)\
        Chrome/122.0.6261.0 Safari/537.36")
    await page.evaluateOnNewDocument(
        '() =>{ Object.defineProperties(navigator,'
        '{ webdriver:{ get: () => false } }) }')

async def pdfDownFromCNKI(dois):        # dois为需要下载论文的doi列表
    width, height = 1400, 800                     # 网页宽高
    browser = await pyp.launch(headless=False,
        executablePath = "./chrome-win/chrome.exe",
        userdataDir = "./tmp",    
        args=[f'--window-size={width},{height}']) # 创建浏览器对象browser
    page = await browser.newPage()                # 打开新的标签页page
    await antiAntiSpider(page)                    # 反反爬措施
    await page.setViewport({'width': width, 'height': height})
    url = "https://www.cnki.net/"
    await page.goto(url)               # 进入网站
    time.sleep(40)                     # 程序暂停45秒,等待验证登录  

    for doi in dois:
        page2 = await browser.newPage()    # 打开新的标签页page2
        await antiAntiSpider(page2)                   # 反反爬措施
        await page2.setViewport({'width': width, 'height': height}) 
        await page2.goto(url)
        time.sleep(1.5)

        element = await page2.querySelector("#DBFieldBox > div.sort-default > span")
        await element.click()
        await page2.waitForSelector("#DBFieldList > ul > li:nth-child(16) > a",timeout=30000);   # 等待页面跳转出现doi
        #time.sleep(0.5)
        #element = await page2.querySelector("#DBFieldList > ul > li:nth-child(16) > a")
        element = await page2.querySelector("#DBFieldList > ul > li:nth-child(4) > a")
        await element.click()
        
        time.sleep(0.5)
        element = await page2.querySelector("#txt_SearchText")
        await element.type(doi)
        element = await page2.querySelector("body > div.wrapper.section1 > div.searchmain > div > div.input-box > input.search-btn")
        await element.click()
        await page2.waitForNavigation();   # 等待页面跳转
        time.sleep(2)
        #await page2.waitForSelector("#gridTable > div > div > table > tbody > tr > td.name > a",timeout=30000);   # 等待页面跳转出现文章
        element = await page2.querySelector("#gridTable > div > div > table > tbody > tr > td.name > a")
        # 获取href属性
        obj = await element.getProperty("href")
        url_new= await obj.jsonValue()
        
        #在新页面(标签)中装入新网页page3
        page3 = await browser.newPage()                # 打开新的标签页page3
        await antiAntiSpider(page3)                    # 反反爬措施
        await page3.setViewport({'width': width, 'height': height})
        await page3.goto(url_new)
        time.sleep(1)
        element = await page3.querySelector("#pdfDown")
        
        num_index = dois.index(doi)
        print(num_index)
        if num_index == 0:
            await element.click()
        else:
            if (num_index % 30) == 0:
                await element.click()
                input("下载数量达到30，请滑动进度条验证，准备好了回车")
            else:
                await element.click()
        time.sleep(1)
        await page2.close()     # 关闭页面page2
        await page3.close()     # 关闭页面page3
        
        # 程序暂停,等待选择
        if doi == dois[-1]:
            input()
            await browser.close()       # 关闭浏览器
        else:
            pass
        
        file_path_of_dois_down = 'D:/Py_File_2023/QiJi_20240122_webdrive/dois_down.txt'
        with open(file_path_of_dois_down, 'a', encoding="utf-8") as f:
            f.write("%s\t完成\n" % doi)

'''
file_path_of_dois = 'dois.txt'   
with open(file_path_of_doi, 'r', encoding="utf-8") as f:
    content = f.read()
dois = content.split("\n")
'''
titles = ["基于全卷积神经网络多任务学习的时域语音分离"]

# 半自动下载知网pdf文档
goto_weibo = asyncio.ensure_future(pdfDownFromCNKI(titles))     # 协程外启动协程
asyncio.get_event_loop().run_until_complete(goto_weibo)   # 等待协程结束
