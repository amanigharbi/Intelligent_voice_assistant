import torch.optim as optim
from tqdm import tqdm
import json 
import numpy as np
from nltk_utils import tokenize, stem, bag_of_words
import torch
from torch.utils.data import Dataset, DataLoader
from model import NeuralNet
from tqdm import tqdm
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from torchvision import datasets, transforms
import numpy as np
import matplotlib.pyplot as plt
from torch.utils.data.sampler import SubsetRandomSampler
from torch.utils.data.dataset import random_split

# file json
with open('intents_chat.json', encoding='utf-8') as f:
    intents = json.load(f)
# def tokenize(sentence):
#     """
#     diviser la phrase en tableau de mots / jetons
#     un jeton peut être un mot ou un caractère de ponctuation, ou un nombre
#     """
#     return tk.tokenize(sentence)

# def stem(word):
#     """
#     stemming = trouver la racine du mot    examples:
#     words = ["organize", "organizes", "organizing"]
#     words = [stem(w) for w in words]
#     -> ["organ", "organ", "organ"]
#     """
#     return stemmer.stem(word.lower())
all_words = []
tags = []
xy = []

for intent in intents['intents']:
    tag = intent['tag']
    tags.append(tag)
    for pattern in intent['patterns']:
        w = tokenize(pattern)
        all_words.extend(w)
        xy.append((w, tag))

ignore_words = ['?', '!', '.', ',']
all_words = [stem(w) for w in all_words if w not in ignore_words]
all_words = sorted(set(all_words))
tags = sorted(set(tags))


# bag of words

# def bag_of_words(tokenized_sentence, words):
#     """
#     return bag of words array:
#     1 for each known word that exists in the sentence, 0 otherwise
#     example:
#     sentence = ["hello", "how", "are", "you"]
#     words = ["hi", "hello", "I", "you", "bye", "thank", "cool"]
#     bog   = [  0 ,    1 ,    0 ,   1 ,    0 ,    0 ,      0]
#     """
#     # stem each word
#     sentence_words = [stem(word) for word in tokenized_sentence]
#     # initialize bag with 0 for each word
#     bag = np.zeros(len(words), dtype=np.float32)
#     for idx, w in enumerate(words):
#         if w in sentence_words: 
#             bag[idx] = 1

#     return bag

X_train = []
y_train = []
for (pattern_sentence, tag) in xy:
    bag = bag_of_words(pattern_sentence, all_words)
    X_train.append(bag)

    label = tags.index(tag)
    y_train.append(label) 

X_train = np.array(X_train)
y_train = np.array(y_train)

class ChatDataset(Dataset):
    def __init__(self):
        self.n_samples = len(X_train)
        self.x_data = X_train
        self.y_data = y_train

    #dataset[idx]
    def __getitem__(self, index):
        return self.x_data[index], self.y_data[index]

    def __len__(self):
        return self.n_samples


# Hyerparameters
BATCH_SIZE = 8
INPUT_SIZE = len(X_train[0])
HIDDEN_SIZE = 8
OUTPUT_SIZE = len(tags)
LEARNING_RATE = 1e-3
EPOCHS = 100
WORKERS = 2

dataset = ChatDataset()
# print("dataset size", len(dataset))
len_ = len(dataset)
train_dataset, valid_dataset = random_split(dataset, [round(len_*0.75), round(len_*0.25)])

                                               
train_loader = DataLoader(dataset=train_dataset, batch_size=BATCH_SIZE, shuffle=True, num_workers=WORKERS)

test_loader = DataLoader(dataset=valid_dataset,
                          batch_size=BATCH_SIZE,
                          shuffle=False,
                          num_workers=WORKERS,
                        )

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
# model = NeuralNet(input_size=INPUT_SIZE, hidden_size=HIDDEN_SIZE, output_size=OUTPUT_SIZE).to(device)
# dataset = ChatDataset()
loader = DataLoader(dataset=dataset,
                          batch_size=BATCH_SIZE,
                          shuffle=True,
                          num_workers=0)
#suppose if Gpu is available, we can puish our model to the device. otherwise we can have in cpu itself
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = NeuralNet(input_size=INPUT_SIZE, hidden_size=HIDDEN_SIZE, output_size=OUTPUT_SIZE).to(device)
# Loss is CrossEntropyLoss and optimizer is Adam
loss_fn=nn.CrossEntropyLoss()

criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)
# optimizer=optim.SGD(model.parameters(),lr=0.001,momentum=0.9)
total=0
correct=0
train_losses=[]
train_accu=[]
# Train the model
for epoch in range(EPOCHS):
    for (words, labels) in loader:
        words = words.to(device)
        labels = labels.to(dtype=torch.long).to(device)
        
        # Forward pass
        outputs = model(words)
        # if y would be one-hot, we must apply
        # labels = torch.max(labels, 1)[1]
        loss = criterion(outputs, labels)
        # Backward and optimize
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        scores = model(words)
        _, pred = scores.max(1)
        total += len(words)
        correct += (pred==labels).sum()
        train_accu.append((correct/total)*100)
        train_losses.append(loss.item())
    if (epoch+1) % 1 == 0:
        print (f'Epoch [{epoch+1}/{EPOCHS}], Loss: {loss.item():.4f} And Got {correct} / {total} with accuracy {float(correct)/float(total)*100:.2f}')
