import define
###########
# This file is for calculating the probabilities from the training set
###########

#####calculate start probabilities#####
startprob = {'noun': 0, 'verb':0, 'adj': 0, 'adv': 0, 'adp': 0, 'conj': 0, 'det': 0, 'num': 0, 'pron': 0, 'prt': 0, 'x': 0, '.': 0}

def probstart():
    total = 0
    for i in define.start:
        case = define.start[i]
        for c in case:
            startprob[i] += case[c] 
        total += startprob[i]
    for i in startprob:
        num = startprob[i]
        startprob[i] = num/total 


#####calculate transition probabilities#####
nounprob = {'n-n': 0, 'n-v': 0, 'n-adj': 0, 'n-adv': 0, 'n-adp':0,'n-conj':0, 'n-det': 0, 'n-num':0, 'n-pron': 0, 'n-prt':0, 'n-X': 0, 'n-.':0}
verbprob = {'v-n': 0, 'v-v': 0, 'v-adj': 0, 'v-adv': 0, 'v-adp':0, 'v-conj':0, 'v-det': 0, 'v-num':0, 'v-pron': 0, 'v-prt':0, 'v-X': 0, 'v-.':0}
adjprob = {'adj-n': 0, 'adj-v': 0, 'adj-adj': 0, 'adj-adv': 0,  'adj-adp':0,'adj-conj':0, 'adj-det': 0, 'adj-num':0, 'adj-pron': 0, 'adj-prt':0, 'adj-X': 0, 'adj-.':0}
advprob = {'adv-n': 0, 'adv-v': 0, 'adv-adj': 0, 'adv-adv': 0, 'adv-adp':0, 'adv-conj':0, 'adv-det': 0, 'adv-num':0, 'adv-pron': 0, 'adv-prt':0, 'adv-X': 0, 'adv-.':0}
adpprob = {'adp-n': 0, 'adp-v': 0, 'adp-adj': 0, 'adp-adv': 0, 'adp-adp':0, 'adp-conj':0, 'adp-det': 0, 'adp-num':0, 'adp-pron': 0, 'adp-prt':0, 'adp-X': 0, 'adp-.':0}
conjprob = {'conj-n': 0, 'conj-v': 0, 'conj-adj': 0, 'conj-adv': 0, 'conj-adp':0, 'conj-conj':0, 'conj-det': 0, 'conj-num':0, 'conj-pron': 0, 'conj-prt':0, 'conj-X': 0, 'conj-.':0}
detprob = {'det-n': 0, 'det-v': 0, 'det-adj': 0, 'det-adv': 0, 'det-adp':0, 'det-conj':0, 'det-det': 0, 'det-num':0, 'det-pron': 0, 'det-prt':0, 'det-X': 0, 'det-.':0}
numprob = {'num-n': 0, 'num-v': 0, 'num-adj': 0, 'num-adv': 0, 'num-adp':0, 'num-conj':0, 'num-det': 0, 'num-num':0, 'num-pron': 0, 'num-prt':0, 'num-X': 0, 'num-.':0}
pronprob = {'pron-n': 0, 'pron-v': 0, 'pron-adj': 0, 'pron-adv': 0, 'pron-adp':0, 'pron-conj':0, 'pron-det': 0, 'pron-num':0, 'pron-pron': 0, 'pron-prt':0, 'pron-X': 0, 'pron-.':0}
prtprob = {'prt-n': 0, 'prt-v': 0, 'prt-adj': 0, 'prt-adv': 0, 'prt-adp':0, 'prt-conj':0, 'prt-det': 0, 'prt-num':0, 'prt-pron': 0, 'prt-prt':0, 'prt-X': 0, 'prt-.':0}
Xprob = {'X-n': 0, 'X-v': 0, 'X-adj': 0, 'X-adv': 0, 'X-adp':0, 'X-conj':0, 'X-det': 0, 'X-num':0, 'X-pron': 0, 'X-prt':0, 'X-X': 0, 'X-.':0}
punctprob = {'.-n': 0, '.-v': 0, '.-adj': 0, '.-adv': 0, '.-adp':0, '.-conj':0, '.-det': 0, '.-num':0, '.-pron': 0, '.-prt':0, '.-X': 0, '.-.':0}

