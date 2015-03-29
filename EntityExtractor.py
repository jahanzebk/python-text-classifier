# from nltk.internals import config_java
# config_java("C:/Program Files/Java/jdk1.8.0_05/bin/java.exe")
 
class EntitityExtractor():
    def ST_NER_extract_entities(self):
        from nltk.tag.stanford import NERTagger
        st = NERTagger('C:\Users\Jahanzeb\workspace/turboEngine\stanford-ner\classifiers\english.all.3class.distsim.crf.ser.gz',
                'C:\Users\Jahanzeb\workspace/turboEngine\stanford-ner\stanford-ner.jar')
        print "Loaded Tagger." 
        ents =  st.tag('Rami Eid is studying at Stony Brook University located in NY'.split())
        return ents
        
    def NLTK_NER(self):
        from nltk import sent_tokenize, word_tokenize, pos_tag, batch_ne_chunk
        
        sample = "Rami's Eid is studying at Stony Brook University located in NY."
        sentences = sent_tokenize(sample)
        tokenized_sentences = [word_tokenize(sentence) for sentence in sentences]
        tagged_sentences = [pos_tag(sentence) for sentence in tokenized_sentences]
        chunked_sentences = batch_ne_chunk(tagged_sentences)
#         print chunked_sentences

        
    def NLTK_rel_ext(self, tree):
        from nltk.corpus import ieer
        docs = ieer.parsed_docs('NYT_19980315')
        tree = docs[1].text
        print(tree) 
        
        from nltk.sem import relextract
        reldicts = relextract.semi_rel2reldict(pairs)
        for k, v in sorted(reldicts[0].items()):
            print(k, '=>', v) 

if __name__ == '__main__':
    ee = EntitityExtractor()
    ents = ee.ST_NER_extract_entities()
    ee.NLTK_NER()
    ee.NLTK_rel_ext(ents)
