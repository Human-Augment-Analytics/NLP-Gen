from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, Seq2SeqTrainer, Seq2SeqTrainingArguments

from datasets import Dataset, load_metric

import pandas as pd

import torch

path_to_csv = "parsed_documents.csv"

df = pd.read_csv(path_to_csv, sep="|").dropna()

dataset = Dataset.from_pandas(df).train_test_split(test_size=0.2)

model_name = 'google/long-t5-tglobal-base'

max_input_length = 4096
max_target_length = 500
batch_size = 1

tokenizer = AutoTokenizer.from_pretrained(model_name)

def process_data_to_model_inputs(batch):
    inputs = [doc for doc in batch["Document"]]
    model_inputs = tokenizer(inputs, max_length=max_input_length, truncation=True)

    # Setup the tokenizer for targets
    with tokenizer.as_target_tokenizer():
        labels = tokenizer(batch["Summary"], max_length=max_target_length, truncation=True)

    model_inputs["labels"] = labels["input_ids"]
    return model_inputs

rouge = load_metric("rouge", trust_remote_code=True)

train_dataset = dataset["train"]
val_dataset = dataset["test"]
summary_generation = dataset["test"]
train_dataset = train_dataset.map(
    process_data_to_model_inputs,
    batched=True,
    batch_size=batch_size,
    remove_columns=["Document", "Summary"],
)

train_dataset.set_format(
    type="torch",
)

val_dataset = val_dataset.map(
    process_data_to_model_inputs,
    batched=True,
    batch_size=batch_size,
    remove_columns=["Document", "Summary"],
)

val_dataset.set_format(
    type="torch",
)

model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

step_report = 10

training_args = Seq2SeqTrainingArguments(
    evaluation_strategy="steps",
    per_device_train_batch_size=batch_size,
    per_device_eval_batch_size=batch_size,
    output_dir="./longt5-model",
    logging_steps=step_report,
    eval_steps=step_report,
    save_steps=step_report,
    num_train_epochs=1,
    weight_decay=0.01,
    learning_rate=2e-5,
)

trainer = Seq2SeqTrainer(
    model=model,
    tokenizer=tokenizer,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
)

trainer.train()
model.eval()
if torch.backends.mps.is_available():
    device = "mps"
elif torch.cuda.is_available():
    device = "cuda"
else:
    device = "cpu"

model = model.to(device)

import pandas as pd
import matplotlib.pyplot as plt

df = pd.DataFrame(trainer.state.log_history)
train_loss = df["loss"].dropna().values
val_loss = df["eval_loss"].dropna().values

iterations = [step_report*i for i in range(len(train_loss))]

plt.plot(iterations, train_loss, label="Train Loss")
plt.plot(iterations, val_loss, label="Validation Loss")
plt.title("Loss Curves")
plt.xlabel("Training Steps")
plt.ylabel("Loss")
plt.savefig("loss_curve.png", bbox_inches="tight")

def generate_answer(batch):
  inputs_dict = tokenizer(batch["Document"], padding="max_length", max_length=max_input_length, return_tensors="pt", truncation=True)
  input_ids = inputs_dict.input_ids.to(device)
  attention_mask = inputs_dict.attention_mask.to(device)

  predicted_abstract_ids = model.generate(input_ids, attention_mask=attention_mask)
  batch["predicted_summary"] = tokenizer.batch_decode(predicted_abstract_ids, skip_special_tokens=True)
  return batch

result = summary_generation.map(generate_answer, batched=True, batch_size=1)
print(rouge.compute(predictions=result["predicted_summary"], references=result["Summary"], rouge_types=["rouge2"])["rouge2"].mid)