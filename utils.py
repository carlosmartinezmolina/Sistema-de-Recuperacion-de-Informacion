

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

def truncate(number,n):
    return float(int(number * (10**n)) / (10**n))

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
    first = -1
    last = -1
    numberDocument = 0
    for item in lines:
        temp = turnLineToWords(item)
        if documentId(temp):
            documentWordList = sumDict(documentWordList,temp)
        elif temp.get('.I') != None:
            numberDocument = int(list(temp)[1])
            if first == -1:
                first = numberDocument
                last = first
            if numberDocument != first:
                documentList.append((last,documentWordList))
                last = numberDocument
                documentsWords = sumDictTerms(documentsWords,documentWordList)
                documentWordList = {}
    if documentWordList != None:
        documentList.append((numberDocument,documentWordList))
        documentsWords = sumDictTerms(documentsWords,documentWordList)
    return documentsWords , documentList

def printRank(rankList):
    for item in rankList:
        for element in item:
            if element[2] < 5:
                print(str(element[0]) + ' ' + str(element[1]) + ' ' + str(element[2]))