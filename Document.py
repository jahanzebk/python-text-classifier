from nltk import FreqDist

class Document():
    def __init__(self, title, content):
        self.title = title
        self.content = content
        self.category = ''
        self.words = []          # List of unique words (each word only once)
        self.freqDist = '' 
        self.features = {}         
        
    def nbPrepare(self):
        self.content = self.content.lower()
        wordList = [w.lower() for w in self.content.split() if len(w) > 2]
        self.freqDist = FreqDist(wordList)
        self.words = self.freqDist.keys()
        
        docWordSet = set(self.content)
        for word in self.words:
            self.features["contains(%s)" % word]  = (word in docWordSet)
       
        