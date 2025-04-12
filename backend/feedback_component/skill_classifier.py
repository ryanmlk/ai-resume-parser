import torch.nn as nn

# Define a simple multi-label classifier
class SkillClassifier(nn.Module):
    def __init__(self, input_size, output_size):
        super(SkillClassifier, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(input_size, 512),
            nn.BatchNorm1d(512),
            nn.ReLU(),
            nn.Dropout(0.3),

            nn.Linear(512, 256),
            nn.ReLU(),
            nn.Dropout(0.2),

            nn.Linear(256, output_size),
            nn.Sigmoid()                # for multi-label output
        )
    
    def forward(self, x):
        return self.net(x)  # sigmoid for multi-label