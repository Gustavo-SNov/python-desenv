import pandas as pd

class DataSet:

    def __init__(self):
        self.dataSet = None

    def carregarDataSet(self, arquivo):
        self.dataSet = arquivo
        return self.dataSet
    
    def getDataset(self):
        return self.dataSet
    
    def getPorNome(self,nome):
        return self.dataSet[self.dataSet['Name'].str.contains(nome,case=False,na=False)]

    def getPorNumero(self,numPoke):
        return self.dataSet[self.dataSet.Number == numPoke]
    
    def getPorTipo(self,tipo):
        return self.dataSet[(self.dataSet['Type 1'] == tipo) | (self.dataSet['Type 2'] == tipo)]
    
    def getVantagensDesvantagensPorTipo(self,tipo):
        return self.dataSet[self.dataSet['Type 2'] != None ]['Type 1']
    

 





