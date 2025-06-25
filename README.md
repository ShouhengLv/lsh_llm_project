# lsh_llm_project
（多模态）大语言模型应用开发
# 大语言模型基础应用

本项目是人工智能基础课程期末大作业，实现基于deepseek-R1的智能问答机器人，支持不同temperature参数调节，输入输出结构校验，基础命令行交互。

## 运行环境

- Python 3.8+
- 依赖库见 requirements.txt

## 使用说明

1. 安装依赖：
pip install -r requirements.txt
2. 配置 API Key：
在 config.json 文件中填写你的OpenAI API Key。
3. 运行程序：
python main.py
4. 输入问题，查看不同 temperature 的回答。

## 项目结构
# lsh_llm_project

* [data/](.\lsh_llm_project\data)
  * [docs.txt](.\lsh_llm_project\data\docs.txt)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# RAG所用训练数据，数据来自百度的DuReader QA语料，由于时间和算力限制，仅用10000条数据进行训练
* [models/](.\lsh_llm_project\models)
  * [text2vec/](.\lsh_llm_project\models\text2vec)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# RAG所用训练embedding模型
* [rag/](.\lsh_llm_project\rag)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# 构建领域知识库增强，利用text2vec+faiss索引
  * [build_index.py](.\lsh_llm_project\rag\build_index.py)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# 构建向量索引
  * [corpus.pkl](.\lsh_llm_project\rag\corpus.pkl)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# 存储文本数据列表
  * [index.faiss](.\lsh_llm_project\rag\index.faiss)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# 存储向量索引
  * [rag_engine.py](.\lsh_llm_project\rag\rag_engine.py)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# 大语言模型知识增强接口
* [schema/](.\lsh_llm_project\schema)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# 定义输入输出规范
  * [input_schema.py](.\lsh_llm_project\schema\input_schema.py)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# 定义输入结构规范
  * [output_schema.py](.\lsh_llm_project\schema\output_schema.py)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# 定义输出结构规范
  * [validator.py](.\lsh_llm_project\schema\validator.py)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# 输入输出结构规范化和内容规范化校验
  * [__init__.py](.\lsh_llm_project\schema\__init__.py)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# 将schema标记为模块包
* [utils/](.\lsh_llm_project\utils)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# 功能模块
  * [prompt_engineering.py](.\lsh_llm_project\utils\prompt_engineering.py)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;#构建输入promp结构化引导
  * [retry.py](.\lsh_llm_project\utils\retry.py)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# 运行失败时重试
* [app_gui.py](.\lsh_llm_project\app_gui.py)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# 前端ui界面设计
* [config.json](.\lsh_llm_project\config.json)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# deepseek-R1连接信息
* [llm_interface.py](.\lsh_llm_project\llm_interface.py)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# 调用deepseek接收answer
* [LLM_project数据流图_proc.jpg](.\lsh_llm_project\LLM_project数据流图_proc.jpg)
* [main.py](.\lsh_llm_project\main.py)
* [README.md](.\lsh_llm_project\README.md)
* [requirements.txt](.\lsh_llm_project\requirements.txt)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# 需要导入的库

