from transformers import AutoTokenizer, AutoModelForMaskedLM
from torch import nn
from transformers import RobertaConfig
from transformers import TrainingArguments, Trainer
from mistral_datasets import *

if __name__ == '__main__':
    model = AutoModelForMaskedLM.from_config(RobertaConfig())
    model.cuda()
    print(model)
    # Create dataset
    train_dataset = MistralMLMDataset(AutoTokenizer.from_pretrained("distilbert/distilbert-base-uncased"))
    val_dataset = MistralMLMDataset(AutoTokenizer.from_pretrained("distilbert/distilbert-base-uncased"), split = 'validation')

    data_collator = DataCollatorForLanguageModeling(tokenizer = train_dataset.tokenizer, mlm_probability = 0.1)
    # DataLoader for batching and shuffling
    mlm_train = train_dataset.prepare_corpus()
    mlm_val = val_dataset.prepare_corpus()
    
    training_args = TrainingArguments(
        output_dir = "runs",
        eval_strategy = "epoch",
        learning_rate=1e-5,
        num_train_epochs=3,
        weight_decay=0.01,
        report_to='tensorboard'
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=mlm_train,
        eval_dataset=mlm_val,
        data_collator=data_collator
    )
    trainer.train()
