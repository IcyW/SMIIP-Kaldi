#! /usr/bin/python
#  encoding=utf-8

import sys
import random
import re

reload(sys)
sys.setdefaultencoding('utf-8')

debugInfo = True
UNKSYMBOL = u'<UNK>'

## 阿拉伯数字转中文, 比如1204转一千二百零四
def digit2Cn(text):
    if not isinstance(text, basestring):
        try:
            text = text.group()
        except Exception as e:
            text = ""
    text = str(int(text))
    cnstr = ""
    end = len(text)
    unit = [u'', u'十', u'百', u'千']
    number = [u'零', u'一', u'二', u'三', u'四', u'五', u'六', u'七', u'八', u'九']

    def allzero(ns):
        flag = True
        for n in range(0, len(ns)):
            if ns[n] != '0':
                flag = False
        return flag

    if allzero(text):
        if len(text) == 1:
            return number[0]
        else:
            return ""

    for i in range(0, len(text)):
        toadd = ""
        if end - i > 0:
            substr = text[i+1:end]
            if not (i == 0 and end - i == 2 and text[i] == '1'):
                toadd += number[int(text[i])]
            if text[i] != '0':
                toadd += unit[end - i - 1]
            if allzero(substr):
                cnstr += toadd
                break
            elif text[i] == '0' and i + 1 < len(text) and text[i + 1] == '0':
                continue
        cnstr += toadd
    return cnstr

## 数字转中文
def num2Cn(text):
    number = [u'零', u'一', u'二', u'三', u'四', u'五', u'六', u'七', u'八', u'九']
    numstr = ""
    if not isinstance(text, basestring):
        try:
            text = text.group()
        except Exception as e:
            text = ""
    for i in range(0, len(text)):
        numstr += number[int(text[i])]
    return numstr

## 多位数字带小数点的转中文
def ldigit2Cn(text):
    if len(text) > 10:
        return u''
    unit = ['点', '万', '亿']
    cnstr = ""
    if '.' in text:
        dotIndex = text.index('.')
        cnstr += ldigit2Cn(text[0:dotIndex]) + unit[0] + num2Cn(text[dotIndex + 1:len(text)])
    else:
        strlen = len(text)
        if strlen <= 8:
            if strlen <= 4:
                cnstr += digit2Cn(text)
            else:
                subcnstr = digit2Cn(text[0:strlen - 4])
                if subcnstr != "":
                    cnstr += digit2Cn(text[0:strlen - 4]) + unit[1] + digit2Cn(text[-4:])
                else:
                    cnstr += digit2Cn(text[-4:])
        else:
            cnstr += ldigit2Cn(text[0:strlen - 8]) + unit[2] + ldigit2Cn(text[-8:])
    return cnstr

def ip2cn(match_str):
    sgm = match_str.group(0).split(u'.')
    if len(sgm) != 4:
        return ""
    else:
        return u'点'.join((num2Cn(i) for i in sgm))

def date(match_obj):
    year, month, day = re.split(ur'[^\d]', match_obj.group())[:3]
    return num2Cn(year) + u'年' + digit2Cn(month) + u'月' + digit2Cn(day) + u'日'

def date2cn(text):
    assert isinstance(text, unicode)
    date_ptn = ur'[1-9][\d]{3}[\-\/\.](1[012]|[0]?[1-9])[\-\/\.]([12][0-9]|3[01]|[0]?[1-9])'
    text = re.sub(ur'[1-9][0-9]{3}[年]', lambda t: re.sub(ur'[\d]+', num2Cn, t.group()), text)
    text = re.sub(ur'(1[012]|[0]?[1-9])[月][份]?', lambda t : re.sub(ur'[\d]+', digit2Cn, t.group()), text)
    text = re.sub(ur'([12][0-9]|3[01]|[0]?[1-9])[日号]', lambda t: re.sub(ur'[\d]+', digit2Cn, t.group()), text)
    text = re.sub(date_ptn, date, text)
    return text

def timeFormator(match_obj):
    t = match_obj.group().split(':')[:3]
    if len(t) == 2:
        return digit2Cn(t[0]) + u'点' + digit2Cn(t[1]) + u'分'
    return digit2Cn(t[0]) + u'点' + digit2Cn(t[1]) + u'分' + digit2Cn(t[2]) + u'秒'

def time2cn(text):
    assert isinstance(text, unicode)
    time_ptn = ur'(1[0-9]|[2][0-4]|0?[0-9])(\:([1-5][0-9]|0?[0-9]))+'
    text = re.sub(ur'(1[0-9]|[2][0-4]|0?[0-9])[时点][钟整]?', lambda t: re.sub(ur'[\d]+', digit2Cn, t.group()), text)
    text = re.sub(ur'([1-5][0-9]|0?[0-9])[分][钟整]?', lambda t: re.sub(ur'[\d]+', digit2Cn, t.group()), text)
    text = re.sub(ur'([1-5][0-9]|0?[0-9])[秒][钟整]?', lambda t: re.sub(ur'[\d]+', digit2Cn, t.group()), text)
    text = re.sub(time_ptn, timeFormator, text)
    return text

