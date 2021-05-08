from utils import turnLineToWords

def Recuperados(rank):
    recuperadosRelevantes = 0
    recuperadosIrrelevantes = 0
    for item in rank:
        for element in item:
            if element[2] < 5:
                recuperadosRelevantes += 1
            else:
                recuperadosIrrelevantes += 1
    return recuperadosRelevantes,recuperadosIrrelevantes

def NoRecuperados(url,recuperados,norecuperados):
    doc = open(url,"r")
    lines = doc.readlines()
    doc.close()
    recuperadosList = []
    for item in lines:
        temp = turnLineToWords(item)
        temp = list(temp.items())
        recuperadosList.append((int(temp[0][0]),int(temp[1][0])))
    lenTemp = len(recuperadosList)
    for item in recuperados:
        for element in item:
            temp = (element[0],element[1])
            try:
                recuperadosList.remove(temp)
            except:
                pass
    noRecuperadosRelevantes = len(recuperadosList)
    noRecuperadosIrrelevantes = norecuperados - lenTemp
    return noRecuperadosRelevantes, noRecuperadosIrrelevantes
        
def Precision(RR,RI):
    return RR/(RR+RI)

def Recobrado(RR,NR):
    return RR/(RR+NR)

def Medida_F(precision,recobrado,beta=1):
    return (1 + beta**2)/(1/precision + (beta**2)/recobrado)

def Medida_F1(precision,recobrado):
    return 2/(1/precision + 1/recobrado)