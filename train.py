from model import NaiveBayesModel

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
    m = NaiveBayesModel()
    m.train(SAMPLE_DOCS, SAMPLE_LABELS)
    m.save("model_params.json")
    print("Model trained and saved to model_params.json")


if __name__ == "__main__":
    main()
