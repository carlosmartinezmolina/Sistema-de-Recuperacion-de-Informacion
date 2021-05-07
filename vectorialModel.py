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
        documentsWords = sumDictTerms(documentsWords,documentWordList)
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
    documentsWords ,documentList = readDocument(url)
    tf = matrix_tf(documentList,documentsWords)
    idf = weightVector_idf(documentList, documentsWords)
    return makeMatrix(tf,idf,lambda x , y : x * y)

def makeMatrix(tf,idf,lambdaFunc):
    matrix_w = []
    for i in range(len(tf)):
        temp = {}
        for j in idf:
            if tf[i].get(j) != None:
                term = tf[i][j]
                temp[j] = truncate(lambdaFunc(term,idf[j]),2)
        matrix_w.append(temp)
    return matrix_w

# def printMatrix():
    # for i in matrix:
    #     for j in i:
    #         print("\t",j[0],end=" ")
    #     break
    # print()
    # c = 1
    # for item in matrix:
    #     print('d' + str(c),end="")
    #     for element in item:
    #         print("\t",element[1],end=" ")
    #     print()
    #     c += 1

def queryWeight(url,a=0.4):
    querysWords ,queryList = readDocument(url)
    tf = matrix_tf(queryList,querysWords)
    idf = weightVector_idf(queryList, querysWords)
    return makeMatrix(tf,idf, lambda x , y : y*((a + (1-a)*x)))

def similitud(vectorQuery,vectorDocument):
    numerador = 0
    normaQuery = 0
    normaDocument = 0
    for item in vectorQuery:
        if vectorDocument.get(item) != None:
            numerador += vectorQuery[item] * vectorDocument[item]
        normaQuery += vectorQuery[item]**2
    for item in vectorDocument:
        normaDocument += vectorDocument[item]**2
    return numerador/(math.sqrt(normaQuery) * math.sqrt(normaDocument))

def rank(queryWeight,documentWeight):
    resultRank = []
    cquery = 0
    for item in queryWeight:
        cquery += 1
        cdocument = 0
        temp = []
        if len(item) > 0:
            for element in documentWeight:
                cdocument += 1
                if len(element) == 0:
                    break
                sim = truncate(similitud(item,element),2)
                temp.append((cquery,cdocument,sim))
            temp.sort(key=lambda x:x[2],reverse=True)
        resultRank.append(temp)
    return resultRank

def printRank(rankList):
    for item in rankList:
        for element in item:
            print(str(element[0]) + ' ' + str(element[1]) + ' ' + str(element[2]))

def main():
    urlQuery = 'collections/cran.qry'
    urlDocument = 'collections/cran.txt'

    dw = documentWeight(urlDocument)
    qw = queryWeight(urlQuery)
    
    r = rank(qw,dw)
    printRank(r)

if __name__ == '__main__':
    main()