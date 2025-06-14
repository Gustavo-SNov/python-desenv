import pandas as pd
from datetime import datetime
from saneamentos.service import Service
from saneamentos.model.Portabilidade import Portabilidade

class PortabilidadeSaneamento:

    def __init__(self,path,side=False):
        self.service = Service()
        self.path = path
        self.side = side

    def buscaInfoPortabilidade(self, dfRelatorio,numPortabilidade):
        portabDeta = self.service.retornaTabelaDoRel962(df=dfRelatorio,tabela="FO_PORTAB_DETALHE",intervalo={"INICIO": "COL01", "FIM": "COL10"})
        portabDeta = portabDeta[portabDeta["NUM_PORTABILIDADE"] == numPortabilidade]
        portabDeta.reset_index(level=None, drop=True, inplace=True)
        return portabDeta

    def retornaHistoricoPortabilidade(self, numPortabilidade):
        dfHistorico = None
        pathHistPortab = self.path + r"/hist_portab" + f"_{numPortabilidade}"

        if self.side:
            pathHistPortab = pathHistPortab + ".txt"
            with open(pathHistPortab, 'r') as arquivo:
                for linha in arquivo:
                    print(linha)
                    linha = linha.strip()   # remove caracteres de nova linha (\n) no início e no fim
                    if (len(linha) == 63):
                        dfHistorico = dfHistorico._append({ 'TIP_LANCAMENTO': str(int(linha[23:25])),#"{:.0f}".format(int(linha[23:25])), 
                                                    'DATA_LANCAMENTO':  datetime.strptime(linha[25:33], "%Y%m%d"),
                                                    'VLR_HISTORICO': int(linha[33:48])/100, 
                                                    'VLR_ATUALIZADO': int(linha[48:63])/100 }, 
                                                    ignore_index=True)
                        
        else:
            pathHistPortab = pathHistPortab + ".xlsx"
            dfHistorico = pd.read_excel(pathHistPortab,header=0)
            dfHistorico = dfHistorico.loc[: , ['TIP_LANCAMENTO', 'DATA_LANCAMENTO', 'VLR_HISTORICO', 'VLR_ATUALIZADO']]
            dfHistorico.columns = ['TIP_LANCAMENTO', 'DATA_LANCAMENTO', 'VLR_HISTORICO', 'VLR_ATUALIZADO']
        
        return dfHistorico

    def tipLancamento(self, x):
        x = str(x).strip()
        x.capitalize();    
        if (x == "Contribuição Regular"):
            return '1'
        elif (x == "Aporte Esporádico"):
            return '2'
        elif (x == "Portabilidade"):
            return '3'
        elif (x == "Excedente Financeiro"):
            return '4'
        elif (x == "Contribuição Empresa"):
            return '5'
        elif (x == "Fundo Fechado"):
            return '94'
        else:
            return x
        
    def retornaPortabMovtos(self,dfRelatorio ,dfPortabDeta):
        dfPortabMovtos = self.service.retornaTabelaDoRel962(df=dfRelatorio,tabela="FO_PORTAB_MOVTOS",intervalo={"INICIO": "COL01", "FIM": "COL10"})
        dfPortabMovtos = dfPortabMovtos.drop(index=dfPortabMovtos.index)

        dfHistorico = self.retornaHistoricoPortabilidade(numPortabilidade=dfPortabDeta.at[0,"NUM_PORTABILIDADE"])


        dfPortabMovtos["TIP_LANCAMENTO"] = dfHistorico["TIP_LANCAMENTO"].map(lambda t : self.tipLancamento(t))
        dfPortabMovtos["DATA_LANCAMENTO"] = dfHistorico["DATA_LANCAMENTO"].map(lambda  d: self.service.formataData(d))
        dfPortabMovtos["VLR_HISTORICO"] = dfHistorico["VLR_HISTORICO"]
        dfPortabMovtos["VLR_ATUALIZADO"] = dfHistorico["VLR_ATUALIZADO"]

        dfPortabMovtos["COD_EMPRESA"] = dfPortabMovtos["COD_EMPRESA"].apply(lambda x: dfPortabDeta["COD_EMPRESA"] if pd.isna(x) else x)
        dfPortabMovtos["NUM_PORTABILIDADE"] = dfPortabMovtos["NUM_PORTABILIDADE"].apply(lambda x: dfPortabDeta["NUM_PORTABILIDADE"] if pd.isna(x) else x)
        dfPortabMovtos["COD_TIPSALDO"] = dfPortabMovtos["COD_TIPSALDO"].apply(lambda x: dfPortabDeta["COD_TIPSALDO"] if pd.isna(x) else x)
        dfPortabMovtos["COD_INVERSION"] = dfPortabMovtos["COD_INVERSION"].apply(lambda x: dfPortabDeta["COD_INVERSION"] if pd.isna(x) else x)
        dfPortabMovtos["COD_OBJETIVO"] = dfPortabMovtos["COD_OBJETIVO"].apply(lambda x: dfPortabDeta["COD_OBJETIVO"] if pd.isna(x) else x)
        dfPortabMovtos["SEQ_MOVTO"] = range(1, len(dfPortabMovtos) + 1)
        
        self.service.exibeDataframe(dfPortabMovtos,"FO_PORTAB_MOVTOS")
        return dfPortabMovtos

    def buscaInfoSaidas(self, dfRelatorio,numPortabilidade):
        aportes = self.service.retornaTabelaDoRel962(df=dfRelatorio,tabela="FO_APORTES")
        aportes = aportes[aportes["NUM_DOCUMENTO"] == numPortabilidade ]
        aporte = aportes["NUM_APORTE"].apply(lambda a: int(a)).max()

        saidas = self.service.retornaTabelaDoRel962(df=dfRelatorio,tabela="FO_SAIDAS_TIPSALDOSXAPORTE",intervalo={"INICIO": "COL01", "FIM": "COL15"})
        saidas["NUM_APORTE"] = saidas["NUM_APORTE"].apply(lambda a: int(a))
        saidas = saidas[saidas["NUM_APORTE"] == aporte]

        
        codOperSaidas = saidas["COD_OPER"].drop_duplicates()
        numSaidas = saidas["NUM_SOLIC_OPER_SAIDA"].drop_duplicates()
        saidas = {
                "cod_oper": codOperSaidas.to_list(), 
                "num_documento":numSaidas.to_list()      
                }
        print(saidas)
        return saidas


    def validaNovaPortab(self, dfRelatorio,portabDeta,portabMovtos):

        portabSolic = self.service.retornaTabelaDoRel962(df=dfRelatorio,tabela="FO_PORTAB_SOLICITACAO",intervalo={"INICIO": "COL01", "FIM": "COL15"})

        portabSolic = portabSolic[portabSolic["NUM_PORTABILIDADE"] == portabDeta.at[0,"NUM_PORTABILIDADE"]]

        portabilidade = Portabilidade(portabSolic=portabSolic,portabDeta=portabDeta,portabMovtos=portabMovtos)

        totalMovtos =  portabMovtos["VLR_ATUALIZADO"].sum()
        totalSolicitado = portabDeta.at[0,"VLR_SOLICITADO"].replace(",",".")
        print(f"TOTAL VLR_ATUALIZADO: {float(totalMovtos)} - TOTAL VLR_SOLICITADO: {float(totalSolicitado)}")

        tabelas = ["FO_PORTAB_SOLICITACAO", "FO_PORTAB_DETALHE", "FO_PORTAB_MOVTOS"]
        self.service.geraPlanilhaComTabelas(path=self.path,dfRelatorio=dfRelatorio,tabelas=tabelas)


        return portabilidade
        

    def geraScript(self, inserts, portabDeta,dfRelatorio):

        pathArquivo = self.path + r"/alt_hist_portab" + f"_{portabDeta.at[0,"NUM_PORTABILIDADE"]}.txt"
        arquivo = open(pathArquivo, "w")
        codEmpresa = str(portabDeta.at[0,"COD_EMPRESA"])
        codCuenta = str(portabDeta.at[0,"COD_CUENTA"])
        numPortabilidade = str(portabDeta.at[0,"NUM_PORTABILIDADE"])

        delete = f"\tDELETE FROM KIPREV.FO_PORTAB_MOVTOS\n\tWHERE NUM_PORTABILIDADE = '{numPortabilidade}';\n\n"
        arquivo.write(delete)
        for command in inserts:

            arquivo.write(command)

        saidas = self.buscaInfoSaidas(dfRelatorio,portabDeta.at[0,"NUM_PORTABILIDADE"] )
        if saidas != None: 
            arquivo.write(f"\nIN ({', '.join([self.service.formataDadosParaInsert(value) for value in saidas["cod_oper"]])})")
            arquivo.write(f"\nIN ({', '.join([self.service.formataDadosParaInsert(value) for value in saidas["num_documento"]])})\n")
            marcacao = f"\n\tkiprev.pck_db_tmp_cria_tsa_z.p_cria_marcacao('{codEmpresa}','{codCuenta}');"
        else:
            marcacao = f"\n\tkiprev.pck_db_tmp_cria_tsa.p_cria_marcacao('{codEmpresa}','{codCuenta}');"
        arquivo.write(marcacao)
    
