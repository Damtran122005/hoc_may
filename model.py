"""SVM-based classifier wrapper.

This file replaces the previous Naive Bayes implementation with a lightweight
SVM wrapper using scikit-learn. The API preserves `train`, `predict`,
`save`, and `load` methods so `app.py` can remain largely unchanged.
"""

from typing import List, Tuple, Dict
import numpy as np
from sklearn.svm import SVC
import joblib


class SVMModel:
    def __init__(self):
        self.model: SVC | None = None
        self.vocab: Dict[str, int] = {}

    def _build_vocab(self, docs: List[List[str]]):
        idx = 0
        for doc in docs:
            for w in doc:
                if w not in self.vocab:
                    self.vocab[w] = idx
                    idx += 1

    def _docs_to_matrix(self, docs: List[List[str]]) -> np.ndarray:
        X = np.zeros((len(docs), max(len(self.vocab), 1)), dtype=float)
        for i, doc in enumerate(docs):
            for w in doc:
                j = self.vocab.get(w)
                if j is not None:
                    X[i, j] += 1.0
        return X

    def train(self, docs: List[List[str]], labels: List[str]):
        if not docs:
            raise ValueError("No training documents provided")
        self.vocab = {}
        self._build_vocab(docs)
        X = self._docs_to_matrix(docs)
        y = np.array(labels)
        clf = SVC(probability=True, kernel="linear")
        clf.fit(X, y)
        self.model = clf

    def predict(self, features: List[str]) -> Tuple[str, float]:
        if self.model is None:
            raise RuntimeError("Model is not trained or loaded")
        X = np.zeros((1, max(len(self.vocab), 1)), dtype=float)
        for w in features:
            j = self.vocab.get(w)
            if j is not None:
                X[0, j] += 1.0
        probs = self.model.predict_proba(X)[0]
        classes = list(self.model.classes_)
        best_idx = int(np.argmax(probs))
        return classes[best_idx], float(probs[best_idx])

    def save(self, path: str):
        payload = {"model": self.model, "vocab": self.vocab}
        joblib.dump(payload, path)

    @classmethod
    def load(cls, path: str):
        payload = joblib.load(path)
        m = cls()
        m.model = payload.get("model")
        m.vocab = payload.get("vocab", {})
        return m