def textFormator(text):
    text = re.sub(ur'[\x05-\x08\x0b-\x1f\x7f]', u'', text)
    text = re.sub(ur'[\uFF01-\uFF5E]+', lambda t: ''.join(map(lambda c: unichr(ord(c)-0xfee0), t.group())), text)
    IP = ur'([0-9]{1,3}\.){3}[0-9]{1,3}'
    url = ur'&nbsp|(http[s]?\:|www\.|[\w\d\.]+\@)?.+\.(org|com|cn|php|htm[l]?|net)[^\u4e00-\u9fff]*'
    path = ur'([a-zA-Z]\:)?(\\[\d\w\-\+\=\.\~ ]+)+|(\/[\d\w\-\+\=\.\~ ]+)+\
                |ftp\:((\\[\d\w\-\+\.\=\~ ]*)+|(\/[\d\w\-\+\.\=\~ ]*)+)'
    percent = ur'[\d]+([\.][\d]+)?\%'
    text = re.sub(IP, ip2cn, text)
    text = date2cn(text)
    text = time2cn(text)
    text = re.sub('|'.join((url, path, ur'[、《》\u3000]')), u'', text)
    text = re.sub(percent, lambda t: u'百分之' + ldigit2Cn(t.group(0)[0:-1]), text)
    text = re.sub(ur'\d+(\.\d+)?', lambda t: ldigit2Cn(t.group(0)), text)
    text = re.sub(ur'[\(\)\[\]【】（）\{\}「」,\.\?，。？;\!！；“”"]', u'\n', text)
    text = re.sub(ur'[^\n]*\n', lambda t: t.group() if len(t.group().strip()) > 1 and not re.search(ur'[^\u4e00-\u9fff\n]', t.group().strip()) else '', text)
    return text

def processing(text_path, out_path, buffsize=100000):
    out = open(out_path, 'w')
    with open(text_path) as readf:
        rfgen = readf.xreadlines()
        while True:
            buff = ""
            done = False
            for i in xrange(buffsize):
                try:
                    buff += rfgen.next()
                except StopIteration as e:
                    done = True
                    break
            buff = textFormator(buff.decode('utf-8'))
            out.write(buff.encode('utf-8'))
            if done:
                break
    out.close()


def jieba_tokenize(userdict_path, text_path, out_path, buffsize=100000, useUNK=True, jiebaThreads=5):
    #jieba.enable_parallel(jiebaThreads)
    #jieba.set_dictionary('dict.txt.small')
    with file(userdict_path) as rf:
        words_set = set(rf.read().decode('utf-8').splitlines())
    words_set.add(u'\n')
    out = file(out_path, 'w')
    with open(text_path) as readf:
        rfgen = readf.xreadlines()
        while True:
            done = False
            buff = ""
            for i in xrange(buffsize):
                try:
                    buff += rfgen.next()
                except StopIteration as e:
                    done = True
                    break
            buff = buff.decode('utf-8')
            # token ....
            allwords = jieba.lcut(buff, HMM=False)
            if useUNK:
                for i, w in enumerate(allwords):
                    if w not in words_set:
                        allwords[i] = ' '.join(map(lambda x: x if x in words_set else UNKSYMBOL, w))
            buff = u' '.join(allwords)
            buff = re.sub(ur' \n ', u'\n', buff)
            out.write(buff.encode('utf-8'))
            if done:
                break
    out.close()

def ltp_tokenize(userdict_path, text_path, out_path, model_path, buffsize=100000, useUNK=True):
    segmentor = Segmentor()
    segmentor.load(model_path)

    with file(userdict_path) as rf:
        words_set = set(rf.read().decode('utf-8').splitlines())
    words_set.add(u'\n')
    out = file(out_path, 'w')
    with open(text_path) as readf:
        rfgen = readf.xreadlines()
        while True:
            done = False
            buff = ""
            for i in xrange(buffsize):
                try:
                    buff += rfgen.next()
                except StopIteration as e:
                    done = True
                    break
            buff = buff.decode('utf-8')
            # token ....
            allwords = segmentor.segment(buff)
            if useUNK:
                for i, w in enumerate(allwords):
                    if w not in words_set:
                        allwords[i] = ' '.join(map(lambda x: x if x in words_set else UNKSYMBOL, w))
            buff = u' '.join(allwords)
            buff = re.sub(ur' \n ', u'\n', buff)
            out.write(buff.encode('utf-8'))
            if done:
                break
    out.close()


r=open('trainfile.txt','w')
for i in range(0,1000):
	a=random.randint(5,15)
	for j in range(0,a):
		r.write(num2Cn(str(random.randint(0,9))))
		#if random.randint(0,1) == 0:
		#	r.write(' ')
                r.write(' ')
	r.write('\n')

r.close()


