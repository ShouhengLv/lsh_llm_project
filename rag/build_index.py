import os
import faiss
import pickle
import numpy as np
import onnxruntime
from transformers import BertTokenizer  # 或 AutoTokenizer 取决于模型

# ========== 参数设置 ==========
MODEL_PATH = "./models/text2vec/model.onnx"
TOKENIZER_PATH = "./models/text2vec"
DATA_PATH = "data/docs.txt"
INDEX_PATH = "rag/index.faiss"
CORPUS_PATH = "rag/corpus.pkl"
MAX_LINES = 100
BATCH_SIZE = 32

# ========== 初始化 tokenizer 和 ONNX session ==========
tokenizer = BertTokenizer.from_pretrained(TOKENIZER_PATH)
session = onnxruntime.InferenceSession(MODEL_PATH, providers=["CPUExecutionProvider"])

# ========== 读取前 MAX_LINES 行文本 ==========
docs = []
with open(DATA_PATH, "r", encoding="utf-8") as f:
    for i, line in enumerate(f):
        if i >= MAX_LINES:
            break
        line = line.strip()
        if line:
            docs.append(line)

print(f"✅ 成功加载文本数量: {len(docs)}")

# ========== 批量编码函数 ==========
def encode(texts, batch_size=32):
    all_embeddings = []

    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        inputs = tokenizer(batch, return_tensors="np", padding=True, truncation=True, max_length=128)

        # 补全 token_type_ids（有些模型如 RoBERTa 不提供）
        if "token_type_ids" not in inputs:
            inputs["token_type_ids"] = np.zeros_like(inputs["input_ids"])

        ort_inputs = {
            "input_ids": inputs["input_ids"].astype(np.int64),
            "attention_mask": inputs["attention_mask"].astype(np.int64),
            "token_type_ids": inputs["token_type_ids"].astype(np.int64)
        }

        ort_outputs = session.run(None, ort_inputs)
        batch_embeddings = ort_outputs[0][:, 0, :]  # 提取 CLS 向量
        all_embeddings.append(batch_embeddings)

    return np.vstack(all_embeddings)

# ========== 编码文本为向量 ==========
print("🚀 正在编码文本为向量 ...")
embeddings = encode(docs, batch_size=BATCH_SIZE)
print(f"✅ 向量维度: {embeddings.shape}")

# ========== 构建并保存 FAISS 索引 ==========
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

os.makedirs("rag", exist_ok=True)
faiss.write_index(index, INDEX_PATH)
with open(CORPUS_PATH, "wb") as f:
    pickle.dump(docs, f)

print("🎉 FAISS 索引构建完成，已保存到 rag/ 文件夹下")
