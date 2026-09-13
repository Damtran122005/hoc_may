import json
import math
from collections import defaultdict, Counter
from typing import List, Tuple


class NaiveBayesModel:
    def __init__(self):
        self.class_priors = {}  # P(class)
        self.likelihoods = {}  # P(word|class)
        self.vocab = set()

    def train(self, docs: List[List[str]], labels: List[str], alpha: float = 1.0):
        counts = defaultdict(Counter)
        class_counts = Counter()

        for doc, label in zip(docs, labels):
            class_counts[label] += 1
            for word in doc:
                counts[label][word] += 1
                self.vocab.add(word)

        total_docs = sum(class_counts.values())
        self.class_priors = {c: class_counts[c] / total_docs for c in class_counts}

        # compute likelihoods with Laplace smoothing
        self.likelihoods = {}
        V = len(self.vocab)
        for c in counts:
            total_words = sum(counts[c].values())
            self.likelihoods[c] = {}
            for word in self.vocab:
                self.likelihoods[c][word] = (counts[c][word] + alpha) / (total_words + alpha * V)

    def predict(self, features: List[str]) -> Tuple[str, float]:
        # compute log probabilities
        log_probs = {}
        for c in self.class_priors:
            log_prob = math.log(self.class_priors[c]) if self.class_priors[c] > 0 else float("-inf")
            for word in features:
                if word in self.vocab:
                    log_prob += math.log(self.likelihoods[c].get(word, 1e-12))
                else:
                    # unseen words contribute a small uniform probability
                    log_prob += math.log(1e-12)
            log_probs[c] = log_prob

        # convert log probs to normalized probabilities
        max_log = max(log_probs.values())
        exps = {c: math.exp(log_probs[c] - max_log) for c in log_probs}
        total = sum(exps.values())
        probs = {c: exps[c] / total for c in exps}
        best = max(probs, key=probs.get)
        return best, probs[best]

    def save(self, path: str):
        payload = {
            "class_priors": self.class_priors,
            "likelihoods": self.likelihoods,
            "vocab": list(self.vocab),
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False)

    @classmethod
    def load(cls, path: str):
        m = cls()
        with open(path, "r", encoding="utf-8") as f:
            payload = json.load(f)
        m.class_priors = {k: float(v) for k, v in payload.get("class_priors", {}).items()}
        m.likelihoods = payload.get("likelihoods", {})
        m.vocab = set(payload.get("vocab", []))
        return m
