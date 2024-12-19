#++++ 作者：@钟慧奇
#++++ 联系方式：QQ2857839127，邮箱huiqi2001@qq.com
#++++ 用途：通过DOI到知网下载对应论文（仅限知网上能够找到的论文）
#++++ 注意：请确保已经安装asyncio、pyppeteer等第三方库以及chromium！！！
#++++ 2024年1月23日

import asyncio
import pyppeteer as pyp
import time

# 将处理过的文章名字在目录删除
def process_files(success_file, dois_file):
    # 读取dois_success.txt的最后一行
    with open(success_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        if not lines:
            print("dois_success.txt is empty.")
            return
        last_line = lines[-1].strip()
    
    # 读取dois.txt并查找最后一行内容的位置
    with open(dois_file, 'r', encoding='utf-8') as f:
        dois_lines = f.readlines()
    
    # 查找last_line在dois_lines中的位置
    try:
        index = dois_lines.index(last_line + '\n')
    except ValueError:
        print(f"'{last_line}' not found in {dois_file}.")
        return
    
    # 删除index及其之前的所有元素
    new_dois_lines = dois_lines[index + 1:]
    
    # 将修改后的内容写回dois.txt
    with open(dois_file, 'w', encoding='utf-8') as f:
        f.writelines(new_dois_lines)
    
    print(f"Updated {dois_file}. Removed elements before '{last_line}'.")

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
    # 已经存在登录状态不必要等候验证 
    time.sleep(2)                     # 程序暂停45秒,等待验证登录 

    for doi in dois:
        page2 = await browser.newPage()    # 打开新的标签页page2
        await antiAntiSpider(page2)                   # 反反爬措施
        await page2.setViewport({'width': width, 'height': height}) 
        await page2.goto(url)
        time.sleep(1.5)

        element = await page2.querySelector("#DBFieldBox > div.sort-default > span")
        await element.click()
        await page2.waitForSelector("#DBFieldList > ul > li:nth-child(4) > a",timeout=30000);   # 等待页面跳转出现doi  原来4是16 找DOI 改为篇名
        #time.sleep(0.5)
        element = await page2.querySelector("#DBFieldList > ul > li:nth-child(4) > a")   #  原来4是16 找DOI 
        await element.click()
        
        time.sleep(0.5)
        element = await page2.querySelector("#txt_SearchText")
        await element.type(doi)
        element = await page2.querySelector("body > div.wrapper.section1 > div.searchmain > div > div.input-box > input.search-btn")
        await element.click()
        await page2.waitForNavigation();   # 等待页面跳转
        time.sleep(3)

        #await page2.waitForSelector("#gridTable > div > div > table > tbody > tr > td.name > a",timeout=30000);   # 等待页面跳转出现文章
        # element = await page2.querySelector("#gridTable > div > div > table > tbody > tr > td.name > a") # 期刊用这行
        element = await page2.querySelector("#gridTable > div > div > table > tbody > tr > td.name > div > div > a.fz14") # 学位论文用这行
        if element is not None:
            # 获取href属性
            obj = await element.getProperty("href")
            url_new= await obj.jsonValue()
            
            
            #在新页面(标签)中装入新网页page3
            page3 = await browser.newPage()                # 打开新的标签页page3
            await antiAntiSpider(page3)                    # 反反爬措施
            await page3.setViewport({'width': width, 'height': height})
            await page3.goto(url_new)
            time.sleep(1)

            # element = await page3.querySelector("#pdfDown") # 期刊用这行

            # 学位论文用下面这几行
            element_list = await page3.querySelectorAll("#cajDown")
            if len(element_list) >= 2:
                element = element_list[1]
            else:
                element = None

            
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
            # 在处理到 dois 列表的最后一个元素时，暂停程序并等待用户输入，然后关闭浏览器。
            if doi == dois[-1]:
                input()
                await browser.close()       # 关闭浏览器
            else:
                pass
            
            # file_path_of_dois_down = 'D:/Py_File_2023/QiJi_20240122_webdrive/dois_down.txt'
            # 已经成功下载标记 输出
            file_path_of_dois_down = 'dois_success.txt'
            with open(file_path_of_dois_down, 'a', encoding="utf-8") as f:
                # f.write("%s\t完成\n" % doi)
                f.write("%s\n" % doi)
        else:
            print(f"Element not found for DOI: {doi}")
            file_path_of_dois_down = 'dois_false.txt'
            with open(file_path_of_dois_down, 'a', encoding="utf-8") as f:
                f.write("%s\n" % doi)
            await page2.close()


# 文件路径
success_file = 'dois_success.txt' # 已成功下载
dois_file = 'dois.txt' # 待处理
 
# 调用函数 删除处理过的文章列表
process_files(success_file, dois_file)

   
file_path_of_dois = 'dois.txt'
with open(file_path_of_dois, 'r', encoding="utf-8") as f:
    content = f.read()
dois = content.split("\n")

# 半自动下载知网pdf文档
goto_weibo = asyncio.ensure_future(pdfDownFromCNKI(dois))     # 协程外启动协程
asyncio.get_event_loop().run_until_complete(goto_weibo)   # 等待协程结束
