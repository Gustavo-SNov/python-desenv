import pandas as pd
from datetime import datetime


class Service:
   
  def __init__(self):
    pass 
   
  def retornaRelatorio962(self, pathRelatorio):
    dfRelatorio = pd.read_excel(pathRelatorio,header=5)
    self.exibeDataframe(dfRelatorio,"RELATÓRIO 962")
    return dfRelatorio

  # Função para filtrar e transformar o DataFrame
  def retornaTabelaDoRel962(self,df, tabela, intervalo={"INICIO": "", "FIM": ""}):
      # Filtrar linhas com base no valor de 'TABELA'
      if (intervalo["INICIO"] == "" and intervalo["FIM"] == ""):
         df_filtrado = df.loc[df['TABELA'].str.contains(tabela,case=False,na=False)]
      else:   
        df_filtrado = df.loc[df['TABELA'].str.contains(tabela,case=False,na=False), intervalo["INICIO"]:intervalo["FIM"]]

      # Transformar as colunas em formato estruturado
      df_transformado = df_filtrado.apply(
          lambda row: {col.split(": ")[0]: col.split(": ")[1] for col in row if ": " in str(col) }, axis=1
      ).apply(pd.Series)

      # Explicação .apply()
      # Para cada valor -> (col) da linha -> (row) se essa valor -> (col) possuir ": "
      df_transformado.reset_index(level=None, drop=True, inplace=True)
      self.exibeDataframe(df_transformado,tabela)
      return df_transformado

  def geraPlanilhaComTabelas(self,path, dfRelatorio, tabelas=[]):

    path = path + r"/tabelasRel962.xlsx"
    with pd.ExcelWriter(path) as writer:
        for tabela in tabelas:
          df = self.retornaTabelaDoRel962(df=dfRelatorio,tabela=tabela)
          df.to_excel(writer, sheet_name=tabela,index=False)


  def exibeDataframe(self, dataFrame, nomeTabela):
      print(f"{nomeTabela.upper()}: \n", dataFrame)
      print("\n------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")

  
  def formataData(self,strData):
      # Define o formato da string
      formato = "%d/%m/%Y"  
    
      # String para converter
      data_string = "{}/{}/{}".format(strData.day,strData.month,strData.year)

      # Converter para um objeto datetime
      data = datetime.strptime(data_string, formato)

      return data
  
  def formataDadosParaInsert(self,valor):
    if isinstance(valor, str):
        return f"'{valor}'"
    elif isinstance(valor, datetime):
        valor = valor.strftime("%d/%m/%Y")
        return f"TO_DATE('{valor}', 'dd/mm/yyyy')"
    elif isinstance(valor, float):
        return "{:.2f}".format(valor)
    elif isinstance(valor, int):
        return f"{str(valor)}"
  
  def retornaInserts(self, nomeTabela, dataFrame):
    inserts = []

    insert = f"\tINSERT INTO KIPREV.{nomeTabela} ({', '.join(dataFrame.columns)})\n"

    for index,row in dataFrame.iterrows():
        values = ', '.join([self.formataDadosParaInsert(value) for value in row ])
        temp = insert + f"\tVALUES({values});\n"
        inserts.append(temp)
    
    return inserts
  
  def converter_acentos_html_com_entidades(self,texto):
    
    acentos_html = {'á': '&aacute;', 'à': '&agrave;', 'ã': '&atilde;', 'â': '&acirc',
                  'Á': '&Aacute;', 'À': '&Agrave;', 'Ã': '&Atilde;',
                  'é': '&eacute;', 'É': '&Eacute;', 'ê': '&ecirc;',
                  'Ê': '&Ecirc;', 'ç': '&ccedil;', 'õ': '&otilde;',
                  '°': '&ordm'
      }
    
    for acento, entidade in acentos_html.items():
      if acento in texto:
          texto = texto.replace(acento, entidade)
    return texto