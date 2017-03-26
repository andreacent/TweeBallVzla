#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import network
import numpy as np

#Split data
def split(data,percentage):
    rows=len(data)
    trainRows=int(round((percentage*rows)/float(100)))
    trainD = data[:trainRows]
    testD = data[trainRows:]
    return trainD,testD

##############################################
# Read file
# @param [File] data_file : file with data
def readDataFile(filename):
    inputs,target, data = [],[],[]

    with open(filename, 'r', encoding="utf-8") as data_file:
        for line in data_file:
            l =line.split(",")

            if (l[-1][:-1] == "Iris-setosa"):
                data.append([ float(l[0]), float(l[1]), float(l[2]), float(l[3]), float(1) ])

            else:
                data.append([ float(l[0]), float(l[1]), float(l[2]), float(l[3]), float(0) ])

        np.random.shuffle(data)
            
        for d in data:
            inputs.append([ d[0], d[1], d[2], d[3] ])
            target.append([ d[4] ])

    return inputs, target

##############################################
# MAIN
def main(argv):
    inputs, target = readDataFile(argv[1])
    percentage=[50,60,70,80,90]

    for p in percentage:
        trainI, testI = split(inputs,p)
        trainT, testT = split(target,p)
        print("\n####################   "+str(p)+"%   ####################\nTrain input rows: "+str(len(trainI)))
        print("Train target rows: ",len(trainT))
        print("Test input rows: ",len(testI))
        print("Test target rows: ",len(testT),"\n")

        filename = argv[1].split(".")[0]+str(p)+"%"+"-neuronas-"
        filename = "SALIDAS31/"+filename.split("/")[1]

        nn_list = []

        #Normalizar
        trainI = network.normalize_array(trainI)

        for k in range(4,11):
            nn = network.NeuralNetwork(2,k,1)
            nn.backPropUpdate(trainI, trainT, 0.1, 1000, filename+str(k)+".txt")
            nn_list.append(nn)

        #Test partition
        old_t_inputs = testI
        t_target = testT
        
        t_inputs = [x[:] for x in old_t_inputs]
        #Normalizar
        t_inputs = network.normalize_array(t_inputs)

        for n in nn_list:

            print("---------NEURONAS ",n.num_h,"----------")
            nn = network.NeuralNetwork(2,n.num_h,1) #red tam2

            buenas = 0
            falso_positivo = 0
            falso_negativo = 0
            for i in range(len(t_inputs)):
                output=nn.predict(t_inputs[i],n.weight_i,n.weight_o)
                for o in range(len(output)):
                    resultado = round(abs(output[o]),0)
                    if t_target[i][o] == resultado:
                        buenas += 1 
                    elif resultado == 1: 
                        falso_positivo += 1
                    else:
                        falso_negativo += 1

                    #print("esperado: "+str(t_target[i][o])+" obtenido: "+str(round(abs(output[o]),0)))

            print("Predicciones correctas:",buenas,"\nFalso positivo:",falso_positivo,"\nFalso negativo:",falso_negativo,"\n")


if __name__ == "__main__":
    main(sys.argv)