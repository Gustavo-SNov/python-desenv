import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
from   dataSetView import DataSetView 


caminho = r'projeto_LPG1\dados\All_Pokemon.csv'

dataSetView = DataSetView()
dataSetDTO = dataSetView.carregaArquivo(caminho)   
dataSetView.exibeInfoDataSet(dataSetDTO=dataSetDTO)


#print('------------------------------------------------------------'*5,'\n')
dataSetView.buscaPorNumero(numPoke=1)

print(dataSetDTO[['Catch Rate','Legendary']])
#rint('------------------------------------------------------------'*5,'\n')
#dataSetView.buscaPorTipo('Grass')

#print('------------------------------------------------------------'*5,'\n')
#dataSetView.buscaPorNome('Bul')

#dataSetView.analiseQuantidadeTipos()

