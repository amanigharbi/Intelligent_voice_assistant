
  # import torch
# import torch.nn as nn

# # feed forwad _neural network
# class NeuralNet(nn.Module):
#     def __init__(self, input_size, hidden_size, num_classes):
#         super(NeuralNet, self).__init__()
#         self.l1 = nn.Linear(input_size, hidden_size) 
#         self.l2 = nn.Linear(hidden_size, hidden_size) 
#         self.l3 = nn.Linear(hidden_size, num_classes)
#         self.relu = nn.ReLU()
    
#     def forward(self, x):
#         out = self.l1(x)
#         out = self.relu(out)
#         out = self.l2(out)
#         out = self.relu(out)
#         out = self.l3(out)
#         # no activation and no softmax at the end
#         return out
import torch
import torch.nn as nn

# class NeuralNet(nn.Module):
#     def __init__(self, input_size, hidden_size, output_size):
#         super(NeuralNet, self).__init__()
#         self.linear1 = nn.Linear(input_size, hidden_size)
#         self.linear2 = nn.Linear(hidden_size, hidden_size)
#         self.linear3 = nn.Linear(hidden_size, output_size)
#         self.relu = nn.ReLU()

#     def forward(self, x):
#         x = self.relu(self.linear1(x))
#         x = self.relu(self.linear2(x))
#         output = self.linear3(x)
        
#         return output
class NeuralNet(nn.Module):
     #Ce sera un réseau de neurones feed-forward 
    def __init__(self, input_size, hidden_size, output_size):
        super(NeuralNet, self).__init__()
        nn.Dropout(),
       #création de la première couche linéaire. Cela obtient la taille d'entrée, 
       # puis la couche cachée connectée
        self.linearlayer1 = nn.Linear(input_size, hidden_size)
        #appliquer la normalisation par lots(batch normalization)
        self.bn1= nn.BatchNorm1d(hidden_size)
        # création de la 2eme couche linéaire
        self.linearlayer2 = nn.Linear(hidden_size, hidden_size)
        #appliquer la normalisation par lots(batch normalization)
        self.bn2= nn.BatchNorm1d(hidden_size) 
        # création de la 3 eme couche linéaire
        self.linearlayer3 = nn.Linear(hidden_size, output_size)
        #en utilisant la fonction d'activation relu
        self.relu = nn.ReLU()
    #i#implémenter la passe avant(forward pass)
    def forward(self, x):
      #appliquez notre première couche linéaire qui 
      # reçoit x en entrée et donne ensuite la sortie
        output = self.linearlayer1(x)
       #fonction d'activation
        output = self.relu(output)
        output = self.linearlayer2(output)
        #fonction d'activation
        output = self.relu(output)
        output = self.linearlayer3(output)
        return output

    
    
# class LeNet5(nn.Module):

#     def __init__(self):
#         super(LeNet5, self).__init__()
        
#         self.convolutional_layer = nn.Sequential(            
#             nn.Conv2d(in_channels=1, out_channels=6, kernel_size=5, stride=1),
#             nn.ReLU(),
#             nn.MaxPool2d(kernel_size=2, stride=2, padding=0),
#             nn.Conv2d(in_channels=6, out_channels=16, kernel_size=5, stride=1),
#             nn.ReLU(),
#             nn.MaxPool2d(kernel_size=2, stride=2, padding=0),
#             nn.Conv2d(in_channels=16, out_channels=327, kernel_size=5, stride=1),
#             nn.ReLU()
#         )

#         self.linear_layer = nn.Sequential(
#             nn.Dropout(),
#             nn.Linear(in_features=327, out_features=8),
#             nn.ReLU(),
#             nn.Linear(in_features=8, out_features=80),
#         )


#     def forward(self, x):
#         x = self.convolutional_layer(x)
#         x = torch.flatten(x, 1)
#         x = self.linear_layer(x)
#         x = F.softmax(x, dim=1)
#         return x

#         x = self.convolutional(x)
#         x = self.avgpool(x)
#         x = torch.flatten(x, 1)
#         x = self.linear(x)
#         return torch.softmax(x, 1)
