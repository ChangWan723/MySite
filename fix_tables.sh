#!/bin/bash

# 修复表格前面缺少空行的问题
sed -i '/^### [0-9]\. 能量来源：/a\\' "_posts/AiGen/2026-03-23-MBTI人格类型测试详解与应用指南.md"
sed -i '/^### 2\. 信息获取：/a\\' "_posts/AiGen/2026-03-23-MBTI人格类型测试详解与应用指南.md"
sed -i '/^### 3\. 决策方式：/a\\' "_posts/AiGen/2026-03-23-MBTI人格类型测试详解与应用指南.md"
sed-i'/^### 4\. 生活方式：/a\\' "_posts/AiGen/2026-03-23-MBTI人格类型测试详解与应用指南.md"

# 在表格后面添加空行
sed -i '/^| 外向（E） | 内向（I） |/{N;N;N;N;N;N;N;N;N;N;N;N;N;N;N;N;a\\' "_posts/AiGen/2026-03-23-MBTI人格类型测试详解与应用指南.md"
sed-i'/| 感觉（S） | 直觉（N） |/{N;N;N;N;N;N;N;N;N;N;a\\'"_posts/AiGen/2026-03-23-MBTI人格类型测试详解与应用指南.md"
