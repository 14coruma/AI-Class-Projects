import prob
########
# Implements viterbi algorithm for HMM
########
#t0 is the dict for the first word in the sentence; assumes sentence always has at least one word
t0 = {'noun': 0, 'verb':0, 'adj': 0, 'adv': 0, 'adp': 0, 'conj': 0, 'det': 0, 'num': 0, 'pron': 0, 'prt': 0, 'x': 0, '.': 0}
sent = {0:t0}

def start (word, total): #looks good so far
    global sent, t0
    sent = {0:t0}
    largest = 0
    tag = ''
    ## add start probs
    for i in prob.startprob:
        if prob.startprob[i] == 0:
            t0[i] = .0001/total
        else:
            t0[i] = prob.startprob[i]
    ## multiply by outprobs
    for i in prob.outprobs:
        case = prob.outprobs[i]
        if word in case.keys():
            t0[i] *= case[word]
        else:
            t0[i] *= .0001/total

def rest (word, total):
    n = {'n-n': 0, 'v-n': 0, 'adj-n': 0, 'adv-n':0, 'adp-n': 0, 'conj-n': 0, 'det-n': 0, 'num-n':0, 'pron-n': 0, 'prt-n':0, 'X-n': 0, '.-n': 0}
    v = {'n-v': 0, 'v-v': 0, 'adj-v': 0, 'adv-v':0, 'adp-v': 0, 'conj-v': 0, 'det-v': 0, 'num-v':0, 'pron-v': 0, 'prt-v':0, 'X-v': 0, '.-v': 0}
    adj = {'n-adj': 0, 'v-adj': 0, 'adj-adj': 0, 'adv-adj':0, 'adp-adj': 0, 'conj-adj': 0, 'det-adj': 0, 'num-adj':0, 'pron-adj': 0, 'prt-adj':0, 'X-adj': 0, '.-adj': 0}
    adv = {'n-adv': 0, 'v-adv': 0, 'adj-adv': 0, 'adv-adv':0, 'adp-adv': 0, 'conj-adv': 0, 'det-adv': 0, 'num-adv':0, 'pron-adv': 0, 'prt-adv':0, 'X-adv': 0, '.-adv': 0}
    adp = {'n-adp': 0, 'v-adp': 0, 'adj-adp': 0, 'adv-adp':0, 'adp-adp': 0, 'conj-adp': 0, 'det-adp': 0, 'num-adp':0, 'pron-adp': 0, 'prt-adp':0, 'X-adp': 0, '.-adp': 0}
    conj = {'n-conj': 0, 'v-conj': 0, 'adj-conj': 0, 'adv-conj':0, 'adp-conj': 0, 'conj-conj': 0, 'det-conj': 0, 'num-conj':0, 'pron-conj': 0, 'prt-conj':0, 'X-conj': 0, '.-conj': 0}
    det = {'n-det': 0, 'v-det': 0, 'adj-det': 0, 'adv-det':0, 'adp-det': 0, 'conj-det': 0, 'det-det': 0, 'num-det':0, 'pron-det': 0, 'prt-det':0, 'X-det': 0, '.-det': 0}
    num = {'n-num': 0, 'v-num': 0, 'adj-num': 0, 'adv-num':0, 'adp-num': 0, 'conj-num': 0, 'det-num': 0, 'num-num':0, 'pron-num': 0, 'prt-num':0, 'X-num': 0, '.-num': 0}
    pron = {'n-pron': 0, 'v-pron': 0, 'adj-pron': 0, 'adv-pron':0, 'adp-pron': 0, 'conj-pron': 0, 'det-pron': 0, 'num-pron':0, 'pron-pron': 0, 'prt-pron':0, 'X-pron': 0, '.-pron': 0}
    prt = {'n-prt': 0, 'v-prt': 0, 'adj-prt': 0, 'adv-prt':0, 'adp-prt': 0, 'conj-prt': 0, 'det-prt': 0, 'num-prt':0, 'pron-prt': 0, 'prt-prt':0, 'X-prt': 0, '.-prt': 0}
    x = {'n-X': 0, 'v-X': 0, 'adj-X': 0, 'adv-X':0, 'adp-X': 0, 'conj-X': 0, 'det-X': 0, 'num-X':0, 'pron-X': 0, 'prt-X':0, 'X-X': 0, '.-X': 0}
    pun = {'n-.': 0, 'v-.': 0, 'adj-.': 0, 'adv-.':0, 'adp-.': 0, 'conj-.': 0, 'det-.': 0, 'num-.':0, 'pron-.': 0, 'prt-.':0, 'X-.': 0, '.-.': 0}

    newtime = len(sent)
    sent[newtime] = {'noun': n, 'verb': v, 'adj': adj, 'adv': adv, 'adp': adp, 'conj': conj, 'det': det, 'num': num, 'pron': pron, 'prt': prt, 'x': x ,'.': pun}

    for pos in sent[newtime]:
        if pos == 'noun':
            for p in sent[newtime-1]:
                case = sent[newtime-1]
                if p == 'noun':
                    n['n-n'] = case[p] # previous
                    if word in prob.onounprob.keys():
                        wordp = prob.onounprob[word]
                    else:
                        wordp = .0001/total
                    n['n-n'] *= wordp #output
                    t = prob.nounprob['n-n']
                    n['n-n'] *= t #transition
                elif p == 'verb':
                    n['v-n'] = case[p]
                    if word in prob.onounprob.keys():
                        wordp = prob.onounprob[word]
                    else:
                        wordp = .0001/total
                    n['v-n'] *= wordp #output
                    t = prob.verbprob['v-n']
                    n['v-n'] *= t #transition
                elif p == 'adj':
                    n['adj-n'] = case[p]
                    if word in prob.onounprob.keys():
                        wordp = prob.onounprob[word]
                    else:
                        wordp = .0001/total
                    n['adj-n'] *= wordp #output
                    t = prob.adjprob['adj-n']
                    n['adj-n'] *= t #transition
                elif p == 'adv':
                    n['adv-n'] = case[p]
                    if word in prob.onounprob.keys():
                        wordp = prob.onounprob[word]
                    else:
                        wordp = .0001/total
                    n['adv-n'] *= wordp #output
                    t = prob.advprob['adv-n']
                    n['adv-n'] *= t #transition
                elif p == 'adp':
                    n['adp-n'] = case[p]
                    if word in prob.onounprob.keys():
                        wordp = prob.onounprob[word]
                    else:
                        wordp = .0001/total
                    n['adp-n'] *= wordp #output
                    t = prob.adpprob['adp-n']
                    n['adp-n'] *= t #transition
                elif p == 'conj':
                    n['conj-n'] = case[p]
                    if word in prob.onounprob.keys():
                        wordp = prob.onounprob[word]
                    else:
                        wordp = .0001/total
                    n['conj-n'] *= wordp #output
                    t = prob.conjprob['conj-n']
                    n['conj-n'] *= t #transition
                elif p == 'det':
                    n['det-n'] = case[p]
                    if word in prob.onounprob.keys():
                        wordp = prob.onounprob[word]
                    else:
                        wordp = .0001/total
                    n['det-n'] *= wordp #output
                    t = prob.detprob['det-n']
                    n['det-n'] *= t #transition
                elif p == 'num':
                    n['num-n'] = case[p]
                    if word in prob.onounprob.keys():
                        wordp = prob.onounprob[word]
                    else:
                        wordp = .0001/total
                    n['num-n'] *= wordp #output
                    t = prob.numprob['num-n']
                    n['num-n'] *= t #transition
                elif p == 'pron':
                    n['pron-n'] = case[p]
                    if word in prob.onounprob.keys():
                        wordp = prob.onounprob[word]
                    else:
                        wordp = .0001/total
                    n['pron-n'] *= wordp #output
                    t = prob.pronprob['pron-n']
                    n['pron-n'] *= t #transition
                elif p == 'prt':
                    n['prt-n'] = case[p]
                    if word in prob.onounprob.keys():
                        wordp = prob.onounprob[word]
                    else:
                        wordp = .0001/total
                    n['prt-n'] *= wordp #output
                    t = prob.prtprob['prt-n']
                    n['prt-n'] *= t #transition
                elif p == 'x':
                    n['X-n'] = case[p]
                    if word in prob.onounprob.keys():
                        wordp = prob.onounprob[word]
                    else:
                        wordp = .0001/total
                    n['X-n'] *= wordp #output
                    t = prob.Xprob['X-n']
                    n['X-n'] *= t #transition
                elif p == '.':
                    n['.-n'] = case[p]
                    if word in prob.onounprob.keys()       :
                        wordp = prob.onounprob[word]
                    else:
                        wordp = .0001/total
                    n['.-n'] *= wordp #output
                    t = prob.punctprob['.-n']
                    n['.-n'] *= t #transition
        if pos == 'verb':
            for p in sent[newtime-1]:
                case = sent[newtime-1]
                if p == 'noun':
                    v['n-v'] = case[p] # previous
                    if word in prob.overbprob.keys():
                        wordp = prob.overbprob[word]
                    else:
                        wordp = .0001/total
                    v['n-v'] *= wordp #output
                    t = prob.nounprob['n-v']
                    v['n-v'] *= t #transition
                elif p == 'verb':
                    v['v-v'] = case[p]
                    if word in prob.overbprob.keys():
                        wordp = prob.overbprob[word]
                    else:
                        wordp = .0001/total
                    v['v-v'] *= wordp #output
                    t = prob.verbprob['v-v']
                    v['v-v'] *= t #transition
                elif p == 'adj':
                    v['adj-v'] = case[p]
                    if word in prob.overbprob.keys():
                        wordp = prob.overbprob[word]
                    else:
                        wordp = .0001/total
                    v['adj-v'] *= wordp #output
                    t = prob.adjprob['adj-v']
                    v['adj-v'] *= t #transition
                elif p == 'adv':
                    v['adv-v'] = case[p]
                    if word in prob.overbprob.keys():
                        wordp = prob.overbprob[word]
                    else:
                        wordp = .0001/total
                    v['adv-v'] *= wordp #output
                    t = prob.advprob['adv-v']
                    v['adv-v'] *= t #transition
                elif p == 'adp':
                    v['adp-v'] = case[p]
                    if word in prob.overbprob.keys():
                        wordp = prob.overbprob[word]
                    else:
                        wordp = .0001/total
                    v['adp-v'] *= wordp #output
                    t = prob.adpprob['adp-v']
                    v['adp-v'] *= t #transition
                elif p == 'conj':
                    v['conj-v'] = case[p]
                    if word in prob.overbprob.keys():
                        wordp = prob.overbprob[word]
                    else:
                        wordp = .0001/total
                    v['conj-v'] *= wordp #output
                    t = prob.conjprob['conj-v']
                    v['conj-v'] *= t #transition
                elif p == 'det':
                    v['det-v'] = case[p]
                    if word in prob.overbprob.keys():
                        wordp = prob.overbprob[word]
                    else:
                        wordp = .0001/total
                    v['det-v'] *= wordp #output
                    t = prob.detprob['det-v']
                    v['det-v'] *= t #transition
                elif p == 'num':
                    v['num-v'] = case[p]
                    if word in prob.overbprob.keys():
                        wordp = prob.overbprob[word]
                    else:
                        wordp = .0001/total
                    v['num-v'] *= wordp #output
                    t = prob.numprob['num-v']
                    v['num-v'] *= t #transition
                elif p == 'pron':
                    v['pron-v'] = case[p]
                    if word in prob.overbprob.keys():
                        wordp = prob.overbprob[word]
                    else:
                        wordp = .0001/total
                    v['pron-v'] *= wordp #output
                    t = prob.pronprob['pron-v']
                    v['pron-v'] *= t #transition
                elif p == 'prt':
                    v['prt-v'] = case[p]
                    if word in prob.overbprob.keys():
                        wordp = prob.overbprob[word]
                    else:
                        wordp = .0001/total
                    v['prt-v'] *= wordp #output
                    t = prob.prtprob['prt-v']
                    v['prt-v'] *= t #transition
                elif p == 'x':
                    v['X-v'] = case[p]
                    if word in prob.overbprob.keys():
                        wordp = prob.overbprob[word]
                    else:
                        wordp = .0001/total
                    v['X-v'] *= wordp #output
                    t = prob.Xprob['X-v']
                    v['X-v'] *= t #transition
                elif p == '.':
                    v['.-v'] = case[p]
                    if word in prob.overbprob.keys()       :
                        wordp = prob.overbprob[word]
                    else:
                        wordp = .0001/total
                    v['.-v'] *= wordp #output
                    t = prob.punctprob['.-v']
                    v['.-v'] *= t #transition
        if pos == 'adj':
            for p in sent[newtime-1]:
                case = sent[newtime-1]
                if p == 'noun':
                    adj['n-adj'] = case[p] # previous
                    if word in prob.oadjprob.keys():
                        wordp = prob.oadjprob[word]
                    else:
                        wordp = .0001/total
                    adj['n-adj'] *= wordp #output
                    t = prob.nounprob['n-adj']
                    adj['n-adj'] *= t #transition
                elif p == 'verb':
                    adj['v-adj'] = case[p]
                    if word in prob.oadjprob.keys():
                        wordp = prob.oadjprob[word]
                    else:
                        wordp = .0001/total
                    adj['v-adj'] *= wordp #output
                    t = prob.verbprob['v-adj']
                    adj['v-adj'] *= t #transition
                elif p == 'adj':
                    adj['adj-adj'] = case[p]
                    if word in prob.oadjprob.keys():
                        wordp = prob.oadjprob[word]
                    else:
                        wordp = .0001/total
                    adj['adj-adj'] *= wordp #output
                    t = prob.adjprob['adj-adj']
                    adj['adj-adj'] *= t #transition
                elif p == 'adv':
                    adj['adv-adj'] = case[p]
                    if word in prob.oadjprob.keys():
                        wordp = prob.oadjprob[word]
                    else:
                        wordp = .0001/total
                    adj['adv-adj'] *= wordp #output
                    t = prob.advprob['adv-adj']
                    adj['adv-adj'] *= t #transition
                elif p == 'adp':
                    adj['adp-adj'] = case[p]
                    if word in prob.oadjprob.keys():
                        wordp = prob.oadjprob[word]
                    else:
                        wordp = .0001/total
                    adj['adp-adj'] *= wordp #output
                    t = prob.adpprob['adp-adj']
                    adj['adp-adj'] *= t #transition
                elif p == 'conj':
                    adj['conj-adj'] = case[p]
                    if word in prob.oadjprob.keys():
                        wordp = prob.oadjprob[word]
                    else:
                        wordp = .0001/total
                    adj['conj-adj'] *= wordp #output
                    t = prob.conjprob['conj-adj']
                    adj['conj-adj'] *= t #transition
                elif p == 'det':
                    adj['det-adj'] = case[p]
                    if word in prob.oadjprob.keys():
                        wordp = prob.oadjprob[word]
                    else:
                        wordp = .0001/total
                    adj['det-adj'] *= wordp #output
                    t = prob.detprob['det-adj']
                    adj['det-adj'] *= t #transition
                elif p == 'num':
                    adj['num-adj'] = case[p]
                    if word in prob.oadjprob.keys():
                        wordp = prob.oadjprob[word]
                    else:
                        wordp = .0001/total
                    adj['num-adj'] *= wordp #output
                    t = prob.numprob['num-adj']
                    adj['num-adj'] *= t #transition
                elif p == 'pron':
                    adj['pron-adj'] = case[p]
                    if word in prob.oadjprob.keys():
                        wordp = prob.oadjprob[word]
                    else:
                        wordp = .0001/total
                    adj['pron-adj'] *= wordp #output
                    t = prob.pronprob['pron-adj']
                    adj['pron-adj'] *= t #transition
                elif p == 'prt':
                    adj['prt-adj'] = case[p]
                    if word in prob.oadjprob.keys():
                        wordp = prob.oadjprob[word]
                    else:
                        wordp = .0001/total
                    adj['prt-adj'] *= wordp #output
                    t = prob.prtprob['prt-adj']
                    adj['prt-adj'] *= t #transition
                elif p == 'x':
                    adj['X-adj'] = case[p]
                    if word in prob.oadjprob.keys():
                        wordp = prob.oadjprob[word]
                    else:
                        wordp = .0001/total
                    adj['X-adj'] *= wordp #output
                    t = prob.Xprob['X-adj']
                    adj['X-adj'] *= t #transition
                elif p == '.':
                    adj['.-adj'] = case[p]
                    if word in prob.oadjprob.keys()       :
                        wordp = prob.oadjprob[word]
                    else:
                        wordp = .0001/total
                    adj['.-adj'] *= wordp #output
                    t = prob.punctprob['.-adj']
                    adj['.-adj'] *= t #transition
        if pos == 'adv':
            for p in sent[newtime-1]:
                case = sent[newtime-1]
                if p == 'noun':
                    adv['n-adv'] = case[p] # previous
                    if word in prob.oadvprob.keys():
                        wordp = prob.oadvprob[word]
                    else:
                        wordp = .0001/total
                    adv['n-adv'] *= wordp #output
                    t = prob.nounprob['n-adv']
                    adv['n-adv'] *= t #transition
                elif p == 'verb':
                    adv['v-adv'] = case[p]
                    if word in prob.oadvprob.keys():
                        wordp = prob.oadvprob[word]
                    else:
                        wordp = .0001/total
                    adv['v-adv'] *= wordp #output
                    t = prob.verbprob['v-adv']
                    adv['v-adv'] *= t #transition
                elif p == 'adj':
                    adv['adj-adv'] = case[p]
                    if word in prob.oadvprob.keys():
                        wordp = prob.oadvprob[word]
                    else:
                        wordp = .0001/total
                    adv['adj-adv'] *= wordp #output
                    t = prob.adjprob['adj-adv']
                    adv['adj-adv'] *= t #transition
                elif p == 'adv':
                    adv['adv-adv'] = case[p]
                    if word in prob.oadvprob.keys():
                        wordp = prob.oadvprob[word]
                    else:
                        wordp = .0001/total
                    adv['adv-adv'] *= wordp #output
                    t = prob.advprob['adv-adv']
                    adv['adv-adv'] *= t #transition
                elif p == 'adp':
                    adv['adp-adv'] = case[p]
                    if word in prob.oadvprob.keys():
                        wordp = prob.oadvprob[word]
                    else:
                        wordp = .0001/total
                    adv['adp-adv'] *= wordp #output
                    t = prob.adpprob['adp-adv']
                    adv['adp-adv'] *= t #transition
                elif p == 'conj':
                    adv['conj-adv'] = case[p]
                    if word in prob.oadvprob.keys():
                        wordp = prob.oadvprob[word]
                    else:
                        wordp = .0001/total
                    adv['conj-adv'] *= wordp #output
                    t = prob.conjprob['conj-adv']
                    adv['conj-adv'] *= t #transition
                elif p == 'det':
                    adv['det-adv'] = case[p]
                    if word in prob.oadvprob.keys():
                        wordp = prob.oadvprob[word]
                    else:
                        wordp = .0001/total
                    adv['det-adv'] *= wordp #output
                    t = prob.detprob['det-adv']
                    adv['det-adv'] *= t #transition
                elif p == 'num':
                    adv['num-adv'] = case[p]
                    if word in prob.oadvprob.keys():
                        wordp = prob.oadvprob[word]
                    else:
                        wordp = .0001/total
                    adv['num-adv'] *= wordp #output
                    t = prob.numprob['num-adv']
                    adv['num-adv'] *= t #transition
                elif p == 'pron':
                    adv['pron-adv'] = case[p]
                    if word in prob.oadvprob.keys():
                        wordp = prob.oadvprob[word]
                    else:
                        wordp = .0001/total
                    adv['pron-adv'] *= wordp #output
                    t = prob.pronprob['pron-adv']
                    adv['pron-adv'] *= t #transition
                elif p == 'prt':
                    adv['prt-adv'] = case[p]
                    if word in prob.oadvprob.keys():
                        wordp = prob.oadvprob[word]
                    else:
                        wordp = .0001/total
                    adv['prt-adv'] *= wordp #output
                    t = prob.prtprob['prt-adv']
                    adv['prt-adv'] *= t #transition
                elif p == 'x':
                    adv['X-adv'] = case[p]
                    if word in prob.oadvprob.keys():
                        wordp = prob.oadvprob[word]
                    else:
                        wordp = .0001/total
                    adv['X-adv'] *= wordp #output
                    t = prob.Xprob['X-adv']
                    adv['X-adv'] *= t #transition
                elif p == '.':
                    adv['.-adv'] = case[p]
                    if word in prob.oadvprob.keys()       :
                        wordp = prob.oadvprob[word]
                    else:
                        wordp = .0001/total
                    adv['.-adv'] *= wordp #output
                    t = prob.punctprob['.-adv']
                    adv['.-adv'] *= t #transition
        if pos == 'adp':
            for p in sent[newtime-1]:
                case = sent[newtime-1]
                if p == 'noun':
                    adp['n-adp'] = case[p] # previous
                    if word in prob.oadpprob.keys():
                        wordp = prob.oadpprob[word]
                    else:
                        wordp = .0001/total
                    adp['n-adp'] *= wordp #output
                    t = prob.nounprob['n-adp']
                    adp['n-adp'] *= t #transition
                elif p == 'verb':
                    adp['v-adp'] = case[p]
                    if word in prob.oadpprob.keys():
                        wordp = prob.oadpprob[word]
                    else:
                        wordp = .0001/total
                    adp['v-adp'] *= wordp #output
                    t = prob.verbprob['v-adp']
                    adp['v-adp'] *= t #transition
                elif p == 'adj':
                    adp['adj-adp'] = case[p]
                    if word in prob.oadpprob.keys():
                        wordp = prob.oadpprob[word]
                    else:
                        wordp = .0001/total
                    adp['adj-adp'] *= wordp #output
                    t = prob.adjprob['adj-adp']
                    adp['adj-adp'] *= t #transition
                elif p == 'adv':
                    adp['adv-adp'] = case[p]
                    if word in prob.oadpprob.keys():
                        wordp = prob.oadpprob[word]
                    else:
                        wordp = .0001/total
                    adp['adv-adp'] *= wordp #output
                    t = prob.advprob['adv-adp']
                    adp['adv-adp'] *= t #transition
                elif p == 'adp':
                    adp['adp-adp'] = case[p]
                    if word in prob.oadpprob.keys():
                        wordp = prob.oadpprob[word]
                    else:
                        wordp = .0001/total
                    adp['adp-adp'] *= wordp #output
                    t = prob.adpprob['adp-adp']
                    adp['adp-adp'] *= t #transition
                elif p == 'conj':
                    adp['conj-adp'] = case[p]
                    if word in prob.oadpprob.keys():
                        wordp = prob.oadpprob[word]
                    else:
                        wordp = .0001/total
                    adp['conj-adp'] *= wordp #output
                    t = prob.conjprob['conj-adp']
                    adp['conj-adp'] *= t #transition
                elif p == 'det':
                    adp['det-adp'] = case[p]
                    if word in prob.oadpprob.keys():
                        wordp = prob.oadpprob[word]
                    else:
                        wordp = .0001/total
                    adp['det-adp'] *= wordp #output
                    t = prob.detprob['det-adp']
                    adp['det-adp'] *= t #transition
                elif p == 'num':
                    adp['num-adp'] = case[p]
                    if word in prob.oadpprob.keys():
                        wordp = prob.oadpprob[word]
                    else:
                        wordp = .0001/total
                    adp['num-adp'] *= wordp #output
                    t = prob.numprob['num-adp']
                    adp['num-adp'] *= t #transition
                elif p == 'pron':
                    adp['pron-adp'] = case[p]
                    if word in prob.oadpprob.keys():
                        wordp = prob.oadpprob[word]
                    else:
                        wordp = .0001/total
                    adp['pron-adp'] *= wordp #output
                    t = prob.pronprob['pron-adp']
                    adp['pron-adp'] *= t #transition
                elif p == 'prt':
                    adp['prt-adp'] = case[p]
                    if word in prob.oadpprob.keys():
                        wordp = prob.oadpprob[word]
                    else:
                        wordp = .0001/total
                    adp['prt-adp'] *= wordp #output
                    t = prob.prtprob['prt-adp']
                    adp['prt-adp'] *= t #transition
                elif p == 'x':
                    adp['X-adp'] = case[p]
                    if word in prob.oadpprob.keys():
                        wordp = prob.oadpprob[word]
                    else:
                        wordp = .0001/total
                    adp['X-adp'] *= wordp #output
                    t = prob.Xprob['X-adp']
                    adp['X-adp'] *= t #transition
                elif p == '.':
                    adp['.-adp'] = case[p]
                    if word in prob.oadpprob.keys()       :
                        wordp = prob.oadpprob[word]
                    else:
                        wordp = .0001/total
                    adp['.-adp'] *= wordp #output
                    t = prob.punctprob['.-adp']
                    adp['.-adp'] *= t #transition
        if pos == 'conj':
            for p in sent[newtime-1]:
                case = sent[newtime-1]
                if p == 'noun':
                    conj['n-conj'] = case[p] # previous
                    if word in prob.oconjprob.keys():
                        wordp = prob.oconjprob[word]
                    else:
                        wordp = .0001/total
                    conj['n-conj'] *= wordp #output
                    t = prob.nounprob['n-conj']
                    conj['n-conj'] *= t #transition
                elif p == 'verb':
                    conj['v-conj'] = case[p]
                    if word in prob.oconjprob.keys():
                        wordp = prob.oconjprob[word]
                    else:
                        wordp = .0001/total
                    conj['v-conj'] *= wordp #output
                    t = prob.verbprob['v-conj']
                    conj['v-conj'] *= t #transition
                elif p == 'adj':
                    conj['adj-conj'] = case[p]
                    if word in prob.oconjprob.keys():
                        wordp = prob.oconjprob[word]
                    else:
                        wordp = .0001/total
                    conj['adj-conj'] *= wordp #output
                    t = prob.adjprob['adj-conj']
                    conj['adj-conj'] *= t #transition
                elif p == 'adv':
                    conj['adv-conj'] = case[p]
                    if word in prob.oconjprob.keys():
                        wordp = prob.oconjprob[word]
                    else:
                        wordp = .0001/total
                    conj['adv-conj'] *= wordp #output
                    t = prob.advprob['adv-conj']
                    conj['adv-conj'] *= t #transition
                elif p == 'adp':
                    conj['adp-conj'] = case[p]
                    if word in prob.oconjprob.keys():
                        wordp = prob.oconjprob[word]
                    else:
                        wordp = .0001/total
                    conj['adp-conj'] *= wordp #output
                    t = prob.adpprob['adp-conj']
                    conj['adp-conj'] *= t #transition
                elif p == 'conj':
                    conj['conj-conj'] = case[p]
                    if word in prob.oconjprob.keys():
                        wordp = prob.oconjprob[word]
                    else:
                        wordp = .0001/total
                    conj['conj-conj'] *= wordp #output
                    t = prob.conjprob['conj-conj']
                    conj['conj-conj'] *= t #transition
                elif p == 'det':
                    conj['det-conj'] = case[p]
                    if word in prob.oconjprob.keys():
                        wordp = prob.oconjprob[word]
                    else:
                        wordp = .0001/total
                    conj['det-conj'] *= wordp #output
                    t = prob.detprob['det-conj']
                    conj['det-conj'] *= t #transition
                elif p == 'num':
                    conj['num-conj'] = case[p]
                    if word in prob.oconjprob.keys():
                        wordp = prob.oconjprob[word]
                    else:
                        wordp = .0001/total
                    conj['num-conj'] *= wordp #output
                    t = prob.numprob['num-conj']
                    conj['num-conj'] *= t #transition
                elif p == 'pron':
                    conj['pron-conj'] = case[p]
                    if word in prob.oconjprob.keys():
                        wordp = prob.oconjprob[word]
                    else:
                        wordp = .0001/total
                    conj['pron-conj'] *= wordp #output
                    t = prob.pronprob['pron-conj']
                    conj['pron-conj'] *= t #transition
                elif p == 'prt':
                    conj['prt-conj'] = case[p]
                    if word in prob.oconjprob.keys():
                        wordp = prob.oconjprob[word]
                    else:
                        wordp = .0001/total
                    conj['prt-conj'] *= wordp #output
                    t = prob.prtprob['prt-conj']
                    conj['prt-conj'] *= t #transition
                elif p == 'x':
                    conj['X-conj'] = case[p]
                    if word in prob.oconjprob.keys():
                        wordp = prob.oconjprob[word]
                    else:
                        wordp = .0001/total
                    conj['X-conj'] *= wordp #output
                    t = prob.Xprob['X-conj']
                    conj['X-conj'] *= t #transition
                elif p == '.':
                    conj['.-conj'] = case[p]
                    if word in prob.oconjprob.keys()       :
                        wordp = prob.oconjprob[word]
                    else:
                        wordp = .0001/total
                    conj['.-conj'] *= wordp #output
                    t = prob.punctprob['.-conj']
                    conj['.-conj'] *= t #transition
        if pos == 'det':
            for p in sent[newtime-1]:
                case = sent[newtime-1]
                if p == 'noun':
                    det['n-det'] = case[p] # previous
                    if word in prob.odetprob.keys():
                        wordp = prob.odetprob[word]
                    else:
                        wordp = .0001/total
                    det['n-det'] *= wordp #output
                    t = prob.nounprob['n-det']
                    det['n-det'] *= t #transition
                elif p == 'verb':
                    det['v-det'] = case[p]
                    if word in prob.odetprob.keys():
                        wordp = prob.odetprob[word]
                    else:
                        wordp = .0001/total
                    det['v-det'] *= wordp #output
                    t = prob.verbprob['v-det']
                    det['v-det'] *= t #transition
                elif p == 'adj':
                    det['adj-det'] = case[p]
                    if word in prob.odetprob.keys():
                        wordp = prob.odetprob[word]
                    else:
                        wordp = .0001/total
                    det['adj-det'] *= wordp #output
                    t = prob.adjprob['adj-det']
                    det['adj-det'] *= t #transition
                elif p == 'adv':
                    det['adv-det'] = case[p]
                    if word in prob.odetprob.keys():
                        wordp = prob.odetprob[word]
                    else:
                        wordp = .0001/total
                    det['adv-det'] *= wordp #output
                    t = prob.advprob['adv-det']
                    det['adv-det'] *= t #transition
                elif p == 'adp':
                    det['adp-det'] = case[p]
                    if word in prob.odetprob.keys():
                        wordp = prob.odetprob[word]
                    else:
                        wordp = .0001/total
                    det['adp-det'] *= wordp #output
                    t = prob.adpprob['adp-det']
                    det['adp-det'] *= t #transition
                elif p == 'conj':
                    det['conj-det'] = case[p]
                    if word in prob.odetprob.keys():
                        wordp = prob.odetprob[word]
                    else:
                        wordp = .0001/total
                    det['conj-det'] *= wordp #output
                    t = prob.conjprob['conj-det']
                    det['conj-det'] *= t #transition
                elif p == 'det':
                    det['det-det'] = case[p]
                    if word in prob.odetprob.keys():
                        wordp = prob.odetprob[word]
                    else:
                        wordp = .0001/total
                    det['det-det'] *= wordp #output
                    t = prob.detprob['det-det']
                    det['det-det'] *= t #transition
                elif p == 'num':
                    det['num-det'] = case[p]
                    if word in prob.odetprob.keys():
                        wordp = prob.odetprob[word]
                    else:
                        wordp = .0001/total
                    det['num-det'] *= wordp #output
                    t = prob.numprob['num-det']
                    det['num-det'] *= t #transition
                elif p == 'pron':
                    det['pron-det'] = case[p]
                    if word in prob.odetprob.keys():
                        wordp = prob.odetprob[word]
                    else:
                        wordp = .0001/total
                    det['pron-det'] *= wordp #output
                    t = prob.pronprob['pron-det']
                    det['pron-det'] *= t #transition
                elif p == 'prt':
                    det['prt-det'] = case[p]
                    if word in prob.odetprob.keys():
                        wordp = prob.odetprob[word]
                    else:
                        wordp = .0001/total
                    det['prt-det'] *= wordp #output
                    t = prob.prtprob['prt-det']
                    det['prt-det'] *= t #transition
                elif p == 'x':
                    det['X-det'] = case[p]
                    if word in prob.odetprob.keys():
                        wordp = prob.odetprob[word]
                    else:
                        wordp = .0001/total
                    det['X-det'] *= wordp #output
                    t = prob.Xprob['X-det']
                    det['X-det'] *= t #transition
                elif p == '.':
                    det['.-det'] = case[p]
                    if word in prob.odetprob.keys()       :
                        wordp = prob.odetprob[word]
                    else:
                        wordp = .0001/total
                    det['.-det'] *= wordp #output
                    t = prob.punctprob['.-det']
                    det['.-det'] *= t #transition
        if pos == 'num':
            for p in sent[newtime-1]:
                case = sent[newtime-1]
                if p == 'noun':
                    num['n-num'] = case[p] # previous
                    if word in prob.onumprob.keys():
                        wordp = prob.onumprob[word]
                    else:
                        wordp = .0001/total
                    num['n-num'] *= wordp #output
                    t = prob.nounprob['n-num']
                    num['n-num'] *= t #transition
                elif p == 'verb':
                    num['v-num'] = case[p]
                    if word in prob.onumprob.keys():
                        wordp = prob.onumprob[word]
                    else:
                        wordp = .0001/total
                    num['v-num'] *= wordp #output
                    t = prob.verbprob['v-num']
                    num['v-num'] *= t #transition
                elif p == 'adj':
                    num['adj-num'] = case[p]
                    if word in prob.onumprob.keys():
                        wordp = prob.onumprob[word]
                    else:
                        wordp = .0001/total
                    num['adj-num'] *= wordp #output
                    t = prob.adjprob['adj-num']
                    num['adj-num'] *= t #transition
                elif p == 'adv':
                    num['adv-num'] = case[p]
                    if word in prob.onumprob.keys():
                        wordp = prob.onumprob[word]
                    else:
                        wordp = .0001/total
                    num['adv-num'] *= wordp #output
                    t = prob.advprob['adv-num']
                    num['adv-num'] *= t #transition
                elif p == 'adp':
                    num['adp-num'] = case[p]
                    if word in prob.onumprob.keys():
                        wordp = prob.onumprob[word]
                    else:
                        wordp = .0001/total
                    num['adp-num'] *= wordp #output
                    t = prob.adpprob['adp-num']
                    num['adp-num'] *= t #transition
                elif p == 'conj':
                    num['conj-num'] = case[p]
                    if word in prob.onumprob.keys():
                        wordp = prob.onumprob[word]
                    else:
                        wordp = .0001/total
                    num['conj-num'] *= wordp #output
                    t = prob.conjprob['conj-num']
                    num['conj-num'] *= t #transition
                elif p == 'det':
                    num['det-num'] = case[p]
                    if word in prob.onumprob.keys():
                        wordp = prob.onumprob[word]
                    else:
                        wordp = .0001/total
                    num['det-num'] *= wordp #output
                    t = prob.detprob['det-num']
                    num['det-num'] *= t #transition
                elif p == 'num':
                    num['num-num'] = case[p]
                    if word in prob.onumprob.keys():
                        wordp = prob.onumprob[word]
                    else:
                        wordp = .0001/total
                    num['num-num'] *= wordp #output
                    t = prob.numprob['num-num']
                    num['num-num'] *= t #transition
                elif p == 'pron':
                    num['pron-num'] = case[p]
                    if word in prob.onumprob.keys():
                        wordp = prob.onumprob[word]
                    else:
                        wordp = .0001/total
                    num['pron-num'] *= wordp #output
                    t = prob.pronprob['pron-num']
                    num['pron-num'] *= t #transition
                elif p == 'prt':
                    num['prt-num'] = case[p]
                    if word in prob.onumprob.keys():
                        wordp = prob.onumprob[word]
                    else:
                        wordp = .0001/total
                    num['prt-num'] *= wordp #output
                    t = prob.prtprob['prt-num']
                    num['prt-num'] *= t #transition
                elif p == 'x':
                    num['X-num'] = case[p]
                    if word in prob.onumprob.keys():
                        wordp = prob.onumprob[word]
                    else:
                        wordp = .0001/total
                    num['X-num'] *= wordp #output
                    t = prob.Xprob['X-num']
                    num['X-num'] *= t #transition
                elif p == '.':
                    num['.-num'] = case[p]
                    if word in prob.onumprob.keys()       :
                        wordp = prob.onumprob[word]
                    else:
                        wordp = .0001/total
                    num['.-num'] *= wordp #output
                    t = prob.punctprob['.-num']
                    num['.-num'] *= t #transition
        if pos == 'pron':
            for p in sent[newtime-1]:
                case = sent[newtime-1]
                if p == 'noun':
                    pron['n-pron'] = case[p] # previous
                    if word in prob.opronprob.keys():
                        wordp = prob.opronprob[word]
                    else:
                        wordp = .0001/total
                    pron['n-pron'] *= wordp #output
                    t = prob.nounprob['n-pron']
                    pron['n-pron'] *= t #transition
                elif p == 'verb':
                    pron['v-pron'] = case[p]
                    if word in prob.opronprob.keys():
                        wordp = prob.opronprob[word]
                    else:
                        wordp = .0001/total
                    pron['v-pron'] *= wordp #output
                    t = prob.verbprob['v-pron']
                    pron['v-pron'] *= t #transition
                elif p == 'adj':
                    pron['adj-pron'] = case[p]
                    if word in prob.opronprob.keys():
                        wordp = prob.opronprob[word]
                    else:
                        wordp = .0001/total
                    pron['adj-pron'] *= wordp #output
                    t = prob.adjprob['adj-pron']
                    pron['adj-pron'] *= t #transition
                elif p == 'adv':
                    pron['adv-pron'] = case[p]
                    if word in prob.opronprob.keys():
                        wordp = prob.opronprob[word]
                    else:
                        wordp = .0001/total
                    pron['adv-pron'] *= wordp #output
                    t = prob.advprob['adv-pron']
                    pron['adv-pron'] *= t #transition
                elif p == 'adp':
                    pron['adp-pron'] = case[p]
                    if word in prob.opronprob.keys():
                        wordp = prob.opronprob[word]
                    else:
                        wordp = .0001/total
                    pron['adp-pron'] *= wordp #output
                    t = prob.adpprob['adp-pron']
                    pron['adp-pron'] *= t #transition
                elif p == 'conj':
                    pron['conj-pron'] = case[p]
                    if word in prob.opronprob.keys():
                        wordp = prob.opronprob[word]
                    else:
                        wordp = .0001/total
                    pron['conj-pron'] *= wordp #output
                    t = prob.conjprob['conj-pron']
                    pron['conj-pron'] *= t #transition
                elif p == 'det':
                    pron['det-pron'] = case[p]
                    if word in prob.opronprob.keys():
                        wordp = prob.opronprob[word]
                    else:
                        wordp = .0001/total
                    pron['det-pron'] *= wordp #output
                    t = prob.detprob['det-pron']
                    pron['det-pron'] *= t #transition
                elif p == 'num':
                    pron['num-pron'] = case[p]
                    if word in prob.opronprob.keys():
                        wordp = prob.opronprob[word]
                    else:
                        wordp = .0001/total
                    pron['num-pron'] *= wordp #output
                    t = prob.numprob['num-pron']
                    pron['num-pron'] *= t #transition
                elif p == 'pron':
                    pron['pron-pron'] = case[p]
                    if word in prob.opronprob.keys():
                        wordp = prob.opronprob[word]
                    else:
                        wordp = .0001/total
                    pron['pron-pron'] *= wordp #output
                    t = prob.pronprob['pron-pron']
                    pron['pron-pron'] *= t #transition
                elif p == 'prt':
                    pron['prt-pron'] = case[p]
                    if word in prob.opronprob.keys():
                        wordp = prob.opronprob[word]
                    else:
                        wordp = .0001/total
                    pron['prt-pron'] *= wordp #output
                    t = prob.prtprob['prt-pron']
                    pron['prt-pron'] *= t #transition
                elif p == 'x':
                    pron['X-pron'] = case[p]
                    if word in prob.opronprob.keys():
                        wordp = prob.opronprob[word]
                    else:
                        wordp = .0001/total
                    pron['X-pron'] *= wordp #output
                    t = prob.Xprob['X-pron']
                    pron['X-pron'] *= t #transition
                elif p == '.':
                    pron['.-pron'] = case[p]
                    if word in prob.opronprob.keys()       :
                        wordp = prob.opronprob[word]
                    else:
                        wordp = .0001/total
                    pron['.-pron'] *= wordp #output
                    t = prob.punctprob['.-pron']
                    pron['.-pron'] *= t #transition
        if pos == 'prt':
            for p in sent[newtime-1]:
                case = sent[newtime-1]
                if p == 'noun':
                    prt['n-prt'] = case[p] # previous
                    if word in prob.oprtprob.keys():
                        wordp = prob.oprtprob[word]
                    else:
                        wordp = .0001/total
                    prt['n-prt'] *= wordp #output
                    t = prob.nounprob['n-prt']
                    prt['n-prt'] *= t #transition
                elif p == 'verb':
                    prt['v-prt'] = case[p]
                    if word in prob.oprtprob.keys():
                        wordp = prob.oprtprob[word]
                    else:
                        wordp = .0001/total
                    prt['v-prt'] *= wordp #output
                    t = prob.verbprob['v-prt']
                    prt['v-prt'] *= t #transition
                elif p == 'adj':
                    prt['adj-prt'] = case[p]
                    if word in prob.oprtprob.keys():
                        wordp = prob.oprtprob[word]
                    else:
                        wordp = .0001/total
                    prt['adj-prt'] *= wordp #output
                    t = prob.adjprob['adj-prt']
                    prt['adj-prt'] *= t #transition
                elif p == 'adv':
                    prt['adv-prt'] = case[p]
                    if word in prob.oprtprob.keys():
                        wordp = prob.oprtprob[word]
                    else:
                        wordp = .0001/total
                    prt['adv-prt'] *= wordp #output
                    t = prob.advprob['adv-prt']
                    prt['adv-prt'] *= t #transition
                elif p == 'adp':
                    prt['adp-prt'] = case[p]
                    if word in prob.oprtprob.keys():
                        wordp = prob.oprtprob[word]
                    else:
                        wordp = .0001/total
                    prt['adp-prt'] *= wordp #output
                    t = prob.adpprob['adp-prt']
                    prt['adp-prt'] *= t #transition
                elif p == 'conj':
                    prt['conj-prt'] = case[p]
                    if word in prob.oprtprob.keys():
                        wordp = prob.oprtprob[word]
                    else:
                        wordp = .0001/total
                    prt['conj-prt'] *= wordp #output
                    t = prob.conjprob['conj-prt']
                    prt['conj-prt'] *= t #transition
                elif p == 'det':
                    prt['det-prt'] = case[p]
                    if word in prob.oprtprob.keys():
                        wordp = prob.oprtprob[word]
                    else:
                        wordp = .0001/total
                    prt['det-prt'] *= wordp #output
                    t = prob.detprob['det-prt']
                    prt['det-prt'] *= t #transition
                elif p == 'num':
                    prt['num-prt'] = case[p]
                    if word in prob.oprtprob.keys():
                        wordp = prob.oprtprob[word]
                    else:
                        wordp = .0001/total
                    prt['num-prt'] *= wordp #output
                    t = prob.numprob['num-prt']
                    prt['num-prt'] *= t #transition
                elif p == 'pron':
                    prt['pron-prt'] = case[p]
                    if word in prob.oprtprob.keys():
                        wordp = prob.oprtprob[word]
                    else:
                        wordp = .0001/total
                    prt['pron-prt'] *= wordp #output
                    t = prob.pronprob['pron-prt']
                    prt['pron-prt'] *= t #transition
                elif p == 'prt':
                    prt['prt-prt'] = case[p]
                    if word in prob.oprtprob.keys():
                        wordp = prob.oprtprob[word]
                    else:
                        wordp = .0001/total
                    prt['prt-prt'] *= wordp #output
                    t = prob.prtprob['prt-prt']
                    prt['prt-prt'] *= t #transition
                elif p == 'x':
                    prt['X-prt'] = case[p]
                    if word in prob.oprtprob.keys():
                        wordp = prob.oprtprob[word]
                    else:
                        wordp = .0001/total
                    prt['X-prt'] *= wordp #output
                    t = prob.Xprob['X-prt']
                    prt['X-prt'] *= t #transition
                elif p == '.':
                    prt['.-prt'] = case[p]
                    if word in prob.oprtprob.keys()       :
                        wordp = prob.oprtprob[word]
                    else:
                        wordp = .0001/total
                    prt['.-prt'] *= wordp #output
                    t = prob.punctprob['.-prt']
                    prt['.-prt'] *= t #transition
        if pos == 'x':
            for p in sent[newtime-1]:
                case = sent[newtime-1]
                if p == 'noun':
                    x['n-X'] = case[p] # previous
                    if word in prob.oXprob.keys():
                        wordp = prob.oXprob[word]
                    else:
                        wordp = .0001/total
                    x['n-X'] *= wordp #output
                    t = prob.nounprob['n-X']
                    x['n-X'] *= t #transition
                elif p == 'verb':
                    x['v-X'] = case[p]
                    if word in prob.oXprob.keys():
                        wordp = prob.oXprob[word]
                    else:
                        wordp = .0001/total
                    x['v-X'] *= wordp #output
                    t = prob.verbprob['v-X']
                    x['v-X'] *= t #transition
                elif p == 'adj':
                    x['adj-X'] = case[p]
                    if word in prob.oXprob.keys():
                        wordp = prob.oXprob[word]
                    else:
                        wordp = .0001/total
                    x['adj-X'] *= wordp #output
                    t = prob.adjprob['adj-X']
                    x['adj-X'] *= t #transition
                elif p == 'adv':
                    x['adv-X'] = case[p]
                    if word in prob.oXprob.keys():
                        wordp = prob.oXprob[word]
                    else:
                        wordp = .0001/total
                    x['adv-X'] *= wordp #output
                    t = prob.advprob['adv-X']
                    x['adv-X'] *= t #transition
                elif p == 'adp':
                    x['adp-X'] = case[p]
                    if word in prob.oXprob.keys():
                        wordp = prob.oXprob[word]
                    else:
                        wordp = .0001/total
                    x['adp-X'] *= wordp #output
                    t = prob.adpprob['adp-X']
                    x['adp-X'] *= t #transition
                elif p == 'conj':
                    x['conj-X'] = case[p]
                    if word in prob.oXprob.keys():
                        wordp = prob.oXprob[word]
                    else:
                        wordp = .0001/total
                    x['conj-X'] *= wordp #output
                    t = prob.conjprob['conj-X']
                    x['conj-X'] *= t #transition
                elif p == 'det':
                    x['det-X'] = case[p]
                    if word in prob.oXprob.keys():
                        wordp = prob.oXprob[word]
                    else:
                        wordp = .0001/total
                    x['det-X'] *= wordp #output
                    t = prob.detprob['det-X']
                    x['det-X'] *= t #transition
                elif p == 'num':
                    x['num-X'] = case[p]
                    if word in prob.oXprob.keys():
                        wordp = prob.oXprob[word]
                    else:
                        wordp = .0001/total
                    x['num-X'] *= wordp #output
                    t = prob.numprob['num-X']
                    x['num-X'] *= t #transition
                elif p == 'pron':
                    x['pron-X'] = case[p]
                    if word in prob.oXprob.keys():
                        wordp = prob.oXprob[word]
                    else:
                        wordp = .0001/total
                    x['pron-X'] *= wordp #output
                    t = prob.pronprob['pron-X']
                    x['pron-X'] *= t #transition
                elif p == 'prt':
                    x['prt-X'] = case[p]
                    if word in prob.oXprob.keys():
                        wordp = prob.oXprob[word]
                    else:
                        wordp = .0001/total
                    x['prt-X'] *= wordp #output
                    t = prob.prtprob['prt-X']
                    x['prt-X'] *= t #transition
                elif p == 'x':
                    x['X-X'] = case[p]
                    if word in prob.oXprob.keys():
                        wordp = prob.oXprob[word]
                    else:
                        wordp = .0001/total
                    x['X-X'] *= wordp #output
                    t = prob.Xprob['X-X']
                    x['X-X'] *= t #transition
                elif p == '.':
                    x['.-X'] = case[p]
                    if word in prob.oXprob.keys()       :
                        wordp = prob.oXprob[word]
                    else:
                        wordp = .0001/total
                    x['.-X'] *= wordp #output
                    t = prob.punctprob['.-X']
                    x['.-X'] *= t #transition
        if pos == '.':
            for p in sent[newtime-1]:
                case = sent[newtime-1]
                if p == 'noun':
                    pun['n-.'] = case[p] # previous
                    if word in prob.opunctprob.keys():
                        wordp = prob.opunctprob[word]
                    else:
                        wordp = .0001/total
                    pun['n-.'] *= wordp #output
                    t = prob.nounprob['n-.']
                    pun['n-.'] *= t #transition
                elif p == 'verb':
                    pun['v-.'] = case[p]
                    if word in prob.opunctprob.keys():
                        wordp = prob.opunctprob[word]
                    else:
                        wordp = .0001/total
                    pun['v-.'] *= wordp #output
                    t = prob.verbprob['v-.']
                    pun['v-.'] *= t #transition
                elif p == 'adj':
                    pun['adj-.'] = case[p]
                    if word in prob.opunctprob.keys():
                        wordp = prob.opunctprob[word]
                    else:
                        wordp = .0001/total
                    pun['adj-.'] *= wordp #output
                    t = prob.adjprob['adj-.']
                    pun['adj-.'] *= t #transition
                elif p == 'adv':
                    pun['adv-.'] = case[p]
                    if word in prob.opunctprob.keys():
                        wordp = prob.opunctprob[word]
                    else:
                        wordp = .0001/total
                    pun['adv-.'] *= wordp #output
                    t = prob.advprob['adv-.']
                    pun['adv-.'] *= t #transition
                elif p == 'adp':
                    pun['adp-.'] = case[p]
                    if word in prob.opunctprob.keys():
                        wordp = prob.opunctprob[word]
                    else:
                        wordp = .0001/total
                    pun['adp-.'] *= wordp #output
                    t = prob.adpprob['adp-.']
                    pun['adp-.'] *= t #transition
                elif p == 'conj':
                    pun['conj-.'] = case[p]
                    if word in prob.opunctprob.keys():
                        wordp = prob.opunctprob[word]
                    else:
                        wordp = .0001/total
                    pun['conj-.'] *= wordp #output
                    t = prob.conjprob['conj-.']
                    pun['conj-.'] *= t #transition
                elif p == 'det':
                    pun['det-.'] = case[p]
                    if word in prob.opunctprob.keys():
                        wordp = prob.opunctprob[word]
                    else:
                        wordp = .0001/total
                    pun['det-.'] *= wordp #output
                    t = prob.detprob['det-.']
                    pun['det-.'] *= t #transition
                elif p == 'num':
                    pun['num-.'] = case[p]
                    if word in prob.opunctprob.keys():
                        wordp = prob.opunctprob[word]
                    else:
                        wordp = .0001/total
                    pun['num-.'] *= wordp #output
                    t = prob.numprob['num-.']
                    pun['num-.'] *= t #transition
                elif p == 'pron':
                    pun['pron-.'] = case[p]
                    if word in prob.opunctprob.keys():
                        wordp = prob.opunctprob[word]
                    else:
                        wordp = .0001/total
                    pun['pron-.'] *= wordp #output
                    t = prob.pronprob['pron-.']
                    pun['pron-.'] *= t #transition
                elif p == 'prt':
                    pun['prt-.'] = case[p]
                    if word in prob.opunctprob.keys():
                        wordp = prob.opunctprob[word]
                    else:
                        wordp = .0001/total
                    pun['prt-.'] *= wordp #output
                    t = prob.prtprob['prt-.']
                    pun['prt-.'] *= t #transition
                elif p == 'x':
                    pun['X-.'] = case[p]
                    if word in prob.opunctprob.keys():
                        wordp = prob.opunctprob[word]
                    else:
                        wordp = .0001/total
                    pun['X-.'] *= wordp #output
                    t = prob.Xprob['X-.']
                    pun['X-.'] *= t #transition
                elif p == '.':
                    pun['.-.'] = case[p]
                    if word in prob.opunctprob.keys()       :
                        wordp = prob.opunctprob[word]
                    else:
                        wordp = .0001/total
                    pun['.-.'] *= wordp #output
                    t = prob.punctprob['.-.']
                    pun['.-.'] *= t #transition
    ## finds largest value going into each node
    largestn = 0
    largestverb = 0
    largestadj = 0
    largestadv = 0
    largestadp = 0
    largestconj = 0
    largestdet = 0
    largestnum = 0
    largestpron = 0
    largestprt = 0
    largestx = 0
    largestpun = 0
    largest = 0
    for i in sent[newtime]:
        a = sent[newtime]
        case = a[i]
        for c in case:
            if largest == 0: 
                largest = case[c]
                tag = c
            elif case[c] > largest:
                largest = case[c]
                tag = c
        a[i] = largest
                    
def trace ():
    l = len(sent)
    path = []
    largest = 0
    tag = ''
    count = 0
    for i in range(0, l):
        for x in sent[i]:
            case = sent[i]
            if tag == '':
                tag = x
                largest = case[x]
            elif case[x] > largest:
                tag = x
                largest = case[x]
        count += 1
        path += [(largest, tag)]
        largest = 0
        tag = ''
    sent.clear()
    return path

    