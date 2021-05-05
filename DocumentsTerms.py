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
    documentList = []
    for item in lines:
        temp = turnLineToWords(item)
        if documentId(temp):
            documentWordList = sumDict(documentWordList,temp)
        elif temp.get('.I') != None and int(list(temp)[1]) > 1:
            documentList.append((int(list(temp)[1]) - 1,documentWordList))
            documentWordList = {}
            #Estas lineas comentadas limitan la cantidad de documentos analizados
            #if int(list(temp)[1]) > 2:
            #    break
    if documentWordList != None:
        documentList.append((len(documentList) + 1,documentWordList))
    return documentList

def main():
    url = 'collections/cran.txt'
    result = readDocument(url)
    
    for i in result:
        print(i[0])
        print(i[1])
        print()
    print(len(result))
if __name__ == '__main__':
    main()