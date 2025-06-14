import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from   controller.dataSetService import DataSetService  
from   model.dataSet    import DataSet

class DataSetView: 

    def __init__(self):
        self.service = DataSetService()
        self.dataSetDTO = DataSet()
        

    #  ------------------------------- [Export/Import de Dados] ------------------------------- 
    def carregaArquivo(self,caminho):
        arquivo = caminho.split('\\')[-1] 
        extensao = caminho.split('.')[-1]
        print(arquivo,extensao)
        self.dataSetDTO = self.service.defineLeitura(caminho,extensao)
        return self.dataSetDTO
        #print(self.dataSetDTO)
      
    def exportaDataSet(self,dataSet,extensionFile):
        result = self.service.exportaDataSet(dataSet=dataSet,extensionFile=extensionFile)
        if(result):
          print("Erro durante Exportação")
          return
        print("DataSet exportado com sucesso!")   

    def exibeInfoDataSet(self, dataSetDTO):
        #pd.set_option('display.max_columns', 25)
        pd.set_option('display.width', 1000)
        # Visualizar as colunas do dataset
        print("\nColunas do dataset:")
        print(dataSetDTO.columns)

        # Obter informações gerais sobre o dataset
        print("\nInformações gerais do dataset:")
        print(dataSetDTO.info())

        # Descrever estatísticas básicas
        print("\nEstatísticas básicas do dataset:")
        print(dataSetDTO.describe())

        # Visualizar as primeiras linhas do dataset
        print("Primeiras linhas do dataset:")
        print(dataSetDTO.head())

    #  ------------------------------- [CONSULTAS] -------------------------------
    def buscaPorNome(self,nome):
        self.dataSetDTO = self.service.buscaPorNome(nome=nome)
        print(self.dataSetDTO)

    def buscaPorNumero(self,numPoke):
        buscaPoke = self.service.buscaPorNumero(numPoke=numPoke)
        print(buscaPoke)

    def buscaPorTipo(self,tipo):
        self.dataSetDTO = self.service.buscaPorTipo(tipo=tipo)
        print(self.dataSetDTO)

    def buscaMaiorStatus(self):
        filtroMaior = self.dataSetDTO['BST'].max()
        maiorStatus = self.dataSetDTO[self.dataSetDTO['BST'] == filtroMaior]
        print(maiorStatus)

    def consultaDinamica():
        print()

    #  ------------------------------- [EDA] -------------------------------  
    # 1. Montar a base do Gráfico -> 2. Busca os dados -> 3. Insere as Informações  -> 4. Exibe
    def formatarTexto(self,pct, allvals):
        absolute = int(np.round(pct/100.*np.sum(allvals)))
        return f"{pct:.1f}%\n({absolute:d})"
    
    def analiseGenPokemon():
        print()
    
    def analiseAtributos():
        print()

    def analiseQuantidadeTipos(self):
        self.dataSetDTO = self.service.buscaDataSet()
        fig, ax = plt.subplots(figsize=(8, 7), subplot_kw=dict(aspect="equal"))

        dataSetTotal = self.dataSetDTO.value_counts("Type 1") + self.dataSetDTO.value_counts("Type 2")
        dataSetTotal = dataSetTotal.to_frame().reset_index()
        dataSetTotal.columns = ['Tipo','Total']
        print(dataSetTotal)

        wedges, texts, autotexts = ax.pie(dataSetTotal['Total'], autopct=lambda pct: self.formatarTexto(pct, dataSetTotal['Total']),
                                          textprops=dict(color="w"))

        ax.legend(wedges, dataSetTotal['Tipo'],
                  title="Tipos",
                  loc="center left",
                  bbox_to_anchor=(1, 0, 0.5, 1))

        plt.setp(autotexts, size=8, weight="bold")

        ax.set_title('Quantidade de Pokemons Por Tipo')
        plt.show()

    def analiseCatchRate():
        print()

    def analiseExpToMax():
        print()

    #  ------------------------------- [DML] -------------------------------
    def criaNovoPokemon():
        print()

    def alteraPokemon():
        print()
    
    def removePokemon():
        print()


caminho = r'projeto_LPG1\dados\All_Pokemon.csv'

dataSetView = DataSetView()
dataSetDTO = dataSetView.carregaArquivo(caminho)   
dataSetView.exibeInfoDataSet(dataSetDTO=dataSetDTO)

