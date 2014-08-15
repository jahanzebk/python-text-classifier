import sys
import FileHandler as FH, Classifier, EntityExtractor as EE
from TextProcessor import TextProcessor as TP
import Document as Doc
from nltk import classify
from sklearn.externals import joblib
from sklearn.naive_bayes import MultinomialNB

def main():
    # Initialize Directory paths and variables
    docsDir = "docs/"
    logFile = "log.txt"
    
    try:
        userId = sys.argv[0] # send via PHP exec()
        userDir = docsDir + userId + "/" # docs/userId/
    except IndexError:
        msg = "No User Id given."
        myFH = FH.FileHandler()
        myFH.makeLog(logFile, msg)
        sys.exit(msg)
        
    try:
        currSetId = sys.argv[0] # send via PHP exec()
        currSetDir = userDir + currSetId + "/" # docs/userId/setname/
    except IndexError:
        msg = "No Set Id given."
        myFH = FH.FileHandler()
        myFH.makeLog(logFile, msg)
        sys.exit(msg)
        #open whole set in another function
    fullAnalysis(currSetDir);  
    
def fullAnalysisOLD(currSetDir):
    dir = "docs/testing/" # actual dir will be build from args (docs/userID/setID dir)
    nbClassifier = Classifier.Classifier()
    myFH = FH.FileHandler()
    
    #nbClassifier.NLTK_NB_sentiTrain()
    
    #Load test documents
    testDocs = myFH.loadDirs(dir, True);
    [doc.nbPrepare() for doc in testDocs]
    testFeatureSet = [(doc.features, doc.category) for doc in testDocs]
          
    #Classify documents 
    #classifier = nbClassifier.nbLoadTrainer()
    classifier = nbClassifier.nbTrain('docs/training/')
       
    #print classifier.classify(testFeatureSet)
      
    print "Accuracy: "
    print classify.accuracy(classifier, testFeatureSet)
    classifier.show_most_informative_features(10)
    
    
def fullAnalysis(currSetDir):
    dir = "docs/testing/" # actual dir will be build from args (docs/userID/setID dir)
    nbClassifier = Classifier.Classifier()
    myFH = FH.FileHandler()
    
    #Load test documents
    testDocs = myFH.loadDirs(dir, True);
    
    docCats = [doc.category for doc in testDocs]
    [tfidfVec, tfidfs] = TP.SK_NB_calcTFIDFs(testDocs)
    
    print "Loading Classifier."
    clf = joblib.load("pickles/SK_classifier.pkl")
    nbClassifier.printImpWords(tfidfVec, clf, 'docs/training/', 50)
    
    for i in range(len(testDocs)):
        prediction = clf.predict(tfidfs[i])[0]
        if (testDocs[i].category != prediction):
            print testDocs[i].title
            print "Actual Class = " + testDocs[i].category
            print prediction
            print ' '
    print "Accuracy: "
    print clf.score(tfidfs, docCats)
    
      
#    todo list: make SGDClassifier, test it, 
#    then fix up NLTK classifiers make sure they work with joblib, 
#    then fit in bhais sentiment analysis
#  ================== DONE ================= also, optimize training function to write classifier pkl file, remove it from RAM, then make tfidf pkl
#  ================== DONE ================= testing function before writing both pickle files that returns accuracy and confirms if you want to write it
# ================== DONE ================= also check most useful features of the classifier and check how useful game of thrones is as a feature
 #     also, crawl for seperate test data and document code
#     figure out with partial_fit 
#     a classify_unlabelled function that will run for the acutal app


if (__name__ == "__main__"):
    main()