transition = {'noun': nounprob, 'verb': verbprob, 'adj': adjprob, 'adv': advprob, 'adp': adpprob, 'conj': conjprob, 'det': detprob, 'num': numprob, 'pron': pronprob, 'prt': prtprob, 'x': Xprob, '.': punctprob}

def probtran (): 
    totaln = 0
    totalv = 0
    totaladj = 0
    totaladv = 0 
    totaladp = 0
    totalconj = 0
    totaldet = 0
    totalnum = 0
    totalpron = 0
    totalprt = 0
    totalx = 0
    totalpun = 0
    for i in define.transition:
        case = define.transition[i]
        for c in case: 
            #print(c)
            if i == 'noun':
                nounprob[c] += case[c] 
                totaln += case[c]
            elif i == 'verb':
                verbprob[c] += case[c] 
                totalv += case[c]
            elif i == 'adj':
                adjprob[c] += case[c] 
                totaladj += case[c]
            elif i == 'adv':
                advprob[c] += case[c] 
                totaladv += case[c]
            elif i == 'adp':
                adpprob[c] += case[c] 
                totaladp += case[c]
            elif i == 'conj':
                conjprob[c] += case[c] 
                totalconj += case[c]
            elif i == 'det':
                detprob[c] += case[c] 
                totaldet += case[c]
            elif i == 'num':
                numprob[c] += case[c] 
                totalnum += case[c]
            elif i == 'pron':
                pronprob[c] += case[c] 
                totalpron += case[c]
            elif i == 'prt':
                prtprob[c] += case[c] 
                totalprt += case[c]
            elif i == 'x':
                Xprob[c] += case[c] 
                totalx += case[c]
            elif i == '.':
                punctprob[c] += case[c] 
                totalpun += case[c]
    for i in nounprob:
        num = nounprob[i]
        nounprob[i] = num/totaln
    for i in verbprob:
        num = verbprob[i]
        verbprob[i] = num/totalv
    for i in adjprob:
        num = adjprob[i]
        adjprob[i] = num/totaladj
    for i in advprob:
        num = advprob[i]
        advprob[i] = num/totaladv
    for i in adpprob:    
        num = adpprob[i]
        adpprob[i] = num/totaladp
    for i in conjprob:
        num = conjprob[i]
        conjprob[i] = num/totalconj
    for i in detprob:
        num = detprob[i]
        detprob[i] = num/totaldet
    for i in numprob:
        num = numprob[i]
        numprob[i] = num/totalnum
    for i in pronprob:
        num = pronprob[i]
        pronprob[i] = num/totalpron
    for i in prtprob:
        num = prtprob[i]
        prtprob[i] = num/totalprt
    for i in Xprob:
        num = Xprob[i]
        Xprob[i] = num/totalx
    for i in punctprob:
        num = punctprob[i]
        punctprob[i] = num/totalpun
        

#####calculate output probabilities#####
## will have to copy contents of respective dictionaries in define w/ value of 0
onounprob = {}
overbprob = {}
oadjprob = {}
oadvprob = {}
oadpprob = {}
oconjprob = {}
odetprob = {}
onumprob = {}
opronprob = {}
oprtprob = {}
oXprob = {}
opunctprob = {}
outprobs = {'noun': onounprob, 'verb': overbprob, 'adj': oadjprob, 'adv':oadvprob, 'adp':oadpprob, 'conj': oconjprob, 'det': odetprob, 'num': onumprob, 'pron':opronprob, 'prt': oprtprob, 'x': oXprob, '.': opunctprob}


