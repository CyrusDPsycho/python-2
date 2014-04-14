# coding=utf-8

import re

#read in a tnt tagged file and convert it to a conll format file for marltparser to parse
#each line in tnt tagged file has the format (word,tag) and each line in conll has the format
#(iden,form,lemma,cpostag,postag,feats,head,deprel,phead,pdeprel),this version only works for English
def tnt_to_conll(file_name):
	f = open(file_name,'r')
	tnt = []
	conll = []
	i = 1
	for line in f:
		if line != '\n' and not re.findall(r'^%%',line):
			line = line.replace('\n','')
			line = re.split('[\r\t]+',line)
			word , tag = tuple(line)
			conll.append([str(i),word,'_',tag,tag,'_','0','Root','_','_'])
			i += 1
			if word == '.':
				i = 1
	f.close()
	return conll

if __name__ == '__main__':
	conll = tnt_to_conll('test2.tagged')
	f = open('test2.conll','w')
	seq = []
	first = False
	for line in conll:
		new_line = '\t'.join(line) + '\n'
		if first and int(line[0]) == 1:
			seq.append('\n')
		seq.append(new_line)
		first = True
	#seq = [ '\t'.join(list(line)) + '\n' for line in conll ]
	seq.append('\n')
	seq.append('\n')
	f.writelines(seq)
	f.close()