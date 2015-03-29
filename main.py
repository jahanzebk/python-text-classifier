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
    test_SK_NB_classification()
    
   
   
def test_SK_NB_classification():
    dir = "docs/testing/" # actual dir will be build from args (docs/userID/setID dir)
    nbClassifier = Classifier.Classifier()
    myFH = FH.FileHandler()
    
    #Load test documents
    testDocs = myFH.loadDirs(dir, True);
    
    docCats = [doc.category for doc in testDocs]
    [tfidfVec, tfidfs] = TP.SK_NB_calcTFIDFs(testDocs)
    uniqueCats = nbClassifier.uniqify(docCats)
    
    print "Loading Classifier."
    clf = joblib.load("pickles/SK_NB/SK_classifier.pkl")
#     nbClassifier.printImpWords(tfidfVec, clf, None, clf.classes_, 50)
#     nbClassifier.showMistakes(clf, testDocs, tfidfs, clf.classes_)
#     print "Accuracy: "
#     print clf.score(tfidfs, docCats)
    nbClassifier.SK_NB_accuracy(clf, tfidfVec, None, True, True, uniqueCats)
    
    
#     todo list:  
#     ================== DONE ================= organize pickles
#     find precision recall and f score in accuracy functions and maybe try use it to make better decisions
 #    decide how to move on based on fscore results (imbalanced) and wikipedia db
#     cleanup project and make sub folders
#     use pipeline instead
#     look into the hashingVector big data problem
#     figure out with partial_fit
#     make passive agressive, test it
#     then fix up NLTK classifiers make sure they work with joblib, 
#     look into a hiearichal classification with partial_fit()
#     give accuracy on a test set, keep sperate test sets eg first10daysofJuly
#     make a proper training data thing
#     a classify_unlabelled function that will run for the acutal app
#     use nltk features to test and increase accuracy e.g stemming, collocations
#     make a function that checks accuracy by setting a documents class to itsmost probable 2/3
#     look into a hiearichal classification with partial_fit()
#     be able to search which category a word probably belongs to
#     then fit in bhais sentiment analysis
#     make entiityExtraction after all these
#     
#     ================== DONE =================  make trainDocs in classifier not an option, just class_labels
#     ================== DONE ================= also, optimize training function to write classifier pkl file, remove it from RAM, then make tfidf pkl
#     ================== DONE ================= testing function before writing both pickle files that returns accuracy and confirms if you want to write it
#     ================== DONE ================= also check most useful features of the classifier and check how useful game of thrones is as a feature
#     ================== DONE =================  also, crawl for seperate test data and document code

if (__name__ == "__main__"):
    main()