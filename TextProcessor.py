class TextProcessor():
    @staticmethod
    def SK_NB_calcTFIDFs(docs, train = False, writeToFile = False):
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.externals import joblib
        
        rawDocs = [doc.content for doc in docs]
#         for doc in rawDocs:
#             if (len(doc.split(" ") < 6)):
#                 print doc
        
        print "Calculating TFIDFs."
        
        if (train):
            tfidfVec = TfidfVectorizer(ngram_range=(1,1), stop_words='english')
            tfidfs = tfidfVec.fit_transform(rawDocs)
            if (writeToFile):
                print "Writing TFIDF pickle file."
                joblib.dump(tfidfVec, "pickles/SK_NB/SK_Tfidfs.pkl")
        else:
            print "Loading TFIDF pickle file."
            tfidfVec = joblib.load("pickles/SK_NB/SK_Tfidfs.pkl")
            tfidfs = tfidfVec.transform(rawDocs)
        print "TFIDFs calculated."
        return [tfidfVec, tfidfs]
        