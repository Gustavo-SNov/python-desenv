
import pandas as pd
from datetime import datetime

from saneamentos.portabilidadeSaneamento import PortabilidadeSaneamento
from saneamentos.service import Service

service = Service()

def saneamentoHistPortabilidade(path, numPortabilidade, side=False):
    portabilidadeSaneamento = PortabilidadeSaneamento(path=path,side=side)

    pathRelatorio = path + r"/REL_962_DADOS_CERTIFICADO" + f"_{numPortabilidade}.xlsx"

    dfRelatorio = service.retornaRelatorio962(pathRelatorio=pathRelatorio)
        
    dfportabDeta = portabilidadeSaneamento.buscaInfoPortabilidade(dfRelatorio=dfRelatorio,numPortabilidade=numPortabilidade)

    portabMovtos = portabilidadeSaneamento.retornaPortabMovtos(dfRelatorio=dfRelatorio ,dfPortabDeta=dfportabDeta)

    portabilidade = portabilidadeSaneamento.validaNovaPortab(dfRelatorio, dfportabDeta, portabMovtos)

    inserts = service.retornaInserts(nomeTabela="FO_PORTAB_MOVTOS", dataFrame=portabMovtos)

    portabilidadeSaneamento.geraScript(inserts=inserts,portabDeta=dfportabDeta, dfRelatorio=dfRelatorio)

    return portabilidade


path = r"automaDados/dados/teste"
numPortabilidade = "040310000273791"
portabilidadeResultado = saneamentoHistPortabilidade(path=path, numPortabilidade=numPortabilidade, side=False)


