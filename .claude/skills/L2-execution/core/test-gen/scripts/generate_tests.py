#!/usr/bin/env python3
"""
Test Generator - 测试生成脚本
为代码自动生成测试用例。
"""

import json
import sys
import re
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional
from pathlib import Path


@dataclass
class TestCase:
    """测试用例"""
    name: str
    function_under_test: str
    test_type: str  # unit, integration, edge_case
    description: str
    code: str


@dataclass
class TestGenerationResult:
    """测试生成结果"""
    test_code: str
    test_files: List[Dict[str, str]]
    test_cases: List[TestCase]
    coverage_estimate: float


# 测试模板
TEMPLATES = {
    "python": {
        "header": '''"""Tests for {module_name}"""
import pytest
from unittest.mock import Mock, patch
{imports}

''',
        "test_function": '''def test_{name}():
    """{description}"""
    # Arrange
    {arrange}

    # Act
    {act}

    # Assert
    {assertion}
''',
        "test_class": '''class Test{class_name}:
    """{description}"""

    def setup_method(self):
        """Set up test fixtures."""
        {setup}

{methods}
''',
        "parametrize": '''@pytest.mark.parametrize("{params}", [
    {values}
])
def test_{name}({params}):
    """{description}"""
    {body}
''',
    },
    "javascript": {
        "header": '''/**
 * Tests for {module_name}
 */
{imports}

''',
        "test_function": '''test('{name}', () => {{
    // Arrange
    {arrange}

    // Act
    {act}

    // Assert
    {assertion}
}});
''',
        "describe": '''describe('{class_name}', () => {{
    beforeEach(() => {{
        {setup}
    }});

{methods}
}});
''',
    }
}


def extract_functions(code: str, language: str) -> List[Dict[str, Any]]:
    """从代码中提取函数定义"""
    functions = []

    if language == "python":
        # 匹配 Python 函数
        pattern = r'def\s+(\w+)\s*\(([^)]*)\)\s*(?:->\s*([^:]+))?\s*:'
        for match in re.finditer(pattern, code):
            func_name = match.group(1)
            params_str = match.group(2)
            return_type = match.group(3) or "Any"

            params = []
            if params_str.strip():
                for p in params_str.split(','):
                    p = p.strip()
                    if p and p != 'self':
                        param_name = p.split(':')[0].split('=')[0].strip()
                        params.append(param_name)

            functions.append({
                "name": func_name,
                "params": params,
                "return_type": return_type.strip(),
            })

    elif language in ("javascript", "typescript"):
        # 匹配 JS/TS 函数
        pattern = r'(?:function\s+(\w+)|(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s*)?\([^)]*\)\s*(?::\s*\w+)?\s*=>)'
        for match in re.finditer(pattern, code):
            func_name = match.group(1) or match.group(2)
            functions.append({
                "name": func_name,
                "params": [],
                "return_type": "any",
            })

    return functions


def generate_unit_test(func: Dict[str, Any], language: str) -> TestCase:
    """为函数生成单元测试"""
    func_name = func["name"]
    params = func["params"]

    if language == "python":
        # 生成基本测试
        arrange = "# Set up test data"
        if params:
            arrange = "\n    ".join(f"{p} = None  # TODO: Set appropriate value" for p in params)

        param_str = ", ".join(params) if params else ""
        act = f"result = {func_name}({param_str})"
        assertion = "assert result is not None  # TODO: Add proper assertion"

        code = TEMPLATES["python"]["test_function"].format(
            name=f"{func_name}_basic",
            description=f"Test {func_name} basic functionality",
            arrange=arrange,
            act=act,
            assertion=assertion
        )

    elif language in ("javascript", "typescript"):
        arrange = "// Set up test data"
        act = f"const result = {func_name}();"
        assertion = "expect(result).toBeDefined();"

        code = TEMPLATES["javascript"]["test_function"].format(
            name=f"{func_name} basic test",
            arrange=arrange,
            act=act,
            assertion=assertion
        )
    else:
        code = f"// TODO: Generate test for {func_name}"

    return TestCase(
        name=f"test_{func_name}_basic",
        function_under_test=func_name,
        test_type="unit",
        description=f"Test {func_name} basic functionality",
        code=code
    )


