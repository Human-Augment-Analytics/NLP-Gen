from transformers import AutoTokenizer, AutoModelForMaskedLM
from torch import nn
from transformers import RobertaConfig
from transformers import TrainingArguments, Trainer, DataCollatorWithPadding
from mistral_datasets import *
from mistral import *
#import evaluate

#accuracy = evaluate.load("accuracy")

#def compute_metrics(eval_pred):
#    logits, labels = eval_pred
#    predictions = np.argmax(logits, axis = -1)
#
#    return accuracy.compute(predictions = predictions, references = labels)

if __name__ == '__main__':
    model = LongformerHeads(num_issues = 26)
    model.cuda()
    print(model)
    # Create dataset
    train_dataset = DocumentClassificationDataset(AutoTokenizer.from_pretrained("allenai/longformer-base-4096"), cases_path = './train_cases.pkl')
    val_dataset = DocumentClassificationDataset(AutoTokenizer.from_pretrained("allenai/longformer-base-4096"), cases_path = './val_cases.pkl')
    #train_dataset = DocumentClassificationDataset(AutoTokenizer.from_pretrained("bert-base-cased"), cases_path = './train_cases.pkl')
    #val_dataset = DocumentClassificationDataset(AutoTokenizer.from_pretrained("bert-base-cased"), cases_path = './val_cases.pkl')


    data_collator = DataCollatorWithPadding(tokenizer = train_dataset.tokenizer)
    # DataLoader for batching and shuffling
    train_ds = train_dataset.prepare_corpus()
    val_ds = val_dataset.prepare_corpus()
    
    training_args = TrainingArguments(
        per_device_train_batch_size = 1,
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
        train_dataset=train_ds,
        eval_dataset=val_ds,
        data_collator=data_collator,
        compute_metrics=compute_metrics
    )
    trainer.train()
