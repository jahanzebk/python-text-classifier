# 100 documents take about 600 MB RAM
from nltk import NaiveBayesClassifier, classify, FreqDist
import FileHandler as FH
import Document as Doc
from TextProcessor import TextProcessor as TP

from sklearn.naive_bayes import MultinomialNB


class Classifier():
    def SK_NB_train(self, trainDir):
        myFH = FH.FileHandler()
        docs = myFH.loadDirs(trainDir, True)
        
        print "Extracting Features..."
        docCats = [doc.category for doc in docs]
        uniqueCats = self.uniqify(docCats)
        [tfidfVec, tfidfs] = TP.SK_NB_calcTFIDFs(docs, True, False)
        
        del(docs)
        
        clf = MultinomialNB(fit_prior=False)
        clf.fit(tfidfs, docCats)
        print "Classifier trained."
        
        
        self.SK_NB_accuracy(clf, tfidfVec, None, False, True, uniqueCats)
        save = raw_input("Would you like to pickle (save) classifier and TFIDFs? (y|n): ")
        
        if (save == 'y'):
            from sklearn.externals import joblib
            print "Writing Classifier to file."
            joblib.dump(clf, "pickles/SK_classifier.pkl")
            del(clf)
            
            print "Writing TFIDF pickle file."
            joblib.dump(tfidfVec, "pickles/SK_Tfidfs.pkl")
            del(tfidfVec)
        else:
            return clf
        
        
    def SK_NB_accuracy(self, clf, tfidfVec, trainDocs = None, showMistakes = False, showImpWords = False, class_labels = None):
        dir = "docs/testing/" # actual dir will be build from args (docs/userID/setID dir)
        myFH = FH.FileHandler()
        
        #Load test documents
        testDocs = myFH.loadDirs(dir, True)
        rawDocs = [doc.content for doc in testDocs]     
        docCats = [doc.category for doc in testDocs]
        tfidfs = tfidfVec.transform(rawDocs)
        
        # Clean up
        del(rawDocs)
        
        if (showMistakes):
            self.showMistakes(clf, testDocs, tfidfs, class_labels)
            
        # Clean up            
        del(testDocs)
                    
        if (showImpWords):
            self.printImpWords(tfidfVec, clf, None, class_labels, 50)
            
        print "Accuracy: ", clf.score(tfidfs, docCats) * 100
        
        # Clean up            
        del(docCats)
        
    def showMistakes(self, clf, testDocs, tfidfs, class_labels):
        for i in range(len(testDocs)):
            prediction = clf.predict(tfidfs[i])[0]
            if (testDocs[i].category != prediction):
                print testDocs[i].title
                print "Actual Class = ", testDocs[i].category
                print "Predicted Class = ", prediction
                if class_labels is not None:
                    predictions = clf.predict_proba(tfidfs[i])
                    for i in range(len(predictions)):
                        print class_labels, " : " 
                        print predictions, ", "
                print ' '

    def printImpWords(self, vectorizer, clf, trainDir = None, class_labels = None, numWords = 10):
        import numpy as np
        """Prints features with the highest coefficient values, per class"""
        print "Most important features:"
        print "..."  
        if trainDir is not None and class_labels is None:
            myFH = FH.FileHandler()
            trainDocs = myFH.loadDirs(trainDir, True)
        elif trainDir is None and class_labels is None:
            import sys
            sys.exit("Error: either pass training documents or a directory of training data or list of classes to printImpWords()")
            
        if class_labels is None: 
            class_labels = self.uniqify([doc.category for doc in trainDocs])
        feature_names = vectorizer.get_feature_names()
        for i, class_label in enumerate(class_labels):
            try:
                topWords = np.argsort(clf.coef_[i])[-numWords:]
                print class_label
                print " ".join(feature_names[j] + ", " for j in topWords)
                print " "
            except:
                pass    
    
    def NLTK_NB_train(self, trainDir):
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
    
    def NLTK_NB_LoadTrainer(self, file = "my_classifier.pickle"): #change to joblib.load andmake sure it all works
        print "Loading Classifier.."
        
#         f = open(file)
#         classifier = pickle.load(f)
#         f.close()
        
#         print "Classifier Loaded."
#         return classifier

    def NLTK_NB_getFeatures(self, document, all_words):
        document_words = set(document) 
        features = {}
        for word in all_words:
            features['contains(%s)' % word] = (word in document_words)
        return features
    
    def NLTK_NB_sentiTrain(self):
        from nltk.corpus import movie_reviews
        
        print "Extracting features.."
        documents = [(list(movie_reviews.words(fileid)), category)
        for category in movie_reviews.categories()
        for fileid in movie_reviews.fileids(category)]
        
        documents = documents[1800:]
        print len(documents)
        
        all_words = FreqDist(w.lower() for w in movie_reviews.words()).keys()
         
        print "Extracting features...."
         
         
        featuresets = [(self.NLTK_NB_getFeatures(d, all_words), c) for (d,c) in documents]
        
        from random import shuffle
        shuffle(featuresets)
        
        train_set, test_set = featuresets[100:], featuresets[:100]
        classifier = NaiveBayesClassifier.train(train_set)
        print classify.accuracy(classifier, test_set)
        classifier.show_most_informative_features(10)
        
        
        #classifier = NaiveBayesClassifier.train(featureSet)
        print "Classifier Trained."
        
#         HELPER FUNCTIONS

    def uniqify(self, seq, idfun=None): 
       # order preserving
       if idfun is None:
           def idfun(x): return x
       seen = {}
       result = []
       for item in seq:
           marker = idfun(item)
           # in old Python versions:
           # if seen.has_key(marker)
           # but in new ones:
           if marker in seen: continue
           seen[marker] = 1
           result.append(item)
       return result
        

    