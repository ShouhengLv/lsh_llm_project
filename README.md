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
* [rag/](.\lsh_llm_project\rag)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# 构建领域知识库增强
  * [build_index.py](.\lsh_llm_project\rag\build_index.py)
  * [corpus.pkl](.\lsh_llm_project\rag\corpus.pkl)
  * [index.faiss](.\lsh_llm_project\rag\index.faiss)
  * [rag_engine.py](.\lsh_llm_project\rag\rag_engine.py)
* [schema/](.\lsh_llm_project\schema)
  * [input_schema.py](.\lsh_llm_project\schema\input_schema.py)
  * [output_schema.py](.\lsh_llm_project\schema\output_schema.py)
  * [validator.py](.\lsh_llm_project\schema\validator.py)
  * [__init__.py](.\lsh_llm_project\schema\__init__.py)
* [utils/](.\lsh_llm_project\utils)
  * [prompt_engineering.py](.\lsh_llm_project\utils\prompt_engineering.py)
  * [retry.py](.\lsh_llm_project\utils\retry.py)
* [app_gui.py](.\lsh_llm_project\app_gui.py)
* [config.json](.\lsh_llm_project\config.json)
* [llm_interface.py](.\lsh_llm_project\llm_interface.py)
* [LLM_project数据流图_proc.jpg](.\lsh_llm_project\LLM_project数据流图_proc.jpg)
* [main.py](.\lsh_llm_project\main.py)
* [README.md](.\lsh_llm_project\README.md)
* [requirements.txt](.\lsh_llm_project\requirements.txt)
