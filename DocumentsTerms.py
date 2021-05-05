import math

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
            documentsWords = sumDict(documentsWords,documentWordList)
            documentWordList = {}
            #Estas lineas comentadas limitan la cantidad de documentos analizados
            #if int(list(temp)[1]) > 2:
            #    break
    if documentWordList != None:
        documentList.append((len(documentList) + 1,documentWordList))
        documentsWords = sumDict(documentsWords,documentWordList)
    return documentsWords , documentList

def weightVector_tf(document,wordList):
    weightVector = {}
    max_freq = -1
    value = 0
    for item in wordList:
        if document.get(item) != None:
            weightVector[item] = document[item]
            if document[item] > max_freq:
                max_freq = document[item]
        else:
            weightVector[item] = 0
    for item in weightVector:
        weightVector[item] = weightVector[item]/max_freq
    return weightVector

def matrix_tf(documentList,documentsWords):
    matrix = []
    for item in documentList:
        row = weightVector_tf(item[1],documentsWords)
        matrix.append(list(row.items()))
    return matrix

def amount_doc_appear_term_i(documentList,termino):
    result = 0
    for item in documentList:
        if item[1].get(termino):
            result += 1
    return result

def weightVector_idf(documentList,documentsWords):
    weightVector = {}
    amountDocCollection = len(documentList)
    for item in documentsWords:
        weightVector[item] = math.log10(amountDocCollection/amount_doc_appear_term_i(documentList,item))
    return weightVector

def matrix_w_ij(documentList,documentsWords):
    matrix_w = []
    tf = matrix_tf(documentList,documentsWords)
    idf = weightVector_idf(documentList, documentsWords)
    for i in range(len(tf)):
        matrix_w.append([])
        for j in range(len(idf)):
            term = tf[i][j][0]
            matrix_w[i].append((term,tf[i][j][1]*idf[term]))
    return matrix_w

def main():
    url = 'collections/cran.txt'
    documentsWords ,documentList = readDocument(url)
    r = matrix_w_ij(documentList,documentsWords)
    print(r)

if __name__ == '__main__':
    main()