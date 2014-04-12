# coding=utf-8
import csv

#take a list of pos-tags and a map of grammar which has the (non-terminal,rule_list)
#return the chart table which stores partial results during CYK parsing
def cyk_offline_parser(pos,grammar):
	#each element of chart should be like this chart[length][start] = symbol_list
	n = len(pos)
	chart = [ [ [] for y in range(n+1) ] for x in range(n+1) ] 

	#intialize the chart[1][start] with pos-tags and its direct inference
	for i in range(1,n+1):
		chart[1][i].append(pos[i-1])
		if (pos[i-1]) in grammar:
			chart[1][i].append(grammar[(pos[i-1])])

	#fill in all valid cells in chart
	for length in range(2,n+1):
		for start in range(1,n-length+2):
			
			#if B C ==> A ,then char[length][start] += {A}
			for m in range(1,length):
				if len(chart[m][start]) and len(chart[length-m][start+m]):
					for symbol_B in chart[m][start]:
						for symbol_C in chart[length-m][start+m]:
						 	if (symbol_B,symbol_C) in grammar:
						 		chart[length][start].append(grammar[(symbol_B,symbol_C)])
			
			#if B C D ==> A,then char[length][start] += {A}
			for m in range(1,length-1):
				for m1 in range(1,length-m):
					if len(chart[m][start]) and len(chart[m1][start+m]) and len(chart[length-m-m1][start+m+m1]):
						for symbol_B in chart[m][start]:
							for symbol_C in chart[m1][start+m]:
								for symbol_D in chart[length-m-m1][start+m+m1]:
									if (symbol_B,symbol_C,symbol_D) in grammar:
										chart[length][start].append(grammar[(symbol_B,symbol_C,symbol_D)])
			
			#if B C D E ==> A,then char[length][start] += {A}
			for m in range(1,length-2):
				for m1 in range(1,length-m-1):
					for m2 in range(1,length-m-m1):
						if len(chart[m][start]) and len(chart[m1][start+m]) and len(chart[m2][start+m+m1]) and len(chart[length-m-m1-m2][start+m+m1+m2]):
							for symbol_B in chart[m][start]:
								for symbol_C in chart[m1][start+m]:
									for symbol_D in chart[m2][start+m+m1]:
										for symbol_E in chart[length-m-m1-m2][start+m+m1+m2]:
											if (symbol_B,symbol_C,symbol_D,symbol_E) in grammar:
												chart[length][start].append(grammar[(symbol_B,symbol_C,symbol_D,symbol_E)])

	return chart

#return the correct ways of parsing
def how_many_ways_of_parsing(chart):
	return len(chart[len(chart)-1][1])

def write_to_csv(chart):
	with open('chart.csv','w') as f:
		chart_writer = csv.writer(f)
		n = len(chart)
		for i in range(1,n):
			chart_writer.writerow(chart[n-i][1:i+1])

if __name__ == '__main__':

	#test case 1
	'''
	grammar = {
		('NP','VP') : 'S',
		('kon','NP','VP') : 'S',
		('NP','VP','S') : 'S',
		('S','S') : 'S',
		('det','n') : 'NP',
		('det','adj','n') : 'NP',
		('adj','n') : 'NP',
		('pp') : 'NP',
		('v') : 'VP',
		('v','NP') : 'VP',
		('v','ADJP') : 'VP',
		('VP','kon','VP') : 'VP',
		('adj') : 'ADJP',
		('adv','adj') : 'ADJP'
	}

	pos = ['kon','pp','v','det','n','det','n','v','adj','kon','det','n','v','adj','n']
	'''

	#test case 2
	grammar = {
		('NP','VP') : 'S',
		('IN','NP','VP') : 'S',
		('IN','NP','VP','S') : 'S',
		('DT','NN') : 'NP',
		('CD','NN') : 'NP',
		('NE') : 'NP',
		('DT','NE','NE') : 'NP',
		('PRP') : 'NP',
		('NP','PP') : 'NP',
		('IN','NP') : 'PP',
		('JJ') : 'JP',
		('VBZ','S') : 'VP',
		('VBD','NP','PP') : 'VP',
		('VBD','JP') :'VP'
	}

	pos = ['CD','NN','VBZ','IN','DT','NN','IN','NE','VBD','PRP','IN','DT','NE','NE','IN','PRP','VBD','JJ']
	chart = cyk_offline_parser(pos,grammar)

	write_to_csv(chart)

	print how_many_ways_of_parsing(chart)