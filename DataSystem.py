#!usr/bin/python
#-*- coding: utf-8 -*-

import re
import MySQLdb
import time
import jieba
import jieba.analyse


def sentiment(word_list,posi_senti_list,nega_senti_list):
    neg_count = 0; posi_count = 0
    for word in word_list:
        if word in posi_senti_list:
            posi_count += 1
        if word in nega_senti_list:
            neg_count += 1
    senti_score = posi_count - neg_count
    return senti_score

def build_senti_list1(file_name,posi_list, nega_list):
    sen_file = open(file_name)
    file_list = sen_file.read().splitlines()
    for read in file_list:
        word,score = read.split(' ')
        if float(score)>0:
            posi_list.append(word)
        elif float(score)<0:
            nega_list.append(word)
    sen_file.close()

def build_senti_list(file_name):
    with open(file_name) as sen_file:
        sentiment_list = sen_file.read().splitlines()
    sen_file.close()

    return sentiment_list

def main():
    db = MySQLdb.connect(host="localhost",user="root",passwd="",db="dp",charset='utf8')
    cursor = db.cursor()
    sql = "SELECT * FROM keywords LIMIT 20"


    nega_senti_list = build_senti_list(file_name='src/ntusd-negative.txt')
    posi_senti_list = build_senti_list(file_name='src/ntusd-positive.txt')
    build_senti_list1('src/BosonNLP_sentiment_score.txt',posi_senti_list,nega_senti_list)

    #cursor.execute(importsql)
    cursor.execute(sql)
    data = cursor.fetchall()

    for idx,row in enumerate(data, start=1):
        sentence = row[6].split('|')[0]
        word_list = jieba.cut(sentence) #分词
        keyword_list = jieba.analyse.extract_tags(sentence,topK=20,withWeight=False,allowPOS=())    #关键词提取
        print str(idx)+"Full Mode:"+'/'.join(keyword_list)
        #sence = sentiment(keyword_list,posi_senti_list,nega_senti_list)
        #print sentence + '/' + str(sence)

    db.close()

if __name__ == "__main__":
    main()
