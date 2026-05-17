#!/usr/bin/env python3
"""
将 YAML frontmatter 格式的 MDX 文件转换为 export const metadata 格式
用于修复多语言 MDX 文件的格式不一致问题
"""

import os
import re
from pathlib import Path

def convert_mdx_file(file_path):
    """将 YAML frontmatter 转换为 export const metadata"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 去掉开头的语言标识符（如 markdown\n 或 yaml\n）
    cleaned = re.sub(r'^(markdown|yaml|mdx)\s*\n', '', content.strip())

    # 检查是否已经是 export 格式
    if cleaned.startswith('export const metadata'):
        print(f"✓ Already converted: {file_path}")
        return False

    # 检查是否有 YAML frontmatter
    if not cleaned.startswith('---'):
        print(f"✗ No frontmatter found: {file_path}")
        return False

    # 提取 YAML frontmatter 和内容
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)$', cleaned, re.DOTALL)
    if not match:
        print(f"✗ Invalid frontmatter format: {file_path}")
        return False

    yaml_content = match.group(1)
    mdx_content = match.group(2)

    # 提取 import 语句
    imports = []
    remaining_lines = []
    for line in mdx_content.split('\n'):
        if line.strip().startswith('import '):
            imports.append(line)
        else:
            remaining_lines.append(line)

    # 解析 YAML 字段
    metadata_fields = []
    for line in yaml_content.split('\n'):
        line = line.strip()
        if not line or not ':' in line:
            continue

        key, value = line.split(':', 1)
        key = key.strip()
        value = value.strip()

        # 处理已经有引号的值
        if value.startswith('"') and value.endswith('"'):
            metadata_fields.append(f'  {key}: {value},')
        elif value.startswith("'") and value.endswith("'"):
            # 转换单引号为双引号
            value_content = value[1:-1]
            metadata_fields.append(f'  {key}: "{value_content}",')
        else:
            # 添加引号
            metadata_fields.append(f'  {key}: "{value}",')

    # 构建新内容
    new_content_parts = []

    # 添加 imports
    if imports:
        new_content_parts.extend(imports)
        new_content_parts.append('')

    # 添加 export const metadata
    new_content_parts.append('export const metadata = {')
    new_content_parts.extend(metadata_fields)
    new_content_parts.append('}')
    new_content_parts.append('')

    # 添加 MDX 内容 (去除开头的空行)
    content_start = False
    for line in remaining_lines:
        if not content_start and not line.strip():
            continue
        content_start = True
        new_content_parts.append(line)

    # 写回文件
    new_content = '\n'.join(new_content_parts)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"✓ Converted: {file_path}")
    return True

def main():
    """批量转换所有语言的全部 MDX 文件"""
    import sys
    base_dir = Path(__file__).parent.parent.parent / 'content'

    # 从命令行参数获取语言列表，默认处理所有语言
    if len(sys.argv) > 1:
        languages = sys.argv[1:]
    else:
        # 自动检测存在的语言目录
        languages = sorted([d.name for d in base_dir.iterdir() if d.is_dir()])

    print(f"开始转换 MDX 文件格式...\n语言: {languages}\n")

    converted_count = 0
    total_count = 0

    for lang in languages:
        lang_dir = base_dir / lang
        if not lang_dir.exists():
            print(f"⊘ Directory not found: {lang_dir}")
            continue

        print(f"\n处理 {lang.upper()} 语言文件:")
        for mdx_file in sorted(lang_dir.rglob('*.mdx')):
            total_count += 1
            if convert_mdx_file(mdx_file):
                converted_count += 1

    print(f"\n" + "="*60)
    print(f"✓ 转换完成: {converted_count}/{total_count} 个文件")
    print(f"="*60)

if __name__ == '__main__':
    main()
