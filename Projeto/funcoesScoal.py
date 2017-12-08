#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 23:45:22 2017

@author: Fabrício Costa Antoniasse
"""
import findspark
findspark.init()
import pyspark
sc = pyspark.SparkContext(appName="Proj_SCOAL")
import numpy as np


###Função que recebe o id_user, id_item, os limites dos clusters de linha e coluna (cl_L e cl_C) e os vetores com os ids dos usuários e dos itens (v_user e v_item)
###Retorna uma tupla contendo no primeiro elemento a qual co-cluster o objeto se encontra, no segundo elemento o cluster de linha e no terceiro o cluster de coluna. 
def coclusters(user,item,cl_L,cl_C,v_user,v_item):

    for lin in range(len(cl_L)):
        for col in range(len(cl_C)):
            if (user in v_user[cl_L[lin][0]-1:cl_L[lin][1]] ):
                if(item in v_item[cl_C[col][0]-1:cl_C[col][1]] ):
                    return (col+1) + len(cl_C)*(lin) , lin , col 



### Função que treina os modelos. Retorna os pesos, Beta, atualizados.
def modelos(pesos,niteracao,dataRDD,alpha):
    pBeta = pesos
    for _ in range(niteracao):
        
        test = dataRDD.map(lambda x : (x[-1][0],nabla(x[3],x[-1][0],x[2],pBeta))).reduceByKey(lambda x,y : np.array(x)+np.array(y)).map(lambda x : (x[0],addBeta(x[0],x[1]*(alpha),pBeta))).sortByKey()
        pBeta = test.collect()
        
    return pBeta

###Função que calcula o valor de (z - ẑ)*xi.
def nabla(vet_x, n_beta, y, pesos ):
    produto = np.dot(vet_x,pesos[n_beta-1][1])
    return np.dot((y- produto),vet_x)


###Função que soma o vetor Beta com o valor de nabla associado, a fim de realizar o ajuste do vetor Beta.
def addBeta(n_beta,vet_xB,pesos):
    return np.array(pesos[n_beta-1][1])+vet_xB


###Função calcula o quadrado do residuo (z - ẑ).
def mse(vet_x, n_beta,y,peso):
    produto = np.dot(vet_x,peso[n_beta-1][1])
    return pow((y - produto),2)

###Calcula os erros , MSE global dos clusters linha, referente ao usuário.
def mseClustersLinha (user,rating,n_clus,clusterLinha,cl_L,cl_C,peso):
    quantidadeClusterLinha = len(cl_L)
    quantidadeClusterColuna = len(cl_C)
    aux = n_clus - clusterLinha*(quantidadeClusterColuna)
    erros = []
    for linha in range(quantidadeClusterLinha):
        erros.append(mse(user,aux,rating,peso))
        aux += quantidadeClusterColuna
    return erros

###Calcula os erros , MSE global dos clusters coluna, referente ao item.
def mseClustersColuna (x_atr,rating,n_clus,clusterColuna,cl_L,cl_C,peso):
    quantidadeClusterColuna = len(cl_C)
    aux = n_clus - clusterColuna
    erros = []
    for coluna in range(quantidadeClusterColuna):
        erros.append(mse(x_atr,aux,rating,peso))
        aux += 1
    return erros

'''A função "mudanca" recebe uma lista contendo os MSE's dos clusters de linha ou de coluna e retorna o indice do menor valor encontrado. Ela auxilia 
no processo de atualização dos clusters de linha e de coluna.'''
def mudanca(x_erros):
    return x_erros.index(min(x_erros))

###Funçao que tem por objetivo atualizar o co-cluster que o par usuário-item se encontra.
def atualizaCoclusters(lin , col, cl_C):
    return (col+1) + len(cl_C)*(lin)




'''A função "ajustar" tem o papel de realizar o treinamento global do SCOAL. Recebe o caminho do arquivo de leitura (dataset treino), o número de co-clusters 
e o numero de partições do RDD. Retorna a matriz contendo os valores de Beta com seus respectivos co-clusters e os dicionarios {user_id: cluster linha}
e {id_item: cluster coluna}'''    
def ajustar(pathArquivo,configuração,numParticoes):
    
    ###Leitura e tratamento dos dados.
    data = sc.textFile(pathArquivo,numParticoes)
    header = data.take(1)[0]
    # dataRdd tem a forma: [user_id, item_id, rating, atb_user1, atb_user2, atb_useri, atb_item1, atb_item2, atb_itemj].
    dataRdd = data.filter(lambda x : x != header).map(lambda x : x.split(',')).map(lambda x : list(map(float,x)))
    
    ###Variáveis
    quantidade = dataRdd.count() # Quantidade de observações da base de treinamento.
    v_user  = sorted(dataRdd.map(lambda x : x[0]).distinct().collect()) # Vetor dos ids dos usuários.
    v_item = sorted(dataRdd.map(lambda x : x[1]).distinct().collect()) # Vetor dos ids dos itens.
    
    ###Dicionário contendo as configurações dos co-clusters. Limites dos clusters de linha e de coluna .  . 
    dic = { 4:[[(1,400),(401,len(v_user))] ,[(1,800),(801,len(v_item))]], 
            8:[[(1,200),(201,400),(401,600),(601,len(v_user))],[(1,800),(801,len(v_item))]],
            16:[[(1,200),(201,400),(401,600),(601,len(v_user))],[(1,400),(401,800),(801,1200),(1201,len(v_item))]],
            32:[[(1,100),(101,200),(201,300),(301,400),(401,500),(501,600),(601,700),(701,len(v_user))],[(1,400),(401,800),(801,1200),(1201,len(v_item))]],
            64:[[(1,100),(101,200),(201,300),(301,400),(401,500),(501,600),(601,700),(701,len(v_user))],[(1,200),(201,400),(401,600),(601,750),(751,900),(901,1000),(1001,1100),(1101,len(v_item))]], 
            128:[[(1,70),(71,140),(141,200),(201,260),(261,310),(311,370),(371,440),(441,510),(511,580),(581,630),(631,680),(681,730),(731,780),(781,830),(880,910),(911,len(v_user))],[(1,200),(201,400),(401,600),(601,750),(751,900),(901,1000),(1001,1100),(1101,len(v_item))]] }
    cl_L , cl_C =  dic[configuração]
    
    
    
    ###É adicionado o valor 1, referente ao Bias da regressão linear, e uma tupla contendo no primeiro elemento o co-cluster, no segundo elemento o cluster de linha e no terceiro o cluster de coluna que o objeto se encontra.
    ###dataCluster tem a forma de: [user_id, item_id, rating,[1,atb_user1, atb_user2, atb_useri, atb_item1, atb_item2, atb_itemj],(nCocluster, clusterLinha, clusterColuna)].
    dataCluster = dataRdd.map(lambda x : x[:3]+[[1] +x[3:]]+[coclusters(x[0],x[1],cl_L,cl_C,v_user,v_item)]) 
    
    
    ###Criação da matriz dos pesos B (beta).
    pesos = np.random.normal(0.1,0.001,(len(cl_L)*len(cl_C),len(dataCluster.take(1)[0][3])))# Geração dos pesos randomicamente.
    beta = list(zip(np.arange((len(cl_L)*len(cl_C)))+1,pesos))# Matriz que assossia o numero do co-cluster com os pesos gerados.
    
    ###Treinamento dos modelos de regressão. modelos dos pesos.
    ### A função "modelos()" recebe como parâmetros a matriz de pesos, o número de iterações e o RDD dataCluster. Retorna a matriz com os pesos atualizados.
    beta = modelos(beta,20,dataCluster,alpha = 0.0000001)
    
    mse_final=[0] # Criação da lista que conterá os erros (MSE_global) de cada iteração. Servirá como referência para a convergência
    
    ###Atualização dos clusters de linha e de coluna. Rearranjos dos usuários e itens.
    for iteracao in range(20):
        
        ###Atualização dos clusters de linha.
        mudancaL = dataCluster.map(lambda x : [x[0], mseClustersLinha(x[3],x[2],x[-1][0],x[-1][1],cl_L,cl_C,beta)])\
                              .reduceByKey(lambda x ,y : np.array(x)+np.array(y))\
                              .mapValues(lambda x : mudanca(list(x)))\
    
        dsAuxiliar = dataCluster.map(lambda x : [x[0], x[1:]]).leftOuterJoin(mudancaL)\
                                .map(lambda x : [x[0]]+ x[1][0][:-1] +[(x[1][0][-1][0],x[1][-1],x[1][0][-1][2])])
    
        
        ###Atualização dos clusters de coluna.
        mudancaC = dsAuxiliar.map(lambda x : [x[1], mseClustersColuna(x[3],x[2],x[-1][0],x[-1][2],cl_L,cl_C,beta)])\
                             .reduceByKey(lambda x ,y : np.array(x)+np.array(y))\
                             .mapValues(lambda x : mudanca(list(x)))
    
        dsFinal = dsAuxiliar.map(lambda x : (x[1],x[:])).leftOuterJoin(mudancaC)\
                            .map(lambda x : x[1]).map(lambda x : x[0][:4]+[(x[0][4][0],x[0][4][1],x[-1])])
    
        
        ###Atualização dos co-clusters.
        novoDataCluster= dsFinal.map(lambda x : x[:4]+[(atualizaCoclusters(x[4][1],x[4][2],cl_C),x[4][1],x[4][2])])
        
        ###Atualização do RDD, dataCluster, para que seja realizada novamente o processo de treinamento dos modelos e rearranjos dos clusters de linha e de coluna.
        dataCluster = sc.parallelize(novoDataCluster.collect(),numParticoes)
        
        
        ###Treinamento dos modelos de regressão. Ajuste dos pesos.
        beta = modelos(beta,10,dataCluster,alpha=0.0000001)
        
        ###Cálculo do erro MSE global.
        erro = dataCluster.map(lambda x : (x[-1][0],mse(x[3],x[-1][0],x[2],beta))).reduceByKey(lambda x,y : x +y).map(lambda x : x[1]).sum()/quantidade
        mse_final.append(erro)
        
        ###Critério de convergência. Quando a diferença for menor que 10^(-4) ,entre os erros globais consecutivos, ou a quantidade de iterações acabar.
        if (abs(mse_final[-2]-mse_final[-1])<0.0001 or iteracao==19):
            
            ###Geração dos dicionários. dic_users tem a forma: dic_users = {user_id : cluster linha}
            limitsCoclusters = dataCluster.map(lambda x : [(x[0],x[-1][1]),(x[1],x[-1][2])])
            dic_users = limitsCoclusters.map(lambda x : x[0]).distinct().sortByKey().collectAsMap()
            dic_itens = limitsCoclusters.map(lambda x : x[1]).distinct().sortByKey().collectAsMap()
            
            return beta, dic_users, dic_itens 



'''
A função "predicao" tem o papel de realizar o cálculo do MSE global da base de teste. Recebe o caminho do arquivo de leitura (dataset teste), os dicionários 
{user_id: cluster linha} e {id_item: cluster coluna}.Retorna o erro médio quadrático do dataset em questão''' 
def predicao(pathArquivo,beta, dic_users,dic_itens):
    
    
    
    v_user = list(dic_users.keys()) # Lista dos ids dos usuários que estiveram na fase de treinamento.
    v_item = list(dic_itens.keys()) # Lista dos ids dos itens que estiveram na fase de treinamento.
    
    ###Leitura e tratamento dos dados.
    dataTest = sc.textFile(pathArquivo)
    header = dataTest.take(1)[0]
    # dataRdd tem a forma: [user_id, item_id, rating, atb_user1, atb_user2, atb_useri, atb_item1, atb_item2, atb_itemj].
    dataRdd = dataTest.filter(lambda x : x != header).map(lambda x : x.split(',')).map(lambda x : list(map(float,x)))
    
    ###O RDD semColdStart filtra as possíveis observações, no dataset teste, cujos usuários ou itens não existam no dataset treino.
    semColdStart = dataRdd.filter(lambda x : (x[0] in v_user) and (x[1] in v_item))
        
    quantidade = semColdStart.count() # Quantidade de observações da base de teste.
    
    ###É adicionado o valor 1, referente ao Bias da regressão linear, e uma tupla contendo no primeiro elemento o co-cluster, no segundo elemento o cluster de linha e no terceiro o cluster de coluna que o objeto se encontra.
    ###dfTeste tem a forma de: [user_id, item_id, rating,[1,atb_user1, atb_user2, atb_useri, atb_item1, atb_item2, atb_itemj],(nCocluster, clusterLinha, clusterColuna)].
    dfTeste = semColdStart.map(lambda x : x[:3]+[[1] +x[3:]]+[atualizaCoclusters(dic_users[x[0]],dic_itens[x[1]],set(dic_itens.values()))])
    
    ###Cálculo do erro MSE global.
    erro = dfTeste.map(lambda x : (x[-1],mse(x[3],x[-1],x[2],beta))).reduceByKey(lambda x,y : x +y).map(lambda x : x[1]).sum()/quantidade
        
    return erro