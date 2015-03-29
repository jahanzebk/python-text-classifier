import nltk


class EntityExtractor:
	def __init__(self):
		pass


	def get_people(self):
		pass


	def get_organizations(self):
		pass


	def get_money(self, taggedText):
		
		#Pattern = $3.2 billion or 50 billion dollars or 50 Dollars
		pattern = """
			MONEY:
				{<\$>?<CD>+<NNP|NNS|NN>?}
		"""

		MoneyChunker = nltk.RegexpParser(pattern)
		result		 = MoneyChunker.parse(taggedText)

		return result


	def get_date_time(self):
		pass


	def get_percentage(self):
		pass


	def get_places(self):
		pass





def main():
	text = "I sold my company worth $3.4 Million to some other company for thirty four thousand dollars in yen. I am a rich man now."
	from nltk.tokenize import word_tokenize
	posTagger = nltk.data.load('taggers/maxent_treebank_pos_tagger/english.pickle')

	tokens  = word_tokenize(text)
	posTags = posTagger.tag(tokens)

	ee = EntityExtractor()
	print ee.get_money(posTags)

# 	print nltk.chunk.util.ieerstr2tree(text, chunk_types=['LOCATION', 'ORGANIZATION', 'PERSON', 'DURATION', 'DATE', 'CARDINAL', 'PERCENT', 'MONEY', 'MEASURE'])

	

if __name__ == '__main__':
	main()