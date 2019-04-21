#!/usr/bin/env python


import sys
import re
import os

def expand(str):
    #find possible errors before applying the regex
    
    #go through str left to right and find START and END indicies of strings to be expended and detect errors
    
    reg = r'\$(([_a-zA-Z][_a-zA-Z1-9]*)|(\{([_a-zA-Z][_a-zA-Z1-9]*)\})|(\{([_a-zA-Z][_a-zA-Z1-9]*)-(.*?)\})|(\{([_a-zA-Z][_a-zA-Z1-9]*)=(.*?)\}+)|(\d+)|(\{(\d+)\})|(\*))'

    #mx<-mutaully exclusive and one must exist

    #group 1 whole string following $
    #group 2 NAME                                        mx
    #group 3 ${NAME}                                     mx
    #group 4 NAME  where ${NAME}
    #group 5 {NAME-WORD}                                 mx
    #group 6 NAME where ${NAME-WORD}
    #group 7 WORD where ${NAME-WORD}
    #group 8 {NAME=WORD}                                 mx
    #group 9 NAME in case where {NAME=WORD}
    #group 10 WORD in case where {NAME=WORD}
    #group 11 N where N                                  mx
    #group 12 {N}                                        mx
    #group 13 N where {N}
    #group 14 *                                          mx


    findexp = re.findall(reg, str)
    product=r''
    remainingstr=str

    for exp in findexp:
        index = remainingstr.find(r'$'+exp[0])
        v=1
        if (index!=0):#must not be preceeded by an odd number of \\
            backslashcount=0
            for i  in range(0, index):
                if (remainingstr[i]=="\\"):
                    backslashcount+=1
                else:
                    backslashcount=0
        if (index!=0):
            if (backslashcount%2!=0):#backslashcount must be 0, 2, 4, ... even
                v=0

        if (v==1): #EXPAND exp[0] in str
            if (len(exp[1])!=0):
                expanded = os.getenv(exp[1])
                if expanded==None:
                    expanded=''
                #product = product + remainingstr[0:index]+expanded+remainingstr[(len(exp[0])+1+index):]
                product = product + remainingstr[0:index]+expanded
            if (len(exp[2])!=0):
                expanded = os.getenv(exp[3])
                if expanded==None:
                    expanded=''
                product = product + remainingstr[0:index]+expanded
                #product = product + remainingstr[0:index]+expanded+remainingstr[(len(exp[0])+1+index):]
            if (len(exp[4])!=0):
                expanded = os.getenv(exp[5])
                if expanded==None:
                    expanded = expand(exp[6])
                #product = product + remainingstr[0:index]+expanded+remainingstr[(len(exp[0])+1+index):]
                product = product + remainingstr[0:index]+expanded
            if (len(exp[7])!=0):
                expanded = os.getenv(exp[8])
                if expanded==None:
                    expanded = expand(exp[9])
                #product = product + remainingstr[0:index]+expanded+remainingstr[(len(exp[0])+1+index):]
                product = product + remainingstr[0:index]+expanded
                os.environ[exp[8]] = expanded
            if (len(exp[10])!=0):
                if (int(exp[10])>=len(sys.argv)):
                    expanded = ''
                else:
                    argc = len(sys.argv)
                    i = int(exp[10])
                    if (i >= argc):
                        expanded = ''
                    else:
                        expanded = expand(sys.argv[i])
                product = product + remainingstr[0:index]+expanded
                #product = product + remainingstr[0:index]+expanded+remainingstr[(len(exp[0])+1+index):]
            if (len(exp[11])!=0):
                if (int(exp[12])>=len(sys.argv)):
                    expanded = ''
                else:
                    expanded = expand(sys.argv(int(exp[12])))
                #product = product + remainingstr[0:index]+expanded+remainingstr[(len(exp[0])+1):]
                product = product + remainingstr[0:index]+expanded
            if (len(exp[13])!=0):
                expanded=''
                for j in range(1, len(sys.argv)):
                    if (j!=1):
                        expanded = expanded + " " + expand(sys.argv[j])
                    else:
                        expanded = expanded + expand(sys.argv[j])
                product = product + remainingstr[0:index]+expanded
        else: #v==0 presumably
            product = product + remainingstr[0:(index+len(exp[0])+1)]
    #for exp in findexp:
        remainingstr = remainingstr[index+len(exp[0])+1:]


    return product+remainingstr


reading=1;
while(reading):
    sys.stdout.write('({})$ '.format(reading))
    sys.stdout.flush()
    line = sys.stdin.readline()
    if line == '':
        break
    expline = expand(line)
    sys.stdout.write('>> {}'.format(expline))
    sys.stdout.flush()
    
    reading+=1
sys.stdout.write('\n')
sys.stdout.flush()
