#!/usr/bin/env pytho    
# -*- coding: utf-8 -*-
import sys
import network
import readData as rd

##############################################
# MAIN
def main(argv):
    data,words = rd.readTrainingData(argv[1])
    d_input,d_target = rd.transformData(data,words)
    del data
    
    print(words)

    #for i in range(len(d_input)):
    #    print(d_input[i],d_target[i])

    percentage=[50,60]
    n_words = len(words)

    for p in percentage:
        trainI, testI = split(d_input,p)
        trainT, testT = split(d_target,p)
        print("\n####################   "+str(p)+"%   ####################\nTrain input rows: "+str(len(trainI)))
        print("Train target rows: ",len(trainT))
        print("Test input rows: ",len(testI))
        print("Test target rows: ",len(testT),"\n")

        filename = argv[1].split(".")[0]+str(p)+"%"+"-neuronas-"
        filename = "SALIDA/"+filename.split("/")[1]

        nn_list = []

        #Normalizar
        #trainI = network.normalize_array(trainI)

        for k in range(4,5):
            nn = network.NeuralNetwork(n_words,k,1)
            nn.backPropUpdate(trainI, trainT, 0.1, 1000, filename+str(k)+".txt")
            nn_list.append(nn)

        #Test partition
        old_t_inputs = testI
        t_target = testT
        
        t_inputs = [x[:] for x in old_t_inputs]
        #Normalizar
        #t_inputs = network.normalize_array(t_inputs)

        for n in nn_list:

            print("---------NEURONAS ",n.num_h,"----------")
            nn = network.NeuralNetwork(n_words,n.num_h,1) #red tam2

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

    '''

if __name__ == "__main__":
    main(sys.argv)