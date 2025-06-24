import faiss
import pickle
import onnxruntime
import numpy as np
from transformers import AutoTokenizer

class ONNXRetriever:
    def __init__(self, index_path="rag/index.faiss", corpus_path="rag/corpus.pkl", top_k=3):
        self.index = faiss.read_index(index_path)
        with open(corpus_path, "rb") as f:
            self.corpus = pickle.load(f)
        self.top_k = top_k

        # 加载本地 tokenizer 和 ONNX 模型
        self.tokenizer = AutoTokenizer.from_pretrained("./models/text2vec")  # 你下载的目录
        self.session = onnxruntime.InferenceSession("./models/text2vec/model.onnx", providers=["CPUExecutionProvider"])

    def encode(self, texts):
        inputs = self.tokenizer(texts, padding=True, truncation=True, return_tensors="np")

        if "token_type_ids" not in inputs:
            inputs["token_type_ids"] = np.zeros_like(inputs["input_ids"])

        # 转换为 int64
        ort_inputs = {
            "input_ids": inputs["input_ids"].astype(np.int64),
            "attention_mask": inputs["attention_mask"].astype(np.int64),
            "token_type_ids": inputs["token_type_ids"].astype(np.int64),
        }

        ort_outs = self.session.run(None, ort_inputs)
        embeddings = ort_outs[0]
        embeddings = embeddings[:, 0, :]  # 取 CLS 向量
        return embeddings


    def retrieve(self, query: str):
        query_vec = self.encode([query])
        D, I = self.index.search(query_vec, self.top_k)
        return [self.corpus[i] for i in I[0] if i < len(self.corpus)]
