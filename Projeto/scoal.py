#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 23:44:42 2017

@author: Fabrício Costa Antoniasse
"""
import funcoesScoal as fs
import os.path    


if __name__ == "__main__":
    
    ###Determina o caminho onde o dataset da fase de treinamento se encontra.
    dirTreino = os.path.join('/home/fabricio/Desktop/100k_carfre_10folds')
    inputPathTreino = os.path.join('mean', 'datatrain_m_5.csv')
    fileNameTreino = os.path.join(dirTreino, inputPathTreino)
    
    resultado = fs.ajustar(fileNameTreino,4,4) #Valores dos pesos dos modelos preditivos e dos dicionários {user_id: cluster linha} e {id_item: cluster coluna}
    
    ###Determina o caminho onde o dataset da fase de teste se encontra.
    dirTeste = os.path.join('/home/fabricio/Desktop/100k_carfre_10folds')
    inputPathTeste = os.path.join('mean', 'datatest_m_5.csv')
    fileNameTeste = os.path.join(dirTeste, inputPathTeste)
    
    erro = fs.predicao(fileNameTeste,resultado[0], resultado[1], resultado[2]) # Valor do erro MSE global do dataset Teste.