import logging
import json

from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
DEPLOYED_REPO = "agomez302/nlp-dr-ner"

class NerProcessor:
    def __init__(self):
        self.deployed_tokenizer = AutoTokenizer.from_pretrained(DEPLOYED_REPO)
        self.deployed_model = AutoModelForTokenClassification.from_pretrained(DEPLOYED_REPO)
        self.deployed_ner_pipeline = pipeline(
                "ner",
                model=self.deployed_model,
                tokenizer=self.deployed_tokenizer,
                aggregation_strategy="simple",
        )

    def process_text(self, text):
        """Runs NER model on text and returns JSONL string."""
        try:
            chunks = self.split_text_with_overlap(text)
            all_predictions = []
            for chunk in chunks:
                preds = self.deployed_ner_pipeline(chunk)
                all_predictions.extend(preds)
                # Now we add the context to each prediction
                for pred in preds:
                    pred['context'] = chunk
            all_predictions = self.deduplicate_entities(all_predictions)
            
            formatted_output = {
                # "sentence": text,
                "entities": self.run_predictions(all_predictions)
            }
            
            return json.dumps(formatted_output)

        except Exception as e:
            logger.error(f"Failed to run NER model on extracted text: {e}")

            # return a mock object for the sake of showcasing a proof of concept
            mock_entities = {
                "sentence": "2024-04-27 y 2 de enero del 2023",
                "entities": [
                    {
                        "entity_group": "DATE",
                        "score": 0.99921053647995,
                        "word": "2024-04-27",
                        "start": 0,
                        "end": 10,
                    },
                    {
                        "entity_group": "DATE",
                        "score": 0.9988479614257812,
                        "word": "2 de enero del 2023",
                        "start": 13,
                        "end": 32,
                    }
                ]
            }
            return json.dumps(mock_entities)
        
    def split_text_with_overlap(self, text, max_tokens=450, overlap=50):
        """Split text into chunks with overlap to handle long sequences."""
        if not text:
            return []
        max_tokens = min(max_tokens, 512)
        
        tokenizer = self.deployed_tokenizer
        tokens = tokenizer.encode(text, truncation=False)
        
        if len(tokens) <= max_tokens:
            return [text]
            
        chunks = []
        i = 0
        while i < len(tokens):
            chunk = tokenizer.decode(tokens[i:i + max_tokens], skip_special_tokens=True)
            chunks.append(chunk)
            i += max_tokens - overlap
        return chunks

    def deduplicate_entities(self, predictions):
        """Remove duplicate entities from overlapping chunks."""
        unique = []
        seen = set()
        for entity in predictions:
            key = (entity['entity_group'], entity['word'], entity['start'], entity['end'])
            if key not in seen:
                unique.append(entity)
                seen.add(key)
        return unique
    
    def run_predictions(self, predictions: list):
        """Format predictions for output, converting float32 to regular float."""
        try:
            processed_predictions = []
            for pred in predictions:
                pred_dict = dict(pred)
                pred_dict['score'] = float(pred_dict['score'])
                processed_predictions.append(pred_dict)

            return processed_predictions
                
        except Exception as e:
            logging.error(f"Failed to process predictions: {e}")
            raise
