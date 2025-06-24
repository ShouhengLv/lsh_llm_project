import json
import base64
from openai import OpenAI
from schema.validator import full_input_validate
from utils.retry import retry_on_exception
from utils.prompt_engineering import build_common_prompt,build_emotional_prompt

from rag.rag_engine import ONNXRetriever
from utils.prompt_engineering import build_prompt_with_rag


with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

client = OpenAI(
    api_key=config["api_key"],
    base_url="https://api.deepseek.com/v1"  # 使用deepseek
)


#普通一次性调用
@retry_on_exception(max_retries=3, delay=2)         #加入重试装置
def call_llm(prompt: str, image_bytes: bytes = None, temperature: float = None) -> str:
    
    if temperature is None:
        temperature = config.get("default_temperature", 0.7)


    try:
        # 构造 message
        if image_bytes:
            # 编码图像
            base64_image = base64.b64encode(image_bytes).decode("utf-8")
            messages = [{
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                ]
            }]
        else:
            # 纯文本模式
            messages = [{"role": "user", "content": prompt}]
        
        response = client.chat.completions.create(
            model=config["model"],
            messages=messages,
            temperature=temperature,
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        raise RuntimeError(f"API调用失败: {e}")


#多模态（图像兼容）&流式调用（打字机效果）
@retry_on_exception(max_retries=3, delay=2)         #加入重试装置
def call_llm_stream_multimodal(prompt: str, image_bytes: bytes = None, temperature: float = None):
    
    if temperature is None:
        temperature = config.get("default_temperature", 0.7)

    full_input_validate({"prompt": prompt, "temperature": temperature})         #输入校验
    
    #prompt engineering
    #prompt = build_common_prompt(prompt)       #普通架构的回答
    prompt = build_emotional_prompt(prompt)     #带情感色彩的回答
    
    #构建领域知识库增强，使用text2vec和FAISS索引，对输入构造结构化引导
    augmented_prompt = build_prompt_with_rag(prompt)


    try:
        # 构造 message
        if image_bytes:
            # 编码图像
            base64_image = base64.b64encode(image_bytes).decode("utf-8")
            messages = [{
                "role": "user",
                "content": [
                    {"type": "text", "text": augmented_prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                ]
            }]
        else:
            # 纯文本模式
            messages = [{"role": "user", "content": augmented_prompt}]
        
        response = client.chat.completions.create(
            model=config["model"],
            messages=messages,
            temperature=temperature,
            stream=True
        )
        
        for chunk in response:
            # chunk是OpenAI返回的对象，属性访问
            if chunk.choices and len(chunk.choices) > 0:
                delta = chunk.choices[0].delta
                content = getattr(delta, "content", None)
                if content:  # 只 yield 非空内容
                    yield content
                    
    except Exception as e:
        raise RuntimeError(f"API调用失败: {e}")