def generate_edge_case_test(func: Dict[str, Any], language: str) -> TestCase:
    """为函数生成边界测试"""
    func_name = func["name"]

    if language == "python":
        code = f'''def test_{func_name}_edge_cases():
    """Test {func_name} edge cases"""
    # Test with None
    with pytest.raises((TypeError, ValueError)):
        {func_name}(None)

    # Test with empty input
    # result = {func_name}("")  # TODO: Adjust based on function signature
    # assert result == ...  # TODO: Expected behavior
'''
    else:
        code = f'''test('{func_name} edge cases', () => {{
    // Test with null/undefined
    expect(() => {func_name}(null)).toThrow();

    // Test with empty input
    // TODO: Add appropriate edge case tests
}});
'''

    return TestCase(
        name=f"test_{func_name}_edge_cases",
        function_under_test=func_name,
        test_type="edge_case",
        description=f"Test {func_name} edge cases",
        code=code
    )


def generate_tests(
    code: str,
    file_path: Optional[str] = None,
    language: str = "python",
    test_framework: Optional[str] = None,
    test_types: Optional[List[str]] = None
) -> TestGenerationResult:
    """
    主测试生成函数

    Args:
        code: 要测试的代码
        file_path: 文件路径
        language: 编程语言
        test_framework: 测试框架
        test_types: 测试类型

    Returns:
        TestGenerationResult
    """
    test_types = test_types or ["unit", "edge_case"]

    # 提取函数
    functions = extract_functions(code, language)

    if not functions:
        # 如果没有找到函数，创建一个占位测试
        functions = [{"name": "placeholder", "params": [], "return_type": "Any"}]

    # 生成测试用例
    test_cases = []
    test_code_parts = []

    # 添加头部
    module_name = Path(file_path).stem if file_path else "module"
    if language == "python":
        imports = f"from {module_name} import *" if file_path else "# TODO: Add imports"
        header = TEMPLATES["python"]["header"].format(
            module_name=module_name,
            imports=imports
        )
    else:
        imports = f"import {{ /* imports */ }} from './{module_name}';"
        header = TEMPLATES["javascript"]["header"].format(
            module_name=module_name,
            imports=imports
        )

    test_code_parts.append(header)

    # 为每个函数生成测试
    for func in functions:
        if "unit" in test_types:
            test_case = generate_unit_test(func, language)
            test_cases.append(test_case)
            test_code_parts.append(test_case.code)

        if "edge_case" in test_types:
            test_case = generate_edge_case_test(func, language)
            test_cases.append(test_case)
            test_code_parts.append(test_case.code)

    # 合并代码
    test_code = "\n".join(test_code_parts)

    # 确定测试文件名
    if file_path:
        base_name = Path(file_path).stem
        if language == "python":
            test_file_name = f"test_{base_name}.py"
        else:
            test_file_name = f"{base_name}.test.{language[:2]}"
    else:
        test_file_name = f"test_module.{'py' if language == 'python' else 'js'}"

    test_files = [{
        "path": test_file_name,
        "content": test_code
    }]

    # 估算覆盖率
    coverage_estimate = min(0.8, len(test_cases) * 0.15)

    return TestGenerationResult(
        test_code=test_code,
        test_files=test_files,
        test_cases=test_cases,
        coverage_estimate=coverage_estimate
    )


def main():
    """CLI 入口"""
    import argparse

    parser = argparse.ArgumentParser(description="Test Generator")
    parser.add_argument("--file", "-f", type=str, help="Code file to test")
    parser.add_argument("--code", "-c", type=str, help="Code string to test")
    parser.add_argument("--language", "-l", type=str, default="python")
    parser.add_argument("--framework", type=str, help="Test framework")
    parser.add_argument("--types", type=str, help="Comma-separated test types")
    parser.add_argument("--output", "-o", type=str, help="Output file")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    if args.file:
        code = Path(args.file).read_text(encoding='utf-8')
        file_path = args.file
    elif args.code:
        code = args.code
        file_path = None
    else:
        code = sys.stdin.read()
        file_path = None

    test_types = args.types.split(',') if args.types else None

    result = generate_tests(
        code=code,
        file_path=file_path,
        language=args.language,
        test_framework=args.framework,
        test_types=test_types
    )

    if args.output:
        Path(args.output).write_text(result.test_code, encoding='utf-8')
        print(f"Test file written to {args.output}")
    elif args.json:
        output = {
            "test_code": result.test_code,
            "test_files": result.test_files,
            "test_cases": [asdict(tc) for tc in result.test_cases],
            "coverage_estimate": result.coverage_estimate
        }
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        print("Generated Tests:")
        print("=" * 50)
        print(result.test_code)
        print("=" * 50)
        print(f"\nTest Cases: {len(result.test_cases)}")
        print(f"Estimated Coverage: {result.coverage_estimate:.0%}")


if __name__ == "__main__":
    main()