def probout (): 
    totaln = 0
    totalv = 0
    totaladj = 0
    totaladv = 0 
    totaladp = 0
    totalconj = 0
    totaldet = 0
    totalnum = 0
    totalpron = 0
    totalprt = 0
    totalx = 0
    totalpun = 0
    for i in define.out:
        case = define.out[i]
        #print(case)
        for c in case: 
            if i == 'noun':
                if c not in onounprob.keys():
                    onounprob[c] = 0
                onounprob[c] += case[c] 
                totaln += case[c]
            elif i == 'verb':
                if c not in overbprob.keys():
                    overbprob[c] = 0
                overbprob[c] += case[c] 
                totalv += case[c]
            elif i == 'adj':
                if c not in oadjprob.keys():
                    oadjprob[c] = 0
                oadjprob[c] += case[c] 
                totaladj += case[c]
            elif i == 'adv':
                if c not in oadvprob.keys():
                    oadvprob[c] = 0
                oadvprob[c] += case[c] 
                totaladv += case[c]
            elif i == 'adp':
                if c not in oadpprob.keys():
                    oadpprob[c] = 0
                oadpprob[c] += case[c] 
                totaladp += case[c]
            elif i == 'conj':
                if c not in oconjprob.keys():
                    oconjprob[c] = 0
                oconjprob[c] += case[c] 
                totalconj += case[c]
            elif i == 'det':
                if c not in odetprob.keys():
                    odetprob[c] = 0
                odetprob[c] += case[c] 
                totaldet += case[c]
            elif i == 'num':
                if c not in onumprob.keys():
                    onumprob[c] = 0
                onumprob[c] += case[c] 
                totalnum += case[c]
            elif i == 'pron':
                if c not in opronprob.keys():
                    opronprob[c] = 0
                opronprob[c] += case[c] 
                totalpron += case[c]
            elif i == 'prt':
                if c not in oprtprob.keys():
                    oprtprob[c] = 0
                oprtprob[c] += case[c] 
                totalprt += case[c]
            elif i == 'x':
                if c not in oXprob.keys():
                    oXprob[c] = 0
                oXprob[c] += case[c] 
                totalx += case[c]
            elif i == '.':
                if c not in opunctprob.keys():
                    opunctprob[c] = 0
                opunctprob[c] += case[c] 
                totalpun += case[c]
    for i in onounprob:
        num = onounprob[i]
        onounprob[i] = num/totaln
    for i in overbprob:
        num = overbprob[i]
        overbprob[i] = num/totalv
    for i in oadjprob:
        num = oadjprob[i]
        oadjprob[i] = num/totaladj
    for i in oadvprob:
        num = oadvprob[i]
        oadvprob[i] = num/totaladv
    for i in oadpprob:    
        num = oadpprob[i]
        oadpprob[i] = num/totaladp
    for i in oconjprob:
        num = oconjprob[i]
        oconjprob[i] = num/totalconj
    for i in odetprob:
        num = odetprob[i]
        odetprob[i] = num/totaldet
    for i in onumprob:
        num = onumprob[i]
        onumprob[i] = num/totalnum
    for i in opronprob:
        num = opronprob[i]
        opronprob[i] = num/totalpron
    for i in oprtprob:
        num = oprtprob[i]
        oprtprob[i] = num/totalprt
    for i in oXprob:
        num = oXprob[i]
        oXprob[i] = num/totalx
    for i in opunctprob:
        num = opunctprob[i]
        opunctprob[i] = num/totalpun
    onounprob['total'] = totaln
    overbprob['total'] = totalv
    oadjprob['total'] = totaladj
    oadvprob['total'] = totaladv
    oadpprob['total'] = totaladp
    oconjprob['total'] = totalconj
    odetprob['total'] = totaldet
    onumprob['total'] = totalnum
    opronprob['total'] = totalpron
    oprtprob['total'] = totalprt
    oXprob['total'] = totalx
    opunctprob['total'] = totalpun
    global totalwords
    totalwords = totaln + totalv + totaladj + totaladv + totaladp + totalconj + totaldet + totalnum + totalpron + totalprt + totalx + totalpun
    return totalwords