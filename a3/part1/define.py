#####
#This file is for training. 
#####

############transition probs##########
### looks at what pos comes after another pos in the file
### might need to reformulate transition to be the pos as the key and the prob..

noun = {'n-n': 0, 'n-v': 0, 'n-adj': 0, 'n-adv': 0, 'n-adp':0,'n-conj':0, 'n-det': 0, 'n-num':0, 'n-pron': 0, 'n-prt':0, 'n-X': 0, 'n-.':0}
verb = {'v-n': 0, 'v-v': 0, 'v-adj': 0, 'v-adv': 0, 'v-adp':0, 'v-conj':0, 'v-det': 0, 'v-num':0, 'v-pron': 0, 'v-prt':0, 'v-X': 0, 'v-.':0}
adj = {'adj-n': 0, 'adj-v': 0, 'adj-adj': 0, 'adj-adv': 0,  'adj-adp':0,'adj-conj':0, 'adj-det': 0, 'adj-num':0, 'adj-pron': 0, 'adj-prt':0, 'adj-X': 0, 'adj-.':0}
adv = {'adv-n': 0, 'adv-v': 0, 'adv-adj': 0, 'adv-adv': 0, 'adv-adp':0, 'adv-conj':0, 'adv-det': 0, 'adv-num':0, 'adv-pron': 0, 'adv-prt':0, 'adv-X': 0, 'adv-.':0}
adp = {'adp-n': 0, 'adp-v': 0, 'adp-adj': 0, 'adp-adv': 0, 'adp-adp':0, 'adp-conj':0, 'adp-det': 0, 'adp-num':0, 'adp-pron': 0, 'adp-prt':0, 'adp-X': 0, 'adp-.':0}
conj = {'conj-n': 0, 'conj-v': 0, 'conj-adj': 0, 'conj-adv': 0, 'conj-adp':0, 'conj-conj':0, 'conj-det': 0, 'conj-num':0, 'conj-pron': 0, 'conj-prt':0, 'conj-X': 0, 'conj-.':0}
det = {'det-n': 0, 'det-v': 0, 'det-adj': 0, 'det-adv': 0, 'det-adp':0, 'det-conj':0, 'det-det': 0, 'det-num':0, 'det-pron': 0, 'det-prt':0, 'det-X': 0, 'det-.':0}
num = {'num-n': 0, 'num-v': 0, 'num-adj': 0, 'num-adv': 0, 'num-adp':0, 'num-conj':0, 'num-det': 0, 'num-num':0, 'num-pron': 0, 'num-prt':0, 'num-X': 0, 'num-.':0}
pron = {'pron-n': 0, 'pron-v': 0, 'pron-adj': 0, 'pron-adv': 0, 'pron-adp':0, 'pron-conj':0, 'pron-det': 0, 'pron-num':0, 'pron-pron': 0, 'pron-prt':0, 'pron-X': 0, 'pron-.':0}
prt = {'prt-n': 0, 'prt-v': 0, 'prt-adj': 0, 'prt-adv': 0, 'prt-adp':0, 'prt-conj':0, 'prt-det': 0, 'prt-num':0, 'prt-pron': 0, 'prt-prt':0, 'prt-X': 0, 'prt-.':0}
X = {'X-n': 0, 'X-v': 0, 'X-adj': 0, 'X-adv': 0, 'X-adp':0, 'X-conj':0, 'X-det': 0, 'X-num':0, 'X-pron': 0, 'X-prt':0, 'X-X': 0, 'X-.':0}
punct = {'.-n': 0, '.-v': 0, '.-adj': 0, '.-adv': 0, '.-adp':0, '.-conj':0, '.-det': 0, '.-num':0, '.-pron': 0, '.-prt':0, '.-X': 0, '.-.':0}

transition = {'noun': noun, 'verb':verb, 'adj':adj, 'adv':adv, 'adp':adp, 'conj':conj,'det':det, 'num':num, 'pron':pron, 'prt':prt, 'x':X, '.':punct}

##############start probs################
### likelihood of a sentence starting w/ pos
### also notes each word starts sentence
startn = {}
startv = {}
startadj ={}
startadv = {}
startadp = {}
startconj = {}
startdet = {}
startnum = {}
startpron = {}
startprt = {}
startX = {}
startpunct = {}

start = {'noun':startn, 'verb': startv, 'adj': startadj, 'adv':startadv, 'adp':startadp, 'conj': startconj, 'det': startdet, 'num': startnum, 'pron':startpron, 'prt': startprt, 'x': startX, '.':startpunct}

