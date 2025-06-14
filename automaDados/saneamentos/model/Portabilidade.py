import pandas as pd
    
class Portabilidade:

    def __init__(self,portabSolic,portabDeta,portabMovtos):
        self.portabSolic = portabSolic 
        self.portabDeta = portabDeta 
        self.portabMovtos = portabMovtos

    def getPortabSolic(self):
        return self.portabSolic
    
    def getPortabDeta(self):
        return self.portabDeta
    
    def getPortabMovtos(self):
        return self.portabMovtos
    
    def setPortabSolic(self, portabSolic):
        self.portabSolic = self.portabSolic
    
    def setPortabDeta(self, portabDeta):
        self.portabDeta = self.portabDeta
    
    def setPortabMovtos(self, portabMovtos):
        self.portabMovtos = self.portabMovtos