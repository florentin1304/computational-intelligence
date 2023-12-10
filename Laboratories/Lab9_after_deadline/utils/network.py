import torch
import torch.nn as nn
import torch.nn.functional as F

import matplotlib.pyplot as plt

from copy import deepcopy
import numpy as np
import random

import os

class FitnessNet_a(nn.Module):

    def __init__(self):
        super(FitnessNet_a, self).__init__()
        self.conv1 = nn.Conv1d(1, 6, 5)
        self.conv2 = nn.Conv1d(6, 16, 5)
        self.fc1 = nn.Linear(16*(1000-8), 32)
        self.fc2 = nn.Linear(32, 1)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = torch.flatten(x, start_dim=1)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x
    
class FitnessNet_b(nn.Module):

    def __init__(self):
        super(FitnessNet_b, self).__init__()
        self.conv1 = nn.Conv1d(1, 6, 5)
        self.fc1 = nn.Linear(6*(1000-4), 1)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = torch.flatten(x, start_dim=1)
        x = self.fc1(x)
        return x
    
class FitnessNet_c(nn.Module):

    def __init__(self):
        super(FitnessNet_c, self).__init__()
        self.conv1 = nn.Conv1d(1, 6, 5)
        self.conv2 = nn.Conv1d(6, 16, 5)
        self.conv3 = nn.Conv1d(16, 32, 5)
        self.conv4 = nn.Conv1d(32, 64, 5)
        self.fc1 = nn.Linear(64*(1000-4*4), 32)
        self.fc2 = nn.Linear(32, 1)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = F.relu(self.conv3(x))
        x = F.relu(self.conv4(x))
        x = torch.flatten(x, start_dim=1)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x

def generate_dataset(fitness, length_solution, size=100000):
    # Generate a vocabulary of solutions and their fitness, such that at each entry of the vocabulary there is the vector of the solution and the fitness of that solution
    dataset = {}
    for i in range(size):
        while True:
            x = np.random.randint(2, size=length_solution)
            if dataset.get(x.tobytes()) == None:
                break

        y = fitness(x)
        dataset[x.tobytes()] = (x,y)
    return dataset

# split dataset in train, val and test

def split_dataset(dataset, train_size=0.8, val_size=0.1, test_size=0.1):
    train_dataset = {}
    val_dataset = {}
    test_dataset = {}

    keys = list(dataset.keys())
    random.shuffle(keys)

    train_keys = keys[:int(train_size*len(keys))]
    val_keys = keys[int(train_size*len(keys)):int((train_size+val_size)*len(keys))] if val_size > 0 else []
    test_keys = keys[int((train_size+val_size)*len(keys)):] if test_size > 0 else []

    train_dataset = [(dataset[k][0], dataset[k][1]) for k in train_keys] 
    val_dataset = [(dataset[k][0], dataset[k][1]) for k in val_keys] if val_size > 0 else []
    test_dataset = [(dataset[k][0], dataset[k][1]) for k in test_keys] if test_size > 0 else []

    return train_dataset, val_dataset, test_dataset

# create a dataloader for the train dataset

def create_dataloader(dataset, batch_size=64):
    x = []
    y = []
    
    for k in dataset:
        x.append(k[0])
        y.append(k[1])

    x = torch.from_numpy(np.array(x)).float().unsqueeze(1)
    y = torch.from_numpy(np.array(y)).float()

    dataset = torch.utils.data.TensorDataset(x, y)
    dataloader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=True)

    return dataloader

def get_loaders(dataset, batch_size=64, train_size=0.8, val_size=0.1, test_size=0.1):
    train_dataset, val_dataset, test_dataset = split_dataset(dataset, train_size, val_size, test_size)
    train_dataloader = create_dataloader(train_dataset, batch_size)
    val_dataloader = create_dataloader(val_dataset, batch_size) if val_size > 0 else None
    test_dataloader = create_dataloader(test_dataset, batch_size) if test_size > 0 else None

    return train_dataloader, val_dataloader, test_dataloader

def train(model, train_dataloader, val_dataloader, test_dataloader, optimizer, criterion, device, epochs=50):
    best_loss = np.inf

    for epoch in range(epochs):
        model.train()
        for i, data in enumerate(train_dataloader):
            inputs, labels = data
            inputs = inputs.to(device)
            labels = labels.to(device)
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
        
        print('Epoch: ', epoch, ' Loss: ', loss.item())

        model.eval()
        val_loss = 0.0
        if val_dataloader != None:
            for i, data in enumerate(val_dataloader):
                inputs, labels = data
                inputs = inputs.to(device)
                labels = labels.to(device)
                outputs = model(inputs)
                loss = criterion(outputs, labels)
                val_loss += loss.item()

            avg_val_loss = val_loss/len(val_dataloader)
            print('Val Loss: ', avg_val_loss)
            # save the best model
            if avg_val_loss < best_loss:
                print("saving best model")
                best_loss = avg_val_loss
                state_dict = deepcopy(model.state_dict())

    if test_dataloader != None:  
        test(model, test_dataloader, criterion, device)

