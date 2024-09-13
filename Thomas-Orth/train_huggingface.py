from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, Seq2SeqTrainer, Seq2SeqTrainingArguments

from datasets import Dataset, load_metric

import pandas as pd

import torch

path_to_csv = "parsed_documents.csv"

df = pd.read_csv(path_to_csv, sep="|").dropna()

dataset = Dataset.from_pandas(df).train_test_split(test_size=0.2)

max_input_length = 7168 # it is calculated
#max_input_length = 16384
max_output_length = 512
batch_size = 1

tokenizer = AutoTokenizer.from_pretrained("allenai/led-base-16384")

def process_data_to_model_inputs(batch):
    # tokenize the inputs and labels
    inputs = tokenizer(
        batch["Document"],
        padding='max_length',
        truncation=True,
        max_length=max_input_length,
    )
    outputs = tokenizer(
        batch["Summary"],
        padding="max_length",
        truncation=True,
        max_length=max_output_length,
    )

    batch["input_ids"] = inputs.input_ids
    batch["attention_mask"] = inputs.attention_mask

    # create 0 global_attention_mask lists
    batch["global_attention_mask"] = len(batch["input_ids"]) * [
        [0 for _ in range(len(batch["input_ids"][0]))]
    ]

    # since above lists are references, the following line changes the 0 index for all samples
    batch["global_attention_mask"][0][0] = 1
    batch["labels"] = outputs.input_ids

    # We have to make sure that the PAD token is ignored
    batch["labels"] = [
        [-100 if token == tokenizer.pad_token_id else token for token in labels]
        for labels in batch["labels"]
    ]

    return batch

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
    columns=["input_ids", "attention_mask", "global_attention_mask", "labels"],
)

val_dataset = val_dataset.map(
    process_data_to_model_inputs,
    batched=True,
    batch_size=batch_size,
    remove_columns=["Document", "Summary"],
)

val_dataset.set_format(
    type="torch",
    columns=["input_ids", "attention_mask", "global_attention_mask", "labels"],
)

led = AutoModelForSeq2SeqLM.from_pretrained("allenai/led-base-16384", gradient_checkpointing=True, use_cache=False)

# set generate hyperparameters
led.config.num_beams = 2
led.config.max_length = 512
led.config.min_length = 100
led.config.length_penalty = 2.0
led.config.early_stopping = True
led.config.no_repeat_ngram_size = 3

from transformers.generation import GenerationConfig

gen_cfg = GenerationConfig.from_model_config(led.config)

step_report = 10

training_args = Seq2SeqTrainingArguments(
    evaluation_strategy="steps",
    per_device_train_batch_size=batch_size,
    per_device_eval_batch_size=batch_size,
    output_dir="./led-model",
    logging_steps=step_report,
    eval_steps=step_report,
    save_steps=step_report,
    gradient_accumulation_steps=4,
    num_train_epochs=3,
)

trainer = Seq2SeqTrainer(
    model=led,
    tokenizer=tokenizer,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
)

trainer.train()
led.eval()
if torch.backends.mps.is_available():
    device = "mps"
elif torch.cuda.is_available():
    device = "cuda"
else:
    device = "cpu"

led = led.to(device)

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

  global_attention_mask = torch.zeros_like(attention_mask).to(device)
  # put global attention on <s> token
  global_attention_mask[:, 0] = 1

  predicted_abstract_ids = led.generate(input_ids, attention_mask=attention_mask, global_attention_mask=global_attention_mask, generation_config=gen_cfg)
  batch["predicted_summary"] = tokenizer.batch_decode(predicted_abstract_ids, skip_special_tokens=True)
  return batch

result = summary_generation.map(generate_answer, batched=True, batch_size=1)
print(rouge.compute(predictions=result["predicted_summary"], references=result["Summary"], rouge_types=["rouge2"])["rouge2"].mid)
