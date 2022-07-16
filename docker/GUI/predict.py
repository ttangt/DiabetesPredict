import numpy as np
import pandas as pd

from keras.models import Sequential, load_model
from keras.layers import Dense
from keras.callbacks import EarlyStopping

from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split

input_data_file = "pima-indians-diabetes.csv"
pretrained_model = "saved_model.h5"

output_label = {0: "Negative", 1: "Positive"}

def data_preprocessing():
    dataframe = pd.read_csv(input_data_file, header = None)
    dataset = np.array(dataframe)

    X = dataset[:, 0:8]
    y = dataset[:, 8]

    y = pd.get_dummies(y).values

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.33, random_state = 50)

    scaler = StandardScaler().fit(X_train)
    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)

    return scaler

def construct_model():
    model = Sequential()
    model.add(Dense(8, input_shape = (8,), activation = "relu"))
    model.add(Dense(4, activation = "relu"))
    model.add(Dense(2, activation = "softmax"))
    model.compile(loss = "categorical_crossentropy", optimizer = "adam", metrics = ["accuracy"])

def fit_model():
    callbacks = EarlyStopping(monitor = "loss", patience = 5)
    history = model.fit(X_train, y_train, epochs = 800, batch_size = 32, callbacks = [callbacks], validation_data = (X_test, y_test))
    model.save(pretrained_model)

def load_model_predict(input_array):
    scaler = data_preprocessing()
    loaded_model = load_model(pretrained_model)
    # test_1 = [[5, 105, 72, 29, 325, 36.9, 0.159, 28]]
    # print(test_1)
    # test_1 = scaler.transform(test_1)
    # print(test_1)
    # pred_1 = loaded_model.predict(test_1)
    # print(pred_1)
    # print(output_label[np.argmax(pred_1)])

    input_data = [input_array]
    input_data = scaler.transform(input_data)
    output_prob = loaded_model.predict(input_data)
    dprob = str(output_prob[0][1])
    dclass = output_label[np.argmax(output_prob)]
    
    return [dprob, dclass]