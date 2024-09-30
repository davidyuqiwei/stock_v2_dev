#https://www.datatechnotes.com/2024/04/sequence-prediction-with-lstm-model-in.html
import torch
import torch.nn as nn
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
from torch.utils import data

from scripts_stock.analysis.fuquan_data.get_data_sql import FGetDataSql 
from scripts_stock.utils.common import CommonScript
from scripts_stock.cfg.set_dir import ProjectDir
import os


# Convert data into sequence and label with given length
def create_labels(data, step):
    X = np.array([data[i:i+step] for i in range(len(data) - step)])
    y = np.array(data[step:])
    return X, y


def get_train_test_data_lstm(df1,df,step_size):
    # Define parameters
    # step_size = 20
    N = df1.shape[0]
    forecast_start = int(df1.shape[0]*0.9)
    # Prepare data for training and testing
    values = df.values
    train, test = values[:forecast_start, :], values[forecast_start:N, :]

    # generate sequence data
    trainX, trainY = create_labels(train, step_size)
    # print(trainX.shape,trainY.shape)
    testX, testY = create_labels(test, step_size)

    # Reshape data for LSTM input
    trainX = np.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
    testX = np.reshape(testX, (testX.shape[0], 1, testX.shape[1]))
    return trainX, trainY,testX, testY 

# trainX, trainY,testX, testY = get_train_test_data_lstm(df1,df,step_size)

def norm_train_test_data(X_input,Y_input):
    max_values_X = np.max(X_input, axis=(1, 2), keepdims=True)
    X_input_norm = X_input/max_values_X
    Y_input_norm = Y_input/max_values_X.reshape(max_values_X.shape[0],1)
    return X_input_norm,Y_input_norm


def get_train_test_data_pytorch(stock_list,date_cut,step_size):
    train_x_list = []
    train_y_list = []
    test_x_list = []
    test_y_list = []
    for i in stock_list["stock_index"].tolist():
        input_sql_str = FGetDataSql.get_data_sql_str_before_years(i,date_cut)
        df1 = pd.read_sql_query(input_sql_str, conn)
        df = df1[["high"]]
        trainX, trainY,testX, testY = get_train_test_data_lstm(df1,df,step_size)
        trainX_norm,trainY_norm = norm_train_test_data(trainX,trainY)

        # max_values_train = np.max(trainX, axis=(1, 2), keepdims=True)
        # trainX_norm = trainX/max_values_train
        # trainY_norm = trainY/max_values_train.reshape(max_values_train.shape[0],1)
        train_x_list.append(trainX_norm)
        train_y_list.append(trainY_norm)
        
        # max_values_test = np.max(testX, axis=(1, 2), keepdims=True)
        # testX_norm = testX/max_values_test
        # testY_norm = testY/max_values_test.reshape(max_values_test.shape[0],1)
        testX_norm,testY_norm =  norm_train_test_data(testX,testY)
        test_x_list.append(testX_norm)
        test_y_list.append(testY_norm)

        
    trainX = np.concatenate(train_x_list, axis=0)
    trainY = np.concatenate(train_y_list, axis=0)
    trainX_tens = torch.tensor(trainX, dtype=torch.float32)
    trainY_tens = torch.tensor(trainY, dtype=torch.float32)

    train_dataset = torch.utils.data.TensorDataset(trainX_tens, trainY_tens)
    train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=64)

    testX_v1 = np.concatenate(test_x_list, axis=0)
    testY_v1 = np.concatenate(test_y_list, axis=0)
    # Convert data to PyTorch tensors

    testX_tens = torch.tensor(testX_norm, dtype=torch.float32)
    testY_tens = torch.tensor(testY_norm, dtype=torch.float32)



    print(trainX.shape,trainY.shape)
    print(testX_tens.shape,testY_tens.shape)
    return train_loader,test_x_list,test_y_list


# Define LSTM model
class LSTMModel(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(LSTMModel, self).__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        out, _ = self.lstm(x)
        out = self.fc(out[:, -1, :])  # Take the last time step's output
        return out
    

def train_model(train_loader,step_size):
    # Hyperparameters
    input_size = step_size
    hidden_size = 128
    output_size = 1
    epochs = 100
    learning_rate = 0.001
    
    # Instantiate LSTM model
    model = LSTMModel(input_size=input_size, hidden_size=hidden_size, output_size=output_size)

    # Define loss function and optimizer
    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)



    # Train the model
    for epoch in range(epochs):
    #for epoch in range(10):
        model.train()
        for batch_X, batch_Y in train_loader:
            optimizer.zero_grad()  # Clears the gradients of all optimized parameters.
            output = model(batch_X)

            # Computes the loss between the model predictions and the ground
            # truth labels for the current mini-batch.
            loss = criterion(output, batch_Y)

            # Computes gradients of the loss with respect to model parameters.
            loss.backward()

            # Updates model parameters based on the computed gradients using
            # the specified optimization algorithm.
            optimizer.step()

        if (epoch + 1) % 10 == 0:
            print(f'Epoch [{epoch + 1}/{epochs}], Loss: {loss.item():.4f}')
    return model

def get_test_error(test_x_list,test_y_list):
    error_list = []
    for i in range(0,len(test_x_list)):
        testX_tens = torch.tensor(test_x_list[i], dtype=torch.float)
        with torch.no_grad():
            #model.eval()
            testPredict = model(testX_tens)
        error_v1 = np.round(np.average(abs((testPredict.numpy()-test_y_list[i])/test_y_list[i])),3)
        error_list.append(error_v1)

    error_1day = round(np.average(error_list),3)

    return error_1day

step_size = 10
conn = CommonScript.connect_to_db("test.db")
date_cut = "2022-01-01"

input_sql_str_v1 = FGetDataSql.get_distinct_stock_index_infuquan()
stock_list = pd.read_sql_query(input_sql_str_v1, conn)

train_loader,test_x_list,test_y_list = get_train_test_data_pytorch(stock_list,date_cut,step_size)

model = train_model(train_loader,step_size)


error_1day = get_test_error(test_x_list,test_y_list)
print(error_1day)
model_path = os.path.join(ProjectDir.model_dir,"ts_pred_lstm","lstm_"+str(step_size)+"_error_"+str(error_1day)+"_test.pth")
torch.save(model.state_dict(), model_path)


conn.close()


"""
predict 
i="601398"
date_cut = "2024-09-01"
input_sql_str = FGetDataSql.get_data_sql_str_before_years(i,date_cut)
df1 = pd.read_sql_query(input_sql_str, conn)
test_data = df1.tail(10)
testx = np.array(test_data["high"])
testx_v1 = np.array([testx])
testx_v2 = np.reshape(testx_v1, (testx_v1.shape[0], 1, testx_v1.shape[1]))
max_values_X = np.max(testx_v2, axis=(1, 2), keepdims=True)
testx_v3 = testx_v2/max_values_X
testX_tens = torch.tensor(testx_v3, dtype=torch.float32)
with torch.no_grad():
    #model.eval()
    testPredict = model(testX_tens)
print(max_values_X[0][0][0])
testPredict[0][0]*max_values_X[0][0][0]

"""