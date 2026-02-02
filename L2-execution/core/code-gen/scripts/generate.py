#!/usr/bin/env python3
"""
Code Generate - 代码生成主脚本
根据需求描述生成代码。
"""

import json
import sys
import re
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional
from pathlib import Path


@dataclass
class GeneratedFile:
    """生成的文件"""
    path: str
    content: str
    language: str


@dataclass
class GenerationResult:
    """生成结果"""
    code: str
    files: List[GeneratedFile]
    imports: List[str]
    functions: List[str]
    classes: List[str]
    quality_score: float


# 语言模板
TEMPLATES = {
    "python": {
        "function": '''def {name}({params}) -> {return_type}:
    """{docstring}"""
    {body}
''',
        "class": '''class {name}:
    """{docstring}"""

    def __init__(self{init_params}):
        {init_body}
''',
        "imports": "from typing import {types}",
    },
    "javascript": {
        "function": '''/**
 * {docstring}
 */
function {name}({params}) {{
    {body}
}}
''',
        "class": '''/**
 * {docstring}
 */
class {name} {{
    constructor({init_params}) {{
        {init_body}
    }}
}}
''',
    },
    "typescript": {
        "function": '''/**
 * {docstring}
 */
function {name}({params}): {return_type} {{
    {body}
}}
''',
        "class": '''/**
 * {docstring}
 */
class {name} {{
    constructor({init_params}) {{
        {init_body}
    }}
}}
''',
    },
}


def extract_requirements(requirement: str) -> Dict[str, Any]:
    """从需求描述中提取结构化信息"""
    info = {
        "functions": [],
        "classes": [],
        "operations": [],
    }

    # 提取函数需求
    func_patterns = [
        r"函数[：:]\s*(\w+)",
        r"function[：:]\s*(\w+)",
        r"实现\s*(\w+)\s*函数",
        r"创建\s*(\w+)\s*方法",
    ]

    for pattern in func_patterns:
        matches = re.findall(pattern, requirement, re.IGNORECASE)
        info["functions"].extend(matches)

    # 提取类需求
    class_patterns = [
        r"类[：:]\s*(\w+)",
        r"class[：:]\s*(\w+)",
        r"创建\s*(\w+)\s*类",
    ]

    for pattern in class_patterns:
        matches = re.findall(pattern, requirement, re.IGNORECASE)
        info["classes"].extend(matches)

    # 提取操作
    operations = ["增删改查", "CRUD", "读取", "写入", "验证", "转换", "计算"]
    for op in operations:
        if op.lower() in requirement.lower():
            info["operations"].append(op)

    return info


def generate_function_code(
    name: str,
    language: str,
    requirement: str
) -> str:
    """生成函数代码"""
    template = TEMPLATES.get(language, TEMPLATES["python"])["function"]

    # 简单的参数推断
    params = "self" if "方法" in requirement else ""

    # 简单的返回类型推断
    return_type = "Any"
    if "返回" in requirement:
        if "列表" in requirement or "list" in requirement.lower():
            return_type = "List[Any]"
        elif "字典" in requirement or "dict" in requirement.lower():
            return_type = "Dict[str, Any]"
        elif "布尔" in requirement or "bool" in requirement.lower():
            return_type = "bool"
        elif "数字" in requirement or "int" in requirement.lower():
            return_type = "int"

    code = template.format(
        name=name,
        params=params,
        return_type=return_type,
        docstring=requirement[:100],
        body="pass  # TODO: Implement"
    )

    return code


def generate_class_code(
    name: str,
    language: str,
    requirement: str
) -> str:
    """生成类代码"""
    template = TEMPLATES.get(language, TEMPLATES["python"])["class"]

    code = template.format(
        name=name,
        docstring=requirement[:100],
        init_params="",
        init_body="pass  # TODO: Initialize"
    )

    return code


def generate_imports(language: str, info: Dict[str, Any]) -> List[str]:
    """生成导入语句"""
    imports = []

    if language == "python":
        imports.append("from typing import Any, List, Dict, Optional")
        if info.get("operations"):
            imports.append("import logging")
    elif language in ("javascript", "typescript"):
        pass  # JavaScript 通常不需要基础导入

    return imports


def generate_code(
    requirement: str,
    language: str,
    framework: Optional[str] = None,
    context: Optional[Dict[str, Any]] = None,
    output_path: Optional[str] = None
) -> GenerationResult:
    """
    主生成函数

    Args:
        requirement: 需求描述
        language: 编程语言
        framework: 框架
        context: 上下文
        output_path: 输出路径

    Returns:
        GenerationResult
    """
    # 提取需求
    info = extract_requirements(requirement)

    # 生成导入
    imports = generate_imports(language, info)

    # 生成代码
    code_parts = []

    # 添加导入
    code_parts.extend(imports)
    code_parts.append("")  # 空行

    # 生成类
    classes = []
    for class_name in info["classes"]:
        code = generate_class_code(class_name, language, requirement)
        code_parts.append(code)
        classes.append(class_name)

    # 生成函数
    functions = []
    for func_name in info["functions"]:
        code = generate_function_code(func_name, language, requirement)
        code_parts.append(code)
        functions.append(func_name)

    # 如果没有提取到具体的函数/类，生成一个默认的
    if not classes and not functions:
        # 生成一个基于需求的默认函数
        default_name = "main_function"
        code = generate_function_code(default_name, language, requirement)
        code_parts.append(code)
        functions.append(default_name)

    # 合并代码
    full_code = "\n".join(code_parts)

    # 创建文件
    extension = {
        "python": ".py",
        "javascript": ".js",
        "typescript": ".ts",
        "java": ".java",
        "go": ".go",
    }.get(language, ".txt")

    file_path = output_path or f"generated{extension}"
    files = [GeneratedFile(
        path=file_path,
        content=full_code,
        language=language
    )]

    # 计算质量分数（简化）
    quality_score = 0.7
    if imports:
        quality_score += 0.1
    if classes or functions:
        quality_score += 0.1
    if len(full_code) > 100:
        quality_score += 0.05

    return GenerationResult(
        code=full_code,
        files=files,
        imports=imports,
        functions=functions,
        classes=classes,
        quality_score=min(quality_score, 1.0)
    )


def main():
    """CLI 入口"""
    import argparse

    parser = argparse.ArgumentParser(description="Code Generator")
    parser.add_argument("--requirement", "-r", type=str, required=True,
                        help="Requirement description")
    parser.add_argument("--language", "-l", type=str, default="python",
                        help="Programming language")
    parser.add_argument("--framework", "-f", type=str, help="Framework")
    parser.add_argument("--output", "-o", type=str, help="Output file path")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    result = generate_code(
        requirement=args.requirement,
        language=args.language,
        framework=args.framework,
        output_path=args.output
    )

    if args.json:
        output = asdict(result)
        output["files"] = [asdict(f) for f in result.files]
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        print("Generated Code:")
        print("=" * 50)
        print(result.code)
        print("=" * 50)
        print(f"\nFunctions: {result.functions}")
        print(f"Classes: {result.classes}")
        print(f"Quality Score: {result.quality_score}")


if __name__ == "__main__":
    main()
