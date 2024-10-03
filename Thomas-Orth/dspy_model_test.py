import dspy

import pandas as pd
from dspy.datasets.dataset import Dataset

from datasets import load_metric

class CSVDataset(Dataset):
    def __init__(self, file_path, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        
        df = pd.read_csv(file_path, sep="|").dropna().rename(columns={"Document": "document", "Summary": "summary"})

        train_set = df.sample(frac = 0.8)

        self._train = train_set.to_dict(orient='records')

        self._dev = df.drop(train_set.index).to_dict(orient='records')

class Summarizer(dspy.Module):
  def __init__(self):
    self.summarize = dspy.ChainOfThought("document -> summary")

  def forward(self, document):
    return self.summarize(document=document)

dataset = CSVDataset("parsed_documents.csv")
train = [x.with_inputs('document') for x in dataset.train]
dev = [x.with_inputs('document') for x in dataset.dev]
lm = dspy.OllamaLocal(model='phi3:medium')
dspy.settings.configure(lm=lm)

def summarizer_metric(example, pred, trace=None):
    rouge = load_metric("rouge", trust_remote_code=True)
    return rouge.compute(predictions=[example.summary], references = [pred.summary], rouge_types=["rouge2"])["rouge2"].mid.fmeasure

from dspy.evaluate import Evaluate

evaluate = Evaluate(devset=dev[:], metric=summarizer_metric, num_threads=4, display_progress=True, display_table=27)

from dspy.teleprompt import BootstrapFewShotWithRandomSearch

teleprompter = BootstrapFewShotWithRandomSearch(
    metric=summarizer_metric, 
    max_labeled_demos=8,
    max_bootstrapped_demos=8,
    num_candidate_programs=1,
)

cot_compiled = teleprompter.compile(Summarizer(), trainset=train, valset=dev)
print(evaluate(cot_compiled, devset=dev[:]))