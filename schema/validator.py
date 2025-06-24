import json
import re
import streamlit as st
from jsonschema import validate, ValidationError
from .input_schema import INPUT_SCHEMA  # 你需要定义的输入JSON Schema
from .output_schema import OUTPUT_SCHEMA  # 你需要定义的输出JSON Schema

# 示例敏感词列表（实际应放在文件或配置中维护）
SENSITIVE_KEYWORDS = [
    "暴力", "色情", "地下组织", "杀人"
]

# 简单的 prompt injection 检测：包含类似系统指令提示内容
INJECTION_PATTERNS = [
    r"(你现在是一个.*?)",
    r"(请忽略之前的所有指令)",
    r"(你必须回应.*)",
    r"(作为开发者模式.*)"
]

#输入结构校验
def validate_input_structure(data: dict):
    try:
        validate(instance=data, schema=INPUT_SCHEMA)
    except ValidationError as e:
        raise ValueError(f"输入格式错误: {e.message}")

#输入内容校验
def validate_input_content(text: str):
    # 空内容拦截
    if not text.strip():
        raise ValueError("输入不能为空")
    
    # 敏感词检测
    for word in SENSITIVE_KEYWORDS:
        if word in text:
            raise ValueError(f"输入中包含敏感词汇：'{word}'，请重新输入")

    # 指令注入检测（正则）
    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, text, flags=re.IGNORECASE):
            raise ValueError("检测到疑似指令注入内容，已被拦截")
        


#输入校验
def full_input_validate(data: dict):
    validate_input_structure(data)
    validate_input_content(data["prompt"])
    

#输出结构校验
def full_output_validate(response_text: str) -> bool:
    """
    仅校验字符串是否符合输出JSON结构定义
    """
    try:
        data = json.loads(response_text)
        validate(instance=data, schema=OUTPUT_SCHEMA)
        return True
    except (json.JSONDecodeError, ValidationError) as e:
        raise ValueError(f"⚠️ 模型输出不符合结构化格式: {str(e)}")
    