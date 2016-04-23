#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys

def splitWord(words):
    uni = words.decode('utf-8')
    li = list()    
    for u in uni:
        li.append(u.encode('utf-8'))
    return li

#4 tag
#S/B/E/M
def get4Tag(li):
    length = len(li)
    #print length
    if length == 1:
        return ['S']
    elif length == 2:
        return ['B','E']
    elif length > 2:
        li = list()
        li.append('B')
    for i in range(0,length-2):
        li.append('M')
    li.append('E')
    return li
#6 tag
#S/B/E/M/M1/M2
def get6Tag(li):
    length = len(li)
    #print length
    if length   == 1:
        return ['S']
    elif length == 2:
        return ['B','E']
    elif length == 3:
        return ['B','M','E']
    elif length == 4:
        return ['B','M1','M','E']
    elif length == 5:
        return ['B','M1','M2','M','E']
    elif length > 5:
        li = list()
        li.append('B')
        li.append('M1')
        li.append('M2')
        for i in range(0,length-4):
            li.append('M')
        li.append('E')
    return li

def save_data_file(trainobj,testobj,isTest,word,handle,tag):
    if isTest:
        save_train_file(testobj,word,handle,tag)
    else:
        save_train_file(trainobj,word,handle,tag)

def save_train_file(fiobj,word,handle,tag): 
    if len(word) > 0:
        wordli = splitWord(word)
        if tag == '4':
            tagli = get4Tag(wordli)
        if tag == '6':
            tagli = get6Tag(wordli)
        for i in range(0,len(wordli)):
            w = wordli[i]
            h = handle
            t = tagli[i]
            fiobj.write(w + '\t' + h + '\t' + t + '\n')
    else:
        #print 'New line'
        fiobj.write('\n')

def convert_tag(file_input, tag):
    fiobj    = open(file_input,'r')
    trainobj = open(tag + '.train.data','w' )
    testobj  = open(tag + '.test.data','w')

    arr = fiobj.readlines()
    i = 0
    for a in arr:
        i += 1
        a = a.strip('\r\n\t ')
        words = a.split(' ')
        test = False
        if i % 10 == 0:
            test = True
        for word in words[1:]:
            word = word.strip('\t ')
            if len(word) > 0:
                i1 = word.find('[')
                if i1 >= 0:
                    word = word[i1+1:]
                i2 = word.find(']')
                if i2 > 0:
                    word = word[:i2]
                word_hand = word.split('/')
                w,h = word_hand
                '''
                #print w,h
                if h == 'nr':    #ren min
                    #print 'NR',w
                    if w.find('·') >= 0:
                        tmpArr = w.split('·')
                        for tmp in tmpArr:
                            save_data_file(trainobj,testobj,test,tmp,h,tag)
                        continue
                el'''
                if h == 'w': ##符号
                    save_data_file(trainobj,testobj,test,"","",tag) #split
                else:
                    save_data_file(trainobj,testobj,test,w,h,tag)
    trainobj.flush()
    testobj.flush()

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'tag[6,4] convert raw data to train.data and tag.test.data'
    else:
        input_file = sys.argv[1]
        tag = sys.argv[2]
        convert_tag(input_file, tag)
