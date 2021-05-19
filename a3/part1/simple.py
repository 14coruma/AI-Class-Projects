import prob
import define
## uses actual probabilities for this model
## this works just as well as simple.py
pos = ['noun', 'verb', 'adj', 'adv', 'adp', 'conj', 'det', 'num', 'pron', 'prt', 'x', '.']

con = {'noun': 0, 'verb':0, 'adj': 0, 'adv': 0, 'adp': 0, 'conj': 0, 'det': 0, 'num': 0, 'pron': 0, 'prt': 0, 'x': 0, '.': 0}

def find (word, total): 
    global pos
    lst = []
    pt1 = 0
    pt2 = 0
    pt3 = 0
    prob = 0
    largest = 0
    tag = ''
    for i in pos:
        pt1 = part1(word, i)
        if pt1 == 0: ## if word never been seen before (probability)
            prob = .0001/total
            ### to get tag maybe look at transition probabilities from simple.py
        else: ## if word has been seen before
            pt2 = part2(i,total)
            pt3 = part3(word, i, total)
            prob = (pt1 * pt2)/pt3
        lst += [prob]
        global con
        con[i] = prob
        if largest == 0:
            largest += prob
            if prob == .0001/total:
                tag = None
            else:
                tag = i
        elif prob > largest:
            largest += prob
            if prob == .0001/total:
                tag = None
            else:
                tag = i
    return tag, largest
    

## simple model p(si|W) = p(W|si) * p(si) / p(W)

# p(W|si)
def part1 (word, pos):
    Wsi = 0
    case = prob.outprobs[pos]
    if word in case.keys():
        Wsi = case[word] 
    return Wsi

# p(si)
def part2 (pos, total):
    case = prob.outprobs[pos]
    t = case['total'] 
    return t/total

# p(W)
def part3 (word, pos, total):
    """
    W = 0
    case = define.out[pos]
    if word in case.keys():
        W = case[word]
    W = W/total
    return W
    """
    W = 0
    a = 0
    b = 0
    for i in prob.outprobs:
        case = prob.outprobs[i]
        if word in case.keys():
            a = case[word]
            b = (case['total'])/ total
            p = a*b
        else:
            p = .01/total
        W += p
    return W


def examineTransition (previous): #revise
    smallest = (0, '')
    global pos_sentence
    if previous == 'noun':
        for i in define.noun:
            if smallest[1] == '':
                smallest = (define.noun[i], i)
            elif define.noun[i] > smallest[0]:
                smallest = (define.noun[i], i)
    elif previous == 'verb':
        for i in define.verb:
            if smallest[1] == '':
                smallest = (define.verb[i], i)
            elif define.verb[i] > smallest[0]:
                smallest = (define.verb[i], i)
    elif previous == 'adj':
        for i in define.adj:
            if smallest[1] == '':
                smallest = (define.adj[i], i)
            elif define.adj[i] > smallest[0]:
                smallest = (define.adj[i], i)
    elif previous == 'adv':
        for i in define.adv:
            if smallest[1] == '':
                smallest = (define.adv[i], i)
            elif define.adv[i] > smallest[0]:
                smallest = (define.adv[i], i)
    elif previous == 'adp':
        for i in define.adp:
            if smallest[1] == '':
                smallest = (define.adp[i], i)
            elif define.adp[i] > smallest[0]:
                smallest = (define.adp[i], i)
    elif previous == 'conj':
        for i in define.conj:
            if smallest[1] == '':
                smallest = (define.conj[i], i)
            elif define.conj[i] > smallest[0]:
                smallest = (define.conj[i], i)
    elif previous == 'det':
        for i in define.det:
            if smallest[1] == '':
                smallest = (define.det[i], i)
            elif define.det[i] > smallest[0]:
                smallest = (define.det[i], i)
    elif previous == 'num':
        for i in define.num:
            if smallest[1] == '':
                smallest = (define.num[i], i)
            elif define.num[i] > smallest[0]:
                smallest = (define.num[i], i)
    elif previous == 'pron':
        for i in define.pron:
            if smallest[1] == '':
                smallest = (define.pron[i], i)
            elif define.pron[i] > smallest[0]:
                smallest = (define.pron[i], i)
    elif previous == 'prt':
        for i in define.prt:
            if smallest[1] == '':
                smallest = (define.prt[i], i)
            elif define.prt[i] > smallest[0]:
                smallest = (define.prt[i], i)
    elif previous == 'x':
        for i in define.X:
            if smallest[1] == '':
                smallest = (define.X[i], i)
            elif define.X[i] > smallest[0]:
                smallest = (define.X[i], i)
    elif previous == '.':
        for i in define.punct:
            if smallest[1] == '':
                smallest = (define.punct[i], i)
            elif define.punct[i] > smallest[0]:
                smallest = (define.punct[i], i)
    if '-n' in smallest[1]:
        return 'noun'
    elif '-v' in smallest[1]:
        return 'verb'
    elif '-adj' in smallest[1]:
        return 'adj'
    elif '-adv' in smallest[1]:
        return 'adv'
    elif '-adp' in smallest[1]:
        return 'adp'
    elif '-conj' in smallest[1]:
        return 'conj'
    elif '-det' in smallest[1]:
        return 'det'
    elif '-num' in smallest[1]:
        return 'num'
    elif '-pron' in smallest[1]:
        return 'pron'
    elif '-prt' in smallest[1]:
        return 'prt'
    elif '-X' in smallest[1]:
        return 'x'
    elif '-.' in smallest[1]:
        return '.'