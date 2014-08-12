import sys
import FileHandler as FH, Classifier, EntityExtractor as EE, TextProcessor as TP
import Document as Doc
from nltk import classify

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
    
def fullAnalysis(currSetDir):
    dir = "docs/testing/" # actual dir will be build from args (docs/userID/setID dir)
    nbClassifier = Classifier.Classifier()
    myFH = FH.FileHandler()
    
    #nbClassifier.nbSentiTrain()
    
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
      
    
   
    

if (__name__ == "__main__"):
    main()