#This a GA exmaple searching for the best recipe for making cookies.
#It is consisted of sugar and flour as two major raw material.
#The quantity of sugar and flour range from 1 to 9 respectively
#and the quality of the cookie is measured from 0 to 9,9 represents best
#In this algorithm,we choose a recipe as chromosome and make sugar and
#flour as two genes for this chromosome.The initial population size is 1 and so
#crossover has been cancelled here and mutation is the main method for evolution.
#Each time we choose one cookie randomly in the population to mutate.

import random

#make the maximum trials to find good enough descendants 
maxTrials = 100

class Cookie:
    #recipes for cookie
    sugar = 0
    flour = 0
    #initialization
    def __init__(self,s,f):
        self.sugar = s
        self.flour = f
    def copy(self,c):
        self.sugar = c.sugar
        self.flour = c.flour

#mutation function
#the mutate rate is +/- 1 for sugar or flour
def mutate(c):
    cookie = Cookie(0,0)
    cookie.copy(c)
    if cookie.sugar == 1:
        if cookie.flour == 1:
            pos = random.choice([1,2])
            if pos == 1:
                cookie.sugar += 1
            else:
                cookie.flour += 1
        elif cookie.flour == 9:
            pos = random.choice([1,2])
            if pos == 1:
                cookie.sugar += 1
            else:
                cookie.flour -= 1
        else:
            pos = random.choice([1,2,3])
            if pos == 1:
                cookie.sugar += 1
            elif pos == 2:
                cookie.flour -= 1
            else:
                cookie.flour += 1
    elif cookie.sugar == 9:
        if cookie.flour == 1:
            pos = random.choice([1,2])
            if pos == 1:
                cookie.sugar -= 1
            else:
                cookie.flour += 1
        elif cookie.flour == 9:
            pos = random.choice([1,2])
            if pos == 1:
                cookie.sugar -= 1
            else:
                cookie.flour -= 1
        else:
            pos = random.choice([1,2,3])
            if pos == 1:
                cookie.sugar -= 1
            elif pos == 2:
                cookie.flour -= 1
            else:
                cookie.flour += 1
    elif cookie.flour == 1:
        pos = random.choice([1,2,3])
        if pos == 1:
            cookie.sugar += 1
        elif pos == 2:
            cookie.sugar -= 1
        else:
            cookie.flour += 1
    elif cookie.flour == 9:
        pos = random.choice([1,2,3])
        if pos == 1:
            cookie.sugar += 1
        elif pos == 2:
            cookie.sugar -= 1
        else:
            cookie.flour -= 1
    else:
        pos = random.choice([1,2,3,4])
        if pos == 1:
            cookie.sugar += 1
        elif pos == 2:
            cookie.flour += 1
        elif pos == 3:
            cookie.sugar -= 1
        else:
            cookie.flour -= 1
    return cookie

#return quality value of a cookie 
def quality(cookie):
    quality_table = [[1,2,3,4,5,4,3,2,1],
                     [2,0,0,0,0,0,0,0,2],
                     [3,0,0,0,0,0,0,0,3],
                     [4,0,0,7,8,7,0,0,4],
                     [5,0,0,8,9,8,0,0,5],
                     [4,0,0,7,8,7,0,0,4],
                     [3,0,0,0,0,0,0,0,3],
                     [2,0,0,0,0,0,0,0,2],
                     [1,2,3,4,5,4,3,2,1]]

    return quality_table[cookie.sugar-1][cookie.flour-1]

def printResult(cookies,roundNum):
    print "Generation",
    print roundNum
    print "Chromosome Quality"
    for c in cookies:
        print c.sugar,
        print " ",
        print c.flour,
        print "     ",
        print quality(c)
    print ""

#test if have enough fitable cookie
def testProcedure(cookies):
    for c in cookies:
        if quality(c) == 9:
            return True
    return False

#find out the Worst quanlity cookie
def worstCookie(cookies):
    worst = 10
    for c in cookies:
        if quality(c) < worst:
            worst = quality(c)
            worstcookie = c
    return worstcookie

def main(): 
    #cookies is the population of this GA problem
    #it max size is 4
    cookies = []
    cookies.append(Cookie(3,4)) 
    roundNum = 0
    #repeat the reproduce procedure until to find enough good descendant
    while(not testProcedure(cookies) and roundNum < maxTrials):
        printResult(cookies,roundNum)
        pos = random.randrange(0,len(cookies),1)
        mutateOne = mutate(cookies[pos])
        if len(cookies) < 4:
            cookies.append(mutateOne)
        else:
            #if the population size has reached to the maximum
            #select the worst and subsitute it with the mutated one
            c = worstCookie(cookies)
            if quality(c) < quality(mutateOne):
                cookies.remove(c)
                cookies.append(mutateOne)
        roundNum += 1

    printResult(cookies,roundNum)
    return

if __name__ == '__main__':
    main()