###############emission probs################
### looks at what words represent each pos in file
outn = {}
outv = {}
outadj = {}
outadv = {}
outadp = {}
outconj = {}
outdet = {}
outnum = {}
outpron = {}
outprt = {}
outX = {}
outpunct = {}
out = {'noun':outn, 'verb': outv, 'adj': outadj, 'adv':outadv, 'adp':outadp, 'conj': outconj, 'det': outdet, 'num': outnum, 'pron':outpron, 'prt': outprt, 'x': outX, '.': outpunct}

key = {1:'noun', 2: 'verb', 3:'adj', 4:'adv', 5:'adp', 6:'conj'}

def define (words, pos): 
    """
    Takes the data and builds parameters from the training set.
    """
    words = list(words)
    pos = list(pos)
    startword = words[0]
    startpos = pos[0]
    checkpos(startword, startpos, 'S')
    previous = (startpos, 'S')
    for i in range(1, len(words)):
        newword = words[i]
        newpos = pos[i]
        if previous[1] == 'S':
            checkpos(newword, newpos, 'O')
            trprobs(newpos, previous)
            previous = (newpos, 'O')
        elif previous[1] == 'O':
            checkpos(newword, newpos, 'O')
            trprobs(newpos, previous)
            if newword == '.':
                previous = (newpos, 'End')
            else:
                previous = (newpos, 'O')
        elif previous[1] == 'End':
            checkpos(newword, newpos, 'S')
            trprobs(newpos, previous)
            previous = (newpos, 'S')



def checkpos (word, pos, w):
    """
    Checks the pos of each word. Then checks whether it's a start or out prob and adds to proper dictionary
    """
    if pos == 'noun':
        if w == 'S':
            if word not in startn.keys():
                startn[word] = 1
            else:
                startn[word] += 1
        #if w == 'O' or w == 'End':
        if word not in outn.keys():
            outn[word] = 1
        else:
            outn[word] += 1
    elif pos == 'verb':
        if w == 'S':
            if word not in startv.keys():
                startv[word] = 1
            else:
                startv[word] += 1
        #if w == 'O' or w == 'End':
        if word not in outv.keys():
            outv[word] = 1
        else:
            outv[word] += 1
    elif pos == 'adj':
        if w == 'S':
            if word not in startadj.keys():
                startadj[word] = 1
            else:
                startadj[word] += 1
        #if w == 'O' or w == 'End':
        if word not in outadj.keys():
            outadj[word] = 1
        else:
            outadj[word] += 1
    elif pos == 'adv':
        if w == 'S':
            if word not in startadv.keys():
                startadv[word] = 1
            else:    
                startadv[word] += 1
        #if w == 'O' or w == 'End':
        if word not in outadv.keys():
            outadv[word] = 1
        else:
            outadv[word] += 1
    elif pos == 'adp':
        if w == 'S':
            if word not in startadp.keys():
                startadp[word] = 1
            else:
                startadp[word] += 1
        #if w == 'O' or w == 'End':
        if word not in outadp.keys():
            outadp[word] = 1
        else:
            outadp[word] += 1
    elif pos == 'conj':
        if w == 'S':
            if word not in startconj.keys():
                startconj[word] = 1
            else:
                startconj[word] += 1
        #if w == 'O' or w == 'End':
        if word not in outconj.keys():
            outconj[word] = 1
        else:
            outconj[word] += 1
    elif pos == 'det':
        if w == 'S':
            if word not in startdet.keys():
                startdet[word] = 1
            else:
                startdet[word] += 1
        #if w == 'O' or w == 'End':
        if word not in outdet.keys():
            outdet[word] = 1
        else:
            outdet[word] += 1
    elif pos == 'num':
        if w == 'S':
            if word not in startnum.keys():
                startnum[word] = 1
            else:
                startnum[word] += 1
        #if w == 'O' or w == 'End':
        if word not in outnum.keys():
            outnum[word] = 1
        else:
            outnum[word] += 1
    elif pos == 'pron':
        if w == 'S':
            if word not in startpron.keys():
                startpron[word] = 1
            else:
                startpron[word] += 1
        #if w == 'O' or w == 'End':
        if word not in outpron.keys():
            outpron[word] = 1
        else:
            outpron[word] += 1
    elif pos == 'prt':
        if w == 'S':
            if word not in startprt.keys():
                startprt[word] = 1
            else:
                startprt[word] += 1
        #if w == 'O' or w == 'End':
        if word not in outprt.keys():
            outprt[word] = 1
        else:
            outprt[word] += 1
    elif pos == 'x':
        if w == 'S':
            if word not in startX.keys():
                startX[word] = 1
            else:
                startX[word] += 1
        #if w == 'O' or w == 'End':
        if word not in outX.keys():
            outX[word] = 1
        else:
            outX[word] += 1
    elif pos == '.':
        if w == 'S':
            if word not in startpunct.keys():
                startpunct[word] = 1
            else:
                startpunct[word] += 1
        #if w == 'O' or w == 'End':
        if word not in outpunct.keys():
            outpunct[word] = 1
        else:
            outpunct[word] += 1

