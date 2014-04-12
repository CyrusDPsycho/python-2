import re 

# construct bigram dict for an input file
def construct_bigram_dict(filename):
	'''construct words dict'''
	f = open(filename,'rU')
	words = []
	for line in f:
		match  = re.findall(r'[a-zA-Z\-]+|[\.\,\?]',line)
		if match:
			words.extend(match)
	#print words
	f.close()
	'''construct bigram and unigram probabilty dict'''
	'''eg.bigram probabilty dict looks like {bigram1:probabilty1,bigram2:probabilty2,...}'''
	unigrams = {}
	bigrams = {}
	for word in words:
		if word in unigrams:
			unigrams[word] += 1
		else:
			unigrams[word] = 1
	#print unigrams
	bi_words = []
	for i in range(len(words)-1):
		bi_words.append(words[i]+' '+words[i+1])
	
	#print bi_words
	for bi_word in bi_words:
		if bi_word in bigrams:
			bigrams[bi_word] += 1
		else:
			bigrams[bi_word] = 1

	uni_len = len(words)
	for key in unigrams.keys():
		unigrams[key] = (unigrams[key] + 0.0) / uni_len
	#print unigrams

	bi_len = len(words) - 1
	for key in bigrams.keys():
		bigrams[key] = (bigrams[key] + 0.0) / bi_len
	#print bigrams
	return (unigrams,bigrams)

#caculate probability of each bigram in dict
def caculate_probability(unigrams,bigrams,sentence):
	def caculate_helper(pre_word,cur_word):
		tmp_bigram = pre_word + ' ' + cur_word
		p_bigram = (bigrams[tmp_bigram] if tmp_bigram in bigrams else 0)
		#print p_bigram
		p_pre_word = (unigrams[pre_word] if pre_word in unigrams else 1)
		#print p_pre_word
		return p_bigram/p_pre_word
	words = sentence.split()
	#print words
	p_sentence = unigrams[words[0]]
	for i in range(len(words)-1):
		p_sentence = p_sentence*caculate_helper(words[i],words[i+1])
		#print p_sentence
	return p_sentence


if __name__ == '__main__':
	(unigrams,bigrams) = construct_bigram_dict('nonsense.txt')
	
	'''print bigrams'''
	print 'bigrams:\n'
	for key in bigrams.keys():
		print key + ' : ' + str(bigrams[key])
	print '\n'
	'''print sentences and their probabilties'''
	print "sentences and their probabilties:\n"
	sentence_a = "I do not like them in a mouse ."
	print sentence_a
	print caculate_probability(unigrams,bigrams,sentence_a)
	sentence_b = "I am Sam I am Sam"
	print sentence_b
	print caculate_probability(unigrams,bigrams,sentence_b)
	sentence_c = "I do like them anywhere ."
	print sentence_c
	print caculate_probability(unigrams,bigrams,sentence_c)