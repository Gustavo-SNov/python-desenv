#importando a biblioteca sqlite3
import sqlite3
import pandas as pd
from   model.dataSet import DataSet

#  dataSetService => Controller + DAO
class DataSetService:

    def __init__(self):
        self.dataSet = DataSet()

    def defineLeitura(self,fileHandler, extensionFile):
        tiposArquivo = ['txt', 'xlsx','csv']

        if extensionFile == tiposArquivo[0]:
            with open(fileHandler, 'r') as txtExtension:
                arquivo = txtExtension.read()
        elif extensionFile == tiposArquivo[1]:
            arquivo = pd.read_excel(fileHandler, header=3)
        elif extensionFile == tiposArquivo[2]:
            arquivo = pd.read_csv(fileHandler)
        else: 
            return -1
        

        return self.dataSet.carregarDataSet(arquivo)
    
    def exportaDataSet(self,dataSet,extensionFile):
        path = r'projeto_LPG1\dados\dataSetPokemon.'

        if extensionFile == self.tiposArquivo[0]:
            path = path + self.tiposArquivo[0]
            with open(path, 'w') as txtExtension:
                txtExtension.write(dataSet.to_string())

        elif extensionFile == self.tiposArquivo[1]:
            path = path + self.tiposArquivo[1]
            dataSet.to_excel(path)

        elif extensionFile == self.tiposArquivo[2]:
            path = path + self.tiposArquivo[2]
            dataSet.to_csv(path)

        else:
            return True

        return False
  
    def buscaPorNome(self,nome):
        dataSetDTO = self.dataSet.getPorNome(nome=nome)
        return dataSetDTO

    def buscaPorNumero(self,numPoke):
        buscaPoke = self.dataSet.getPorNumero(numPoke=numPoke)
        return buscaPoke

    def buscaPorTipo(self,tipo):
        dataSetDTO = self.dataSet.getPorTipo(tipo=tipo)
        return dataSetDTO

#dataSet = u.handlerUserFile()


# Criando uma conexão com o Banco de Dados
def getConnectionDB(nomeBancoDeDados):
    return sqlite3.connect(nomeBancoDeDados + '.db')

def exibeColunasSQL(nomeBancoDeDados, connectionDB):
    # Comando SQL é usado para obter informações sobre a estrutura de uma tabela no SQLite.
    query = "PRAGMA table_info(" + nomeBancoDeDados + ");"

    colunas = pd.read_sql_query(query, connectionDB)

    # Filtro para Exibir nome e tipo das colunas
    return colunas[['nome','tipo']]

# INSERT
def criaNovoRegistro(nomeBancoDeDados, cursor, valores):
    sqlCommand = 'INSERT INTO ' + nomeBancoDeDados 
    sqlValues = ' VALUES();'
    sqlInsert = sqlCommand + sqlValues

    cursor.execute(sqlInsert)
    cursor.commit()

# SELECT 
def consultaInfoPokemon(connectionDB):
    query = ''' 
    SELECT Number, Name, Type 1, Type 2
    FROM   PROJETO_SPOLPG1_GRUPO_3
    ORDER BY Number DESC
    LIMIT 10;
    '''    
    top_pokes = pd.read_sql_query(connectionDB)
    print(top_pokes)

def alteraPokemon(cursor,connectionDB):
    sqlUpdate01 = 'UPDATE PROJETO_SPOLPG1_GRUPO_3'
    sqlUpdate02 = 'SET ' 
    sqlUpdate03 = 'WHERE '
    upd = sqlUpdate01 + sqlUpdate02 + sqlUpdate03
    cursor.execute(upd)
    connectionDB.commit()
    query = ''' 
    SELECT Number, Name, Type 1, Type 2
    FROM   PROJETO_SPOLPG1_GRUPO_3 
    WHERE  Number = '' 
    '''
    updated_poke = pd.read_sql_query(query,connectionDB)
    print(updated_poke)

def deletePokemon(cursor, connectionDB, predicate):
    sqlDelete = 'DELETE FROM PROJETO_SPOLPG1_GRUPO_3' + predicate
    cursor.execute(sqlDelete)
    connectionDB.commit()
    query = ''' 
    SELECT Number, Name, Type 1, Type 2
    FROM   PROJETO_SPOLPG1_GRUPO_3  
    ''' + predicate
    delete_poke = pd.read_sql_query(query,connectionDB)
    if delete_poke.empty: 
        print("\nPokemon deletado com sucesso!\n")
        return
    
    print("\nErro ao tentar deletar o pokemon.\n")