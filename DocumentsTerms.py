def turnLineToWords(line):
    wordList = []
    word = ''
    for item in line:
        if (item == ' ' or item == '\n') and len(word) > 0:
            wordList.append(word)
            word = ''
        elif item != ' ':
            word += item
    if len(word) > 0:
        wordList.append(word)
    return wordList

def readDocument(url):
    doc = open(url,"r")
    lines = doc.readlines()
    doc.close()
    documentWordList = []
    for item in lines:
        documentWordList = documentWordList + turnLineToWords(item)
    return documentWordList

def main():
    url = 'collections/testCollection.txt'
    readDocument(url)

if __name__ == '__main__':
    main()