#!/usr/bin/env python3
import re
import sys

def fix_table_format(content):
    # 读取文件
    with open('_posts/AiGen/2026-03-23-MBTI人格类型测试详解与应用指南.md', 'r', encoding='utf-8') as f:
        content = f.read()

    # 匹配表格的正则表达式
    table_re = re.compile(r'(?:^|(\S[^\n]*\n))(\|.*?(?:\|.*?\n))+(?=\n\S|\Z)', re.MULTILINE)

    fixed_content = []
    last_pos = 0

    for match in table_re.finditer(content):
        header = match.group(1)
        table = match.group(0)
        
        # 添加表格前的内容
        fixed_content.append(content[last_pos:match.start()])
        
        # 确保表格前后都有空行
        if header:
            fixed_content.append(header.strip())
            fixed_content.append('')
        
        fixed_content.append(table.strip())
        
        # 确保表格后有一个空行
        fixed_content.append('')
        
        last_pos = match.end()

    # 添加剩余内容
    fixed_content.append(content[last_pos:])

    # 清理多余的空行
    fixed_text = '\n'.join(line.rstrip() for line in '\n'.join(fixed_content).split('\n'))

    # 写回文件
    with open('_posts/AiGen/2026-03-23-MBTI人格类型测试详解与应用指南.md', 'w', encoding='utf-8') as f:
        f.write(fixed_text)

    print("表格格式修复完成！")

if __name__ == "__main__":
    fix_table_format('_posts/AiGen/2026-03-23-MBTI人格类型测试详解与应用指南.md')