print(f'final Accuracy-----> Got {correct} / {total} with accuracy {float(correct)/float(total)*100:.2f}') 
print(f'final loss: {loss.item():.4f}')
# loss y optimizador
# criterion = torch.nn.CrossEntropyLoss()
# optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)

# for epoch in range(EPOCHS):
#     for (words, labels) in train_loader:
#         words = words.to(device)
#         labels = labels.to(dtype=torch.long).to(device)

#         # forward
#         outputs = model(words)
#         loss = criterion(outputs, labels)

#         # backprop y update
#         optimizer.zero_grad()
#         loss.backward()
#         optimizer.step()
    
#     if (epoch + 1) % 100 == 0:
#         print(f'epoch {epoch + 1}/{EPOCHS}, loss={loss.item():.4f}')

# print(f'final loss={loss.item():.4f}')

data = {
    "model_state": model.state_dict(),
    "input_size": INPUT_SIZE,
    "output_size": OUTPUT_SIZE,
    "hidden_size": HIDDEN_SIZE,
    "all_words": all_words,
    "tags": tags
}

FILE = "data.pth"
torch.save(data, FILE)

print("save data "+ FILE)
# # Train and Test functions



# def check_accuracyTest(loader, model):
#     running_loss=0
#     num_correct = 0
#     num_samples = 0
#     model.eval()

#     with torch.no_grad():
#         for words, labels in loader:
#             words = words.to(device=device)
#             labels = labels.to(device=device)
#             labels = labels.to(dtype=torch.long).to(device)

#             scores = model(words)
# #             loss
#             loss=criterion(scores,labels)
#             running_loss+=loss.item()
# #             acc
#             _, predictions = scores.max(1)
#             num_correct += (predictions == labels).sum()
#             num_samples += predictions.size(0)

# #     model.train()
#     train_accu.append((num_correct/num_samples)*100)
#     train_losses.append(running_loss/len(loader))
#     return num_correct/num_samples,running_loss/len(loader)
# # acc_train, loss_train =check_accuracy(train_loader, model)
# acc_test, loss_test =check_accuracyTest(test_loader, model)


# print('Accuracy on training set: %.3f | loss on training set: %.3f'%(acc_train*100,loss_train))
# print('Accuracy on test set: %.3f | loss on test set: %.3f'%(acc_test*100,loss_test))
# # # #plot accuracy

# plt.plot(train_accu,'-*')
# plt.plot(train_accu,'-o')
# plt.xlabel('epoch')
# plt.ylabel('accuracy')
# plt.legend(['Acc'])
# plt.title('Accuracy')

# plt.show()
# #plot losses

# plt.plot(train_losses,'-*')
# plt.plot(eval_losses,'-o')
# plt.xlabel('epoch')
# plt.ylabel('losses')
# plt.legend(['loss'])
# plt.title('Losses')

# plt.show()




train_losses=[]
train_accu=[]
def train(epoch):
    print('\nEpoch : %d'%epoch)
    model.train()
    running_loss=0
    correct=0
    total=0

    for words, labels in train_loader:
        words = words.to(device=device)
        labels = labels.to(device=device)
        labels = labels.to(dtype=torch.long).to(device)
        outputs=model(words)
    
        loss=loss_fn(outputs,labels)
    
    #Replaces pow(2.0) with abs() for L1 regularization
    
        l2_lambda = 0.001
        l2_norm = sum(p.pow(2.0).sum()
                  for p in model.parameters())

        loss = loss + l2_lambda * l2_norm
    
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        running_loss += loss.item()
        _, predicted = outputs.max(1)
        total += labels.size(0)
        correct += predicted.eq(labels).sum().item()
    train_loss=running_loss/len(train_loader)
    accu=100.*correct/total
    train_accu.append(accu)
    train_losses.append(train_loss)
    print('Train Loss: %.3f | Accuracy: %.3f'%(train_loss,accu))
    
    
    
    
eval_losses=[]
eval_accu=[]
def test(epoch):
    model.eval()

    running_loss=0
    correct=0
    total=0
    with torch.no_grad():
        for words, labels in test_loader:
            words = words.to(device=device)
            labels = labels.to(device=device)
            labels = labels.to(dtype=torch.long).to(device)
            outputs=model(words)

            loss= loss_fn(outputs,labels)
            optimizer.step()
            running_loss+=loss.item()
      
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()
  
    test_loss=running_loss/len(test_loader)
    accu=100.*correct/total

    eval_losses.append(test_loss)
    eval_accu.append(accu)

    print('Test Loss: %.3f | Accuracy: %.3f'%(test_loss,accu)) 
if __name__ == '__main__':
    
    
    epochs=200
    for epoch1 in range(1,epochs+10): 
        
        train(epoch1)
        test(epoch1)
        
    
    plt.plot(train_accu,'-o')
    plt.plot(eval_accu,'-o')
    plt.xlabel('epoch')
    plt.ylabel('accuracy')
    plt.legend(['Train','Valid'])
    plt.title('Train vs Valid Accuracy')

    plt.show()
    
    
    #plot losses

    plt.plot(train_losses,'-o')
    plt.plot(eval_losses,'-o')
    plt.xlabel('epoch')
    plt.ylabel('losses')
    plt.legend(['Train','Valid'])
    plt.title('Train vs Valid Losses')

    plt.show()
