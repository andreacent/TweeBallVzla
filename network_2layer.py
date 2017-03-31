#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math
import random
import numpy as np

TOL = 0.000001

def sigmoid(x):
    return math.tanh(x)

#Derivada de sigmoid
def dSigmoid(x):
    return 1 - x**2

#Normalize array
def normalize_array(data):

    rows = len(data)
    columns = len(data[0])
    for j in range(columns):
        #Mean
        mean = 0
        for i in range(rows):
            mean += data[i][j]
        mean = mean/rows

        #std
        std = 0
        for i in range(rows):
            std += math.pow(data[i][j]-mean,2)
        std = math.sqrt(std/rows)

        #Nomalize inputs
        for i in range(rows):
            data[i][j]= (data[i][j] - mean)/std

    return data

# Resta de listas
# @param [Float] x : 
# @param [Float] y : 
def subList(x,y):
    res = []
    for i in range(len(x)):
        res.append(x[i] - y[i])
    return res

class NeuralNetwork:

    # @param Int num_i : Número de neuronas de la capa de entrada.
    # @param Int num_h : Número de neuronas de la capa oculta.
    # @param Int num_o : Número de neuronas de la capa de salida.
    def __init__(self, num_i, num_h, num_o):
        # number of nodes in layers
        self.num_i = num_i + 1 # +1 for bias
        self.num_h = num_h
        self.num_o = num_o

        # Weight
        self.weight_i = [[random.uniform(-0.5, 0.5) for j in range(self.num_h)] for i in range(self.num_i)]
        self.weight_h = [[random.uniform(-0.5, 0.5) for j in range(self.num_h)] for i in range(self.num_h)]
        self.weight_o = [[random.uniform(-0.5, 0.5) for j in range(self.num_o)] for i in range(self.num_h)]

        #Activation
        self.activation_i = [1.0 for j in range(self.num_i)]
        self.activation_h1 = [0.0 for j in range(self.num_h)]
        self.activation_h2 = [0.0 for j in range(self.num_h)]
        self.activation_o = [0.0 for j in range(self.num_o)]

    # @param [Int] inputs : Arreglo que contiene las entradas de la red neuronal
    def runNetwork(self, inputs):

        #Input layer
        for i in range(self.num_i-1):
            self.activation_i[i] = inputs[i]

        #Hidden layer1
        for i in range(self.num_h):
            nodeSum = float(0.0)
            #sum(W(j,i)*Aj)
            for j in range(self.num_i):
                nodeSum += self.weight_i[j][i] * self.activation_i[j]

            #Apply g/sigmoid            
            self.activation_h1[i]= sigmoid(nodeSum)

        #Hidden layer2
        for i in range(self.num_h):
            nodeSum = float(0.0)
            #sum(W(j,i)*Aj)
            for j in range(self.num_h):
                nodeSum += self.weight_h[j][i] * self.activation_h1[j]

            #Apply g/sigmoid            
            self.activation_h2[i]= sigmoid(nodeSum)

        #Output layer
        for i in range(self.num_o):
            nodeSum = float(0.0)
            #sum(W(j,i)*Aj)
            for j in range(self.num_h):
                nodeSum += self.weight_o[j][i] * self.activation_h2[j]

            #Apply g/sigmoid 
            self.activation_o[i] = sigmoid(nodeSum)

        return self.activation_o

    # @param [[Int]] input : Conjunto de todos los inputs
    # @param [[Int]] target : Conjunto de objetivos a predecir
    # @param Int alpha : Tasa de aprendizaje
    # @param Int numIter : Numero de iteraciones
    def backPropUpdate(self, inputs, target, alpha, numIter, filename):
        output = 0
        myFile=open(filename, 'w')
        myFile.write("iter , error\n")
        error = 100
        for it in range(numIter):
            e=0

            old_error = error
            error = 0

            for inp in inputs:
                #Compute the output for this input/example
                output = self.runNetwork(inp)

                #Compute the error and delta for units in the output layer
                o_error = subList(target[e],output)
                o_delta = [0.0] * self.num_o
                for k in range(self.num_o):
                    o_delta[k] = o_error[k] * dSigmoid(self.activation_o[k])
                    error += math.pow(o_error[k],2)

                #Update the weights leading to the output layer
                for k in range(self.num_o):
                    for i in range(self.num_h):
                        self.weight_o[i][k] += alpha * self.activation_h2[i] * o_delta[k] 
                        

                #HIDDEN LAYER2
                #Compute the error at each node
                h2_delta = [0.0] * self.num_h
                for i in range(self.num_h):
                    n2_error = 0.0
                    for k in range(self.num_o):
                        n2_error += o_delta[k] * self.weight_o[i][k]
                    h2_delta[i] = n2_error * dSigmoid(self.activation_h2[i])

                #Update the weights leading to the layer (hidden weight)
                for i in range (self.num_h):
                  for j in range (self.num_h):
                    self.weight_h[i][j] += alpha * self.activation_h1[i] * h2_delta[j]

                #HIDDEN LAYER1
                #Compute the error at each node
                h1_delta = [0.0] * self.num_h
                for i in range(self.num_h):
                    n1_error = 0.0
                    for k in range(self.num_h):
                        n1_error += h2_delta[k] * self.weight_h[i][k]
                    h1_delta[i] = n1_error * dSigmoid(self.activation_h1[i])

                #Update the weights leading to the layer (input weight)
                for i in range (self.num_i):
                  for j in range (self.num_h):
                    self.weight_i[i][j] += alpha * self.activation_i[i] * h1_delta[j]


                #Update target counter
                e+=1

            error = error /( 2*len(inputs))  
            myFile.write(str(it+1)+" , "+str(error)+'\n')

            if abs(old_error - error) < TOL:
                break

        myFile.close()

    # @param [Int] inputs : Arreglo que contiene las entradas de la red neuronal
    def predict(self, inp, weight_i, weight_h, weight_o):
        # Weight
        self.weight_i = weight_i
        self.weight_h = weight_h
        self.weight_o = weight_o
        return self.runNetwork(inp)