def trprobs (current, previous):
    """
    Takes the current pos and previous pos and adds to proper transition dictionary. Key names are for previous to current pos. 
    """
    if previous[0] == 'noun':
        if current == 'noun':
            noun['n-n'] += 1
        elif current == 'verb':
            noun['n-v'] += 1
        elif current == 'adj':
            noun['n-adj'] += 1
        elif current == 'adv':
            noun['n-adv'] += 1
        elif current == 'adp':
            noun['n-adp'] += 1
        elif current == 'conj':
            noun['n-conj'] += 1
        elif current == 'det':
            noun['n-det'] += 1
        elif current == 'num':
            noun['n-num'] += 1
        elif current == 'pron':
            noun['n-pron'] += 1
        elif current == 'prt':
            noun['n-prt'] += 1
        elif current == 'x':
            noun['n-X'] += 1
        elif current == '.':
            noun['n-.'] += 1
    elif previous[0] == 'verb':
        if current == 'noun':
            verb['v-n'] += 1
        elif current == 'verb':
            verb['v-v'] += 1
        elif current == 'adj':
            verb['v-adj'] += 1
        elif current == 'adv':
            verb['v-adv'] += 1
        elif current == 'adp':
            verb['v-adp'] += 1
        elif current == 'conj':
            verb['v-conj'] += 1
        elif current == 'det':
            verb['v-det'] += 1
        elif current == 'num':
            verb['v-num'] += 1
        elif current == 'pron':
            verb['v-pron'] += 1
        elif current == 'prt':
            verb['v-prt'] += 1
        elif current == 'x':
            verb['v-X'] += 1
        elif current == '.':
            verb['v-.'] += 1
    elif previous[0] == 'adj':
        if current == 'noun':
            adj['adj-n'] += 1
        elif current == 'verb':
            adj['adj-v'] += 1
        elif current == 'adj':
            adj['adj-adj'] += 1
        elif current == 'adv':
            adj['adj-adv'] += 1
        elif current == 'adp':
            adj['adj-adp'] += 1
        elif current == 'conj':
            adj['adj-conj'] += 1
        elif current == 'det':
            adj['adj-det'] += 1
        elif current == 'num':
            adj['adj-num'] += 1
        elif current == 'pron':
            adj['adj-pron'] += 1
        elif current == 'prt':
            adj['adj-prt'] += 1
        elif current == 'x':
            adj['adj-X'] += 1
        elif current == '.':
            adj['adj-.'] += 1
    elif previous[0] == 'adv':
        if current == 'noun':
            adv['adv-n'] += 1
        elif current == 'verb':
            adv['adv-v'] += 1
        elif current == 'adj':
            adv['adv-adj'] += 1
        elif current == 'adv':
            adv['adv-adv'] += 1
        elif current == 'adp':
            adv['adv-adp'] += 1
        elif current == 'conj':
            adv['adv-conj'] += 1
        elif current == 'det':
            adv['adv-det'] += 1
        elif current == 'num':
            adv['adv-num'] += 1
        elif current == 'pron':
            adv['adv-pron'] += 1
        elif current == 'prt':
            adv['adv-prt'] += 1
        elif current == 'x':
            adv['adv-X'] += 1
        elif current == '.':
            adv['adv-.'] += 1
    elif previous[0] == 'adp':
        if current == 'noun':
            adp['adp-n'] += 1
        elif current == 'verb':
            adp['adp-v'] += 1
        elif current == 'adj':
            adp['adp-adj'] += 1
        elif current == 'adv':
            adp['adp-adv'] += 1
        elif current == 'adp':
            adp['adp-adp'] += 1
        elif current == 'conj':
            adp['adp-conj'] += 1
        elif current == 'det':
            adp['adp-det'] += 1
        elif current == 'num':
            adp['adp-num'] += 1
        elif current == 'pron':
            adp['adp-pron'] += 1
        elif current == 'prt':
            adp['adp-prt'] += 1
        elif current == 'x':
            adp['adp-X'] += 1
        elif current == '.':
            adp['adp-.'] += 1
    elif previous[0] == 'conj':
        if current == 'noun':
            conj['conj-n'] += 1
        elif current == 'verb':
            conj['conj-v'] += 1
        elif current == 'adj':
            conj['conj-adj'] += 1
        elif current == 'adv':
            conj['conj-adv'] += 1
        elif current == 'adp':
            conj['conj-adp'] += 1
        elif current == 'conj':
            conj['conj-conj'] += 1
        elif current == 'det':
            conj['conj-det'] += 1
        elif current == 'num':
            conj['conj-num'] += 1
        elif current == 'pron':
            conj['conj-pron'] += 1
        elif current == 'prt':
            conj['conj-prt'] += 1
        elif current == 'x':
            conj['conj-X'] += 1
        elif current == '.':
            conj['conj-.'] += 1
    elif previous[0] == 'det':
        if current == 'noun':
            det['det-n'] += 1
        elif current == 'verb':
            det['det-v'] += 1
        elif current == 'adj':
            det['det-adj'] += 1
        elif current == 'adv':
            det['det-adv'] += 1
        elif current == 'adp':
            det['det-adp'] += 1
        elif current == 'conj':
            det['det-conj'] += 1
        elif current == 'det':
            det['det-det'] += 1
        elif current == 'num':
            det['det-num'] += 1
        elif current == 'pron':
            det['det-pron'] += 1
        elif current == 'prt':
            det['det-prt'] += 1
        elif current == 'x':
            det['det-X'] += 1
        elif current == '.':
            det['det-.'] += 1
    elif previous[0] == 'num':
        if current == 'noun':
            num['num-n'] += 1
        elif current == 'verb':
            num['num-v'] += 1
        elif current == 'adj':
            num['num-adj'] += 1
        elif current == 'adv':
            num['num-adv'] += 1
        elif current == 'adp':
            num['num-adp'] += 1
        elif current == 'conj':
            num['num-conj'] += 1
        elif current == 'det':
            num['num-det'] += 1
        elif current == 'num':
            num['num-num'] += 1
        elif current == 'pron':
            num['num-pron'] += 1
        elif current == 'prt':
            num['num-prt'] += 1
        elif current == 'x':
            num['num-X'] += 1
        elif current == '.':
            num['num-.'] += 1
    elif previous[0] == 'pron':
        if current == 'noun':
            pron['pron-n'] += 1
        elif current == 'verb':
            pron['pron-v'] += 1
        elif current == 'adj':
            pron['pron-adj'] += 1
        elif current == 'adv':
            pron['pron-adv'] += 1
        elif current == 'adp':
            pron['pron-adp'] += 1
        elif current == 'conj':
            pron['pron-conj'] += 1
        elif current == 'det':
            pron['pron-det'] += 1
        elif current == 'num':
            pron['pron-num'] += 1
        elif current == 'pron':
            pron['pron-pron'] += 1
        elif current == 'prt':
            pron['pron-prt'] += 1
        elif current == 'x':
            pron['pron-X'] += 1
        elif current == '.':
            pron['pron-.'] += 1
    elif previous[0] == 'prt':
        if current == 'noun':
            prt['prt-n'] += 1
        elif current == 'verb':
            prt['prt-v'] += 1
        elif current == 'adj':
            prt['prt-adj'] += 1
        elif current == 'adv':
            prt['prt-adv'] += 1
        elif current == 'adp':
            prt['prt-adp'] += 1
        elif current == 'conj':
            prt['prt-conj'] += 1
        elif current == 'det':
            prt['prt-det'] += 1
        elif current == 'num':
            prt['prt-num'] += 1
        elif current == 'pron':
            prt['prt-pron'] += 1
        elif current == 'prt':
            prt['prt-prt'] += 1
        elif current == 'x':
            prt['prt-X'] += 1
        elif current == '.':
            prt['prt-.'] += 1
    elif previous[0] == 'x':
        if current == 'noun':
            X['X-n'] += 1
        elif current == 'verb':
            X['X-v'] += 1
        elif current == 'adj':
            X['X-adj'] += 1
        elif current == 'adv':
            X['X-adv'] += 1
        elif current == 'adp':
            X['X-adp'] += 1
        elif current == 'conj':
            X['X-conj'] += 1
        elif current == 'det':
            X['X-det'] += 1
        elif current == 'num':
            X['X-num'] += 1
        elif current == 'pron':
            X['X-pron'] += 1
        elif current == 'prt':
            X['X-prt'] += 1
        elif current == 'x':
            X['X-X'] += 1
        elif current == '.':
            X['X-.'] += 1
    elif previous[0] == '.':
        if current == 'noun':
            punct['.-n'] += 1
        elif current == 'verb':
            punct['.-v'] += 1
        elif current == 'adj':
            punct['.-adj'] += 1
        elif current == 'adv':
            punct['.-adv'] += 1
        elif current == 'adp':
            punct['.-adp'] += 1
        elif current == 'conj':
            punct['.-conj'] += 1
        elif current == 'det':
            punct['.-det'] += 1
        elif current == 'num':
            punct['.-num'] += 1
        elif current == 'pron':
            punct['.-pron'] += 1
        elif current == 'prt':
            punct['.-prt'] += 1
        elif current == 'x':
            punct['.-X'] += 1
        elif current == '.':
            punct['.-.'] += 1

