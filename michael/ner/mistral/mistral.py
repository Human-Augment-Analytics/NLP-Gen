from transformers import LongformerForTokenClassification, LongformerModel, AutoTokenizer, AutoModelForTokenClassification, BertTokenizer, BertModel
from torch import nn
from transformers import MistralConfig, MistralModel
import torch

#bidirectional mistral class
class LongformerHeads(nn.Module):
    def __init__(self, num_issues, sequence_length=4096):
        super(LongformerHeads, self).__init__()
        #self.mistral = MistralModel(MistralConfig(num_hidden_layers = num_blocks, hidden_size = hidden_size))
        #print('Decoder built: ', self.mistral)
        #self.classifier = nn.Linear(hidden_size, num_entities)
        self.backbone = LongformerModel.from_pretrained("allenai/longformer-base-4096")#BertModel.from_pretrained("bert-base-cased")
        self.issue_classifier = nn.Linear(768, num_issues)
        #self.court_ner = nn.Linear(768, sequence_length * 2)#reshape this output to (sequence_length, 2)

    def forward(self, input_ids, attention_mask, labels = None):
        print(input_ids, input_ids.shape)
        x = self.backbone(input_ids[:, :4096], attention_mask)
        logits = self.issue_classifier(x)
        if labels is not None:
            loss = torch.nn.cross_entropy(logits, labels)
            return (loss, logits)
        return logits


if __name__ == '__main__':
    #model = LongformerModel.from_pretrained("allenai/longformer-base-4096")
    model = LongformerForTokenClassification.from_pretrained("brad1141/Longformer-finetuned-norm")
    print(model)
