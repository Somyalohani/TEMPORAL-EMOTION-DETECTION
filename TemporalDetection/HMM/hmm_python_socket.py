#!/usr/bin/env python


import asyncio
import websockets
import json
import pandas as pd
import numpy as np
import csv
from csv import reader

#Global
FRAMES = [] 

#Model_functions 
def forward(V, a, b, initial_distribution):
    alpha = np.zeros((V.shape[0], a.shape[0]))
    alpha[0, :] = initial_distribution * b[:, V[0]]
    for t in range(1, V.shape[0]):
        for j in range(a.shape[0]):
            alpha[t, j] = alpha[t - 1].dot(a[:, j]) * b[j, V[t]]
    return alpha

def backward(V, a, b):
    beta = np.zeros((V.shape[0], a.shape[0]))
    beta[V.shape[0] - 1] = np.ones((a.shape[0]))
    for t in range(V.shape[0] - 2, -1, -1):
        for j in range(a.shape[0]):
            beta[t, j] = (beta[t + 1] * b[:, V[t + 1]]).dot(a[j, :])
    return beta

# need to make sure that all lists in V are of same length
def baum_welch(V, a, b, initial_distribution, n_iter=100):
    M = a.shape[0]
    T = len(V[0])
    for n in range(n_iter):
        xi = np.zeros((M, M, T - 1))
        for vs in V:
            alpha = forward(vs, a, b, initial_distribution)
            beta = backward(vs, a, b)
            for t in range(T - 1):
                denominator = np.dot(np.dot(alpha[t, :].T, a) * b[:, vs[t + 1]].T, beta[t + 1, :])
                for i in range(M):
                    numerator = alpha[t, i] * a[i, :] * b[:, vs[t + 1]].T * beta[t + 1, :].T
                    xi[i, :, t] += numerator / denominator
        gamma = np.sum(xi, axis=1)
        a = np.sum(xi, 2) / np.sum(gamma, axis=1).reshape((-1, 1))
        gamma = np.hstack((gamma, np.sum(xi[:, :, T - 2], axis=0).reshape((-1, 1))))
        K = b.shape[1]
        denominator = np.sum(gamma, axis=1)
        for l in range(K):
            sumval = 0
            for vs in V:
                sumval += np.sum(gamma[:, vs == l], axis=1)
            b[:,l] = sumval
        b = np.divide(b, denominator.reshape((-1, 1)))
    return {"a":a, "b":b}

with open('Train_set', 'r') as read_obj:
    csv_reader = reader(read_obj)
    train = list(csv_reader)
train_list = []
for inner_list in train:
    inner_out_list = []
    for string in inner_list:
        inner_out_list.append(int(string))
    train_list.append(inner_out_list)

# this is a 3 nod dataset created manually, all of size 8
V = np.array(train_list)

# no of states and actions are chosen as up, down and stable. 
a = np.ones((3, 3))
a = a / np.sum(a, axis=1)

b = np.ones((3,3))
b = b / np.sum(b, axis=1).reshape((-1, 1))

# starts with stable
initial_distribution = np.array((1,0,0))

# print(baum_welch(V, a, b, initial_distribution, n_iter=100))
# abdict contains both the learned parameters -> a and b.
# these will be used for predictions
abdict = baum_welch(V, a, b, initial_distribution, n_iter=100)

def prediction(test_seq, abdict, threshold=0.001):
    initial_distribution = np.array((1,0,0))
    return (forward(test_seq, abdict['a'], abdict['b'], initial_distribution)[-1,0]*pow(10,-16))


def create_json(res, a, b):
    return json.dumps({"result" : res, "stime" : a, "endtime" : b})

async def consumer(websocket, path):
    async for message in websocket:
        result = "False"
        stime = 0.00
        endtime = 0.00
        FRAMES.append(message)
        n = len(FRAMES)
        if(n >= 17):
            rdata = FRAMES[n-16:n]
            lis1 = []
            for dic in rdata:
                try:
                    dicti = eval(dic)
                    lis1.append(dicti['measurements']['orientation']['pitch'])
                except:
                    SyntaxError
            li1 = []
            for i in range(1, 16):
                dx = lis1[i] - lis1[i-1]
                if (abs(dx) < 1):
                    li1.append(0)
                elif (dx > 0):
                    li1.append(1)
                else:
                    li1.append(2)
            val = prediction(np.array(li1), abdict)
            if ( 0.5 <= val <= 1):
                result = "True"
                endtime = n*0.2
                stime = endtime - 3.2
                
        message1 = "Result of nod detection: " + str(result) + " Start Time: " + str(stime) + " End Time: " + str(endtime)
        print(message)
        print(message1)
        await websocket.send(create_json(result, stime, endtime))


if __name__ == '__main__':
    start_server = websockets.serve(consumer, "localhost", 3000)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
