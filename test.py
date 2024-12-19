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

# 文件路径
success_file = 'dois_success.txt'
dois_file = 'dois.txt'

# 调用函数
process_files(success_file, dois_file)
