# 写一个seq2seq代码，实现中英互译，用pytorch架构


import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import random

# 设定随机种子以便复现结果
random.seed(123)
torch.manual_seed(123)


# 定义编码器（Encoder）模型
class Encoder(nn.Module):
    def __init__(self, input_size, hidden_size):
        super(Encoder, self).__init__()
        self.hidden_size = hidden_size
        self.embedding = nn.Embedding(input_size, hidden_size)
        self.lstm = nn.LSTM(hidden_size, hidden_size, bidirectional=True)

    def forward(self, input, hidden):
        embedded = self.embedding(input).view(1, 1, -1)
        output, hidden = self.lstm(embedded, hidden)
        return output, hidden

    def init_hidden(self):
        return (torch.zeros(2, 1, self.hidden_size), torch.zeros(2, 1, self.hidden_size))  # 双向LSTM的隐状态


# 定义解码器（Decoder）模型
class Decoder(nn.Module):
    def __init__(self, hidden_size, output_size):
        super(Decoder, self).__init__()
        self.hidden_size = hidden_size
        self.embedding = nn.Embedding(output_size, hidden_size)
        self.lstm = nn.LSTM(hidden_size, hidden_size)
        self.out = nn.Linear(hidden_size, output_size)
        self.softmax = nn.LogSoftmax(dim=1)

    def forward(self, input, hidden):
        output = self.embedding(input).view(1, 1, -1)
        output = F.relu(output)
        output, hidden = self.lstm(output, hidden)
        output = self.softmax(self.out(output[0]))
        return output, hidden


# 定义训练函数
def train(input_tensor, target_tensor, encoder, decoder, encoder_optimizer, decoder_optimizer, criterion,
          max_length=100):
    encoder_hidden = encoder.init_hidden()

    encoder_optimizer.zero_grad()
    decoder_optimizer.zero_grad()

    input_length = input_tensor.size(0)
    target_length = target_tensor.size(0)

    loss = 0

    encoder_outputs = torch.zeros(max_length, encoder.hidden_size * 2)

    for ei in range(input_length):
        encoder_output, encoder_hidden = encoder(
            input_tensor[ei], encoder_hidden)
        encoder_outputs[ei] = encoder_output[0, 0]

    decoder_input = torch.tensor([[SOS_token]])

    decoder_hidden = encoder_hidden

    for di in range(target_length):
        decoder_output, decoder_hidden = decoder(
            decoder_input, decoder_hidden)
        topv, topi = decoder_output.topk(1)
        decoder_input = topi.squeeze().detach()

        loss += criterion(decoder_output, target_tensor[di])
        if decoder_input.item() == EOS_token:
            break

    loss.backward()

    encoder_optimizer.step()
    decoder_optimizer.step()

    return loss.item() / target_length


# 定义训练参数
hidden_size = 256
learning_rate = 0.01
MAX_LENGTH = 10
SOS_token = 0
EOS_token = 1

# 定义训练数据
input_tensor = torch.tensor([[1, 2, 3, 4, 5]])
target_tensor = torch.tensor([[6, 7, 8, 9, 10]])

# 初始化编码器和解码器
encoder = Encoder(input_tensor.size(1), hidden_size)
decoder = Decoder(hidden_size, target_tensor.size(1))

# 定义优化器和损失函数
encoder_optimizer = optim.SGD(encoder.parameters(), lr=learning_rate)
decoder_optimizer = optim.SGD(decoder.parameters(), lr=learning_rate)
criterion = nn.NLLLoss()

# 开始训练
for epoch in range(100):
    loss = train(input_tensor, target_tensor, encoder, decoder, encoder_optimizer, decoder_optimizer, criterion)
    print('Epoch:', epoch, 'Loss:', loss)
