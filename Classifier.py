# 100 documents take about 600 MB RAM
from nltk import NaiveBayesClassifier, classify, FreqDist
import pickle
import FileHandler as FH
import Document as Doc

class Classifier():
    def nbTrain(self, trainDir):
        myFH = FH.FileHandler()
        docs = myFH.loadDirs(trainDir, True)
        
        print "Extracting Features..."
        [doc.nbPrepare() for doc in docs]
        featureSet = [(doc.features, doc.category) for doc in docs]
        del(docs)
        print "Deleted Docs"
        classifier = NaiveBayesClassifier.train(featureSet)
        del(featureSet)
        print "Deleted Features"
        print "Classifier Trained."
        
#         print "Creating .pickle file..."
#         f = open('my_classifier.pickle', 'wb')
#         pickle.dump(classifier, f)
#         f.close()
#         print "Created .pickle file"
#          
        return classifier
    
    def nbLoadTrainer(self, file = "my_classifier.pickle"):
        print "Loading Classifier.."
        
        f = open(file)
        classifier = pickle.load(f)
        f.close()
        
        print "Classifier Loaded."
        return classifier

    def getFeatures(self, document, all_words):
        document_words = set(document) 
        features = {}
        for word in all_words:
            features['contains(%s)' % word] = (word in document_words)
        return features
    
    def nbSentiTrain(self):
        from nltk.corpus import movie_reviews
        
        print "Extracting features.."
        documents = [(list(movie_reviews.words(fileid)), category)
        for category in movie_reviews.categories()
        for fileid in movie_reviews.fileids(category)]
        
        documents = documents[1800:]
        print len(documents)
        
        all_words = FreqDist(w.lower() for w in movie_reviews.words()).keys()
         
        print "Extracting features...."
         
         
        featuresets = [(self.getFeatures(d, all_words), c) for (d,c) in documents]
        
        from random import shuffle
        shuffle(featuresets)
        
        train_set, test_set = featuresets[100:], featuresets[:100]
        classifier = NaiveBayesClassifier.train(train_set)
        print classify.accuracy(classifier, test_set)
        classifier.show_most_informative_features(10)
        
        
        #classifier = NaiveBayesClassifier.train(featureSet)
        print "Classifier Trained."
        

    