def test(model, test_dataloader, criterion, device):
    model.eval()
    test_loss = 0.0
    for i, data in enumerate(test_dataloader):
        inputs, labels = data
        inputs = inputs.to(device)
        labels = labels.to(device)
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        test_loss += loss.item()

    avg_test_loss = test_loss/len(test_dataloader)
    print('Test Loss: ', avg_test_loss)

def save_model(model, name):
    if not os.path.exists("models/" + name):
        os.makedirs("models/" + name)

    # save the model in the folder models changing the name with the problem size
    torch.save(model.state_dict(), "models/" + name + "/model.pth")

def plot_results(model, test_dataloader, criterion, device, save=False, name=""):
    values = []
    high = []
    low = []
    test_loss = 0.0

    for i, data in enumerate(test_dataloader):
        inputs, labels = data
        inputs = inputs.to(device)
        labels = labels.to(device)
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        test_loss += loss.item()
        
        for i, output in enumerate(outputs): 
            #print("output: ", output.item(), ", label: ", labels[i].item())
            diff = labels[i].item() - output.item()
            values.append(diff)
            if diff > 0.02 or diff < -0.02:
                high.append(output.item())
            else: 
                low.append(output.item())
            

    print("mean: ", np.mean(values))
    print("std: ", np.std(values))
    print("max: ", np.max(values))
    print("min: ", np.min(values))

    plt.hist(values, bins=100)
    plt.axvline(np.mean(values), color='r', linestyle='dashed', linewidth=1, label='mean')
    plt.axvline(np.mean(values) + np.std(values), color='g', linestyle='dashed', linewidth=1, label='mean + std')
    plt.axvline(np.mean(values) - np.std(values), color='g', linestyle='dashed', linewidth=1, label='mean - std')
    plt.axvline(np.max(values), color='k', linestyle='dashed', linewidth=1, label='max')
    plt.axvline(np.min(values), color='k', linestyle='dashed', linewidth=1, label='min')
    plt.legend(loc='upper right')
    plt.title("Histogram of the errors (label - output)")
    plt.xlabel("Error")
    plt.ylabel("Frequency")
    # save the plot of the histogram in the same folder of the model 
    plt.savefig("models/" + name + "/histogram.png")
    # save the mean, std, max and min in a txt file in the same folder of the model
    with open("models/" + name + "/errors.txt", "w") as f:
        f.write("mean: " + str(np.round(np.mean(values), decimals=5)) + "\n")
        f.write("std: " + str(np.round(np.std(values), decimals=5)) + "\n")
        f.write("max: " + str(np.round(np.max(values), decimals=5)) + "\n")
        f.write("min: " + str(np.round(np.min(values), decimals=5)) + "\n")
    plt.show()

    return values, high, low

def plot_high_low(high, low):
    # print information about the high and low errors
    print("high: ", len(high))
    print("low: ", len(low))
    print("high mean: ", np.mean(high))
    print("high std: ", np.std(high))
    print("low mean: ", np.mean(low))
    print("low std: ", np.std(low))
    print("high max: ", np.max(high))
    print("high min: ", np.min(high))
    print("low max: ", np.max(low))
    print("low min: ", np.min(low))

    # plot the high and low errors in the same way of the histogram
    plt.hist(high, bins=100)
    plt.axvline(np.mean(high), color='r', linestyle='dashed', linewidth=1, label='mean')
    plt.axvline(np.mean(high) + np.std(high), color='g', linestyle='dashed', linewidth=1, label='mean + std')
    plt.axvline(np.mean(high) - np.std(high), color='g', linestyle='dashed', linewidth=1, label='mean - std')
    plt.axvline(np.max(high), color='k', linestyle='dashed', linewidth=1, label='max')
    plt.axvline(np.min(high), color='k', linestyle='dashed', linewidth=1, label='min')
    plt.legend(loc='upper right')
    plt.title("Histogram of high errors output (|error| > 0.02))")
    plt.xlabel("Error")
    plt.ylabel("Frequency")
    plt.show()

    plt.hist(low, bins=100)
    plt.axvline(np.mean(low), color='r', linestyle='dashed', linewidth=1, label='mean')
    plt.axvline(np.mean(low) + np.std(low), color='g', linestyle='dashed', linewidth=1, label='mean + std')
    plt.axvline(np.mean(low) - np.std(low), color='g', linestyle='dashed', linewidth=1, label='mean - std')
    plt.axvline(np.max(low), color='k', linestyle='dashed', linewidth=1, label='max')
    plt.axvline(np.min(low), color='k', linestyle='dashed', linewidth=1, label='min')
    plt.legend(loc='upper right')
    plt.title("Histogram of low errors output (|error| <= 0.02))")
    plt.xlabel("Error")
    plt.ylabel("Frequency")
    plt.show()