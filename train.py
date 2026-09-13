from model import SVMModel

SAMPLE_DOCS = [
    ["free", "offer", "click"],
    ["win", "prize", "free"],
    ["hello", "meeting", "schedule"],
    ["project", "deadline", "update"],
    ["free", "money", "offer"],
    ["lunch", "tomorrow", "lets"],
]

SAMPLE_LABELS = [
    "spam",
    "spam",
    "ham",
    "ham",
    "spam",
    "ham",
]


def main():
    m = SVMModel()
    m.train(SAMPLE_DOCS, SAMPLE_LABELS)
    m.save("model_params.joblib")
    print("SVM model trained and saved to model_params.joblib")


if __name__ == "__main__":
    main()
