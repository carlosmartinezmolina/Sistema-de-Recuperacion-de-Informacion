import math

def truncate(number,n):
    return float(int(number * (10**n)) / (10**n))

def turnLineToWords(line):
    wordList = {}
    word = ''
    for item in line:
        if (item == ' ' or item == '\n') and len(word) > 0:
            if wordList.get(word) == None:
                wordList[word] = 1
            else:
                wordList[word] += 1
            word = ''
        elif item != ' ':
            word += item
    if len(word) > 0:
        if wordList.get(word) == None:
            wordList[word] = 1
        else:
            wordList[word] += 1
    return wordList

def sumDict(d1,d2):
    for k in d2:
        if d1.get(k) == None:
            d1[k] = d2[k]
        else:
            d1[k] += d2[k]
    return d1

def sumDictTerms(d1,d2):
    for k in d2:
        if d1.get(k) == None:
            d1[k] = 1
        else:
            d1[k] += 1
    return d1

def documentId(d):
    if len(d) == 2 and d.get('.I') != None:
        return False
    if len(d) == 1 and (d.get('.T') != None or d.get('.A') != None or d.get('.B') != None or d.get('.W') != None):
        return False
    return True

def readDocument(url):
    doc = open(url,"r")
    lines = doc.readlines()
    doc.close()
    documentWordList = {}
    documentsWords = {}
    documentList = []
    for item in lines:
        temp = turnLineToWords(item)
        if documentId(temp):
            documentWordList = sumDict(documentWordList,temp)
        elif temp.get('.I') != None and int(list(temp)[1]) > 1:
            documentList.append((int(list(temp)[1]) - 1,documentWordList))
            documentsWords = sumDictTerms(documentsWords,documentWordList)
            documentWordList = {}
            #Estas lineas comentadas limitan la cantidad de documentos analizados
            #if int(list(temp)[1]) > 2:
            #    break
    if documentWordList != None:
        documentList.append((len(documentList) + 1,documentWordList))
        documentsWords = sumDict(documentsWords,documentWordList)
    return documentsWords , documentList

def weightVector_tf(document):
    weightVector = {}
    max_freq = -1
    value = 0
    for item in document:
        if document[item] > max_freq:
            max_freq = document[item]
        weightVector[item] = document[item]
    for item in weightVector:
        weightVector[item] = truncate(weightVector[item]/max_freq,5)
    return weightVector

def matrix_tf(documentList,documentsWords):
    matrix = []
    for item in documentList:
        row = weightVector_tf(item[1])
        matrix.append(row)
    return matrix

def weightVector_idf(documentList,documentsWords):
    weightVector = {}
    amountDocCollection = len(documentList)
    for item in documentsWords:
        weightVector[item] = truncate(math.log10(amountDocCollection/documentsWords[item]),5)
    return weightVector

def documentWeight(url):
    matrix_w = []
    documentsWords ,documentList = readDocument(url)
    tf = matrix_tf(documentList,documentsWords)
    idf = weightVector_idf(documentList, documentsWords)
    for i in range(len(tf)):
        matrix_w.append([])
        for j in idf:
            if tf[i].get(j) == None:
                matrix_w[i].append((j,0))
            else:
                term = tf[i][j]
                matrix_w[i].append((j,truncate(term*idf[j],2)))
    return matrix_w

def printMatrix(matrix):
    for i in matrix:
        for j in i:
            print("\t",j[0],end=" ")
        break
    print()
    c = 1
    for item in matrix:
        print('d' + str(c),end="")
        for element in item:
            print("\t",element[1],end=" ")
        print()
        c += 1

def queryWeight(url,a=0.5):
    matrix_w = []
    querysWords ,queryList = readDocument(url)
    tf = matrix_tf(queryList,querysWords)
    idf = weightVector_idf(queryList, querysWords)
    for i in range(len(tf)):
        matrix_w.append([])
        for j in idf:
            if tf[i].get(j) == None:
                matrix_w[i].append((j,0))
            else:
                term = tf[i][j]
                matrix_w[i].append((j,truncate(term*idf[j],2)))
    return matrix_w

def similitud(vectorQuery,vectorDocument):
    numerador = 0
    normaQuery = 0
    normaDocument = 0
    for i in range(len(vectorQuery)):
        numerador += vectorQuery[i][1] * vectorDocument[i][1]
        normaQuery += vectorQuery[i][1]**2
        normaDocument += vectorDocument[i][1]**2
    return numerador/math.sqrt(normaQuery) * math.sqrt(normaDocument)

def main():
    urlQuery = 'collections/cran.qry'
    urlDocument = 'collections/cran.txt'

    dw = documentWeight(urlDocument)
    qw = queryWeight(urlQuery)
    
    #r = similitud(dw[0],qw[0])
    #print(r)

if __name__ == '__main__':
    main()