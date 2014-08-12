import os
import Document as Doc

class FileHandler():
    def makeLog(self, myFile, msg):
        logDir = "logs/"    
        os.chdir(logDir)
        
        fo = open(myFile, 'a')
        fo.write(msg + "\n")
        fo.close()
    
    def loadDirs(self, myDir, labelled = False):
        docs = []
        basepath = os.getcwd()
        print "Loading files..."
        for subdir, dirs, files in os.walk(myDir):
            os.chdir(subdir)
            
            for file in files:
                fo = open(file, 'r')
                
                content = fo.read()
                doc = Doc.Document(file, content)
                if (labelled):
                    doc.category = subdir.split("/")[-1]
                
                docs.append(doc)
                fo.close()
                
            os.chdir(basepath)
        print "Loaded Documents."
        return docs
        
          