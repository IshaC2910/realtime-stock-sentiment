from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import numpy as np

class SentimentEngine:
    def __init__(self, model_name: str):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self.pipe = pipeline("sentiment-analysis", model=self.model, tokenizer=self.tokenizer, top_k=None)

    def predict(self, texts):
        if not texts:
            return []
        outputs = self.pipe(texts, truncation=True)
        # Normalize to a signed score in [-1, 1]
        results = []
        for o in outputs:
            # o: [{'label': 'LABEL_0', 'score': 0.9}, {'label': 'LABEL_2', 'score':0.1}] or list
            if isinstance(o, list):
                scores = {d['label']: d['score'] for d in o}
                # Map labels known for cardiffnlp/twitter-roberta-base-sentiment-latest
                neg = scores.get('negative', scores.get('LABEL_0', 0.0))
                neu = scores.get('neutral', scores.get('LABEL_1', 0.0))
                pos = scores.get('positive', scores.get('LABEL_2', 0.0))
            else:
                # Fallback if pipeline returns single dict
                label = o.get('label','neutral').lower()
                pos = 1.0 if label == 'positive' else 0.0
                neg = 1.0 if label == 'negative' else 0.0
                neu = 1.0 if label == 'neutral' else 0.0
            score = pos - neg  # ignore neutral for polarity
            results.append({'neg': float(neg), 'neu': float(neu), 'pos': float(pos), 'score': float(score)})
        return results
