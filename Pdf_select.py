import os
import shutil
import pandas as pd

# 对应操作files目录下的内容 
# 地学院给出最终确定的文献列表 在所有已经下载过的pdf文献中找到并移动出来 未找到的目录和找到的目录都进行输出到txt中
# 后续需要下载四个not_found_documents.txt中的文献

# 配置路径
excel_path = "files/articles_qikan_normal.xlsx" # 需要的pdf文献列表 共分四个
# articles_lunwen_normal.xlsx、articles_qikan_good.xlsx、articles_qikan_normal.xlsx
pdf_folder_path = "files/pdf_articles_qikan" # 所有已经下载的pdf文献
output_folder = "files/articles_qikan_normal" # 需要的文献且已经下载的移动到该文件目录下
found_txt_path = "files/articles_qikan_normal/found_documents.txt" # 需要且已经下载
not_found_txt_path = "files/articles_qikan_normal/not_found_documents.txt" # 需要但是未下载 即未在所有已经下载的pdf文献中找到

# 创建输出目录
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 读取 Excel 文件
df = pd.read_excel(excel_path)
document_names = df.iloc[:, 0].astype(str).tolist()  # 获取第一列的文献名称

# 初始化结果列表
found_documents = []
not_found_documents = []

# 遍历文献名称，查找对应的 PDF 文件
for doc_name in document_names:
    found = False
    for filename in os.listdir(pdf_folder_path):
        if filename.lower().endswith('.pdf') and doc_name.lower() in filename.lower(): # 文件名字部分完全匹配excel中的名字 
        # 文件名字不完全匹配excel中的名字  下载的pdf可能因为名字太长中间自动加了省略号 前13个字符一模一样即可
        # if filename.lower().endswith('.pdf') and filename[:13].lower() == doc_name[:13].lower(): 
            found_documents.append(doc_name)
            # 移动文件到新的目录
            shutil.move(os.path.join(pdf_folder_path, filename), os.path.join(output_folder, filename))
            found = True
            break
    if not found:
        not_found_documents.append(doc_name)

# 保存找到的文献名称到 TXT 文件
with open(found_txt_path, 'w', encoding='utf-8') as file:
    for doc_name in found_documents:
        file.write(f"{doc_name}\n")

# 保存找不到的文献名称到 TXT 文件
with open(not_found_txt_path, 'w', encoding='utf-8') as file:
    for doc_name in not_found_documents:
        file.write(f"{doc_name}\n")

print("处理完成。找到的文献和找不到的文献已分别保存在对应的TXT文件中。")
