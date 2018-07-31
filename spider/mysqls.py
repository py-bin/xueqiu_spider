# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24 15:45:05 2018

@author: bin
"""

import pymysql

db = pymysql.connect("localhost","root","","TESTDB" )
cursor = db.cursor()

#建立雪球讨论表
def creat_table():
    cursor.execute("DROP TABLE IF EXISTS CSSW")
    sql = '''CREATE TABLE CSSW(
            id varchar(20),
            user_id varchar(20),
            title varchar(200),
            text text(10000),
            retweet_count int,
            reply_count int,
            fav_count int,
            type tinyint,
            user_friends_count int,
            user_followers_count int,
            user_status_count int,
            user_province varchar(256),
            timeBefore varchar(40),
            PRIMARY KEY (id)
            );'''
    cursor.execute(sql)
    return

#建立雪球主题评论表
def creat_table_comment():
    cursor.execute("DROP TABLE IF EXISTS CSSW_CMT")
    sql = '''CREATE TABLE CSSW_CMT(
            id varchar(20),
            user_id varchar(20),
            text text(10000),
            like_count int,
            user_friends_count int,
            user_followers_count int,
            user_status_count int,
            user_province varchar(256),
            timeBefore varchar(40),
            root_in_reply_to_status_id varchar(20),
            PRIMARY KEY (id)
            );'''
    cursor.execute(sql)
    return


def save_data(data_dict):
    sql = '''INSERT INTO CSSW(id,user_id,title,text,retweet_count,
        reply_count,fav_count,type,user_friends_count,
        user_followers_count,user_status_count,user_province,timeBefore)
        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
    value_tup = (data_dict['id'],data_dict['user_id'],data_dict['title'],
                 data_dict['text'],data_dict['retweet_count'],
                 data_dict['reply_count'],data_dict['fav_count'],
                 data_dict['type'],data_dict['user_friends_count'],
                 data_dict['user_followers_count'],data_dict['user_status_count'],
                 data_dict['user_province'],data_dict['timeBefore'])
    try:
        cursor.execute(sql,value_tup)
        db.commit()
    except:
        print('数据库写入失败')
    return
    
def save_data_comment(data_dict):
    sql = '''INSERT IGNORE INTO CSSW_CMT(id,user_id,text,
        like_count,user_friends_count,user_followers_count,
        user_status_count,user_province,timeBefore,root_in_reply_to_status_id)
        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
    value_tup = (data_dict['id'],data_dict['user_id'],
                 data_dict['text'],data_dict['like_count'],
                 data_dict['user_friends_count'],data_dict['user_followers_count'],
                 data_dict['user_status_count'],data_dict['user_province'],
                 data_dict['timeBefore'],data_dict['root_in_reply_to_status_id'])
    try:
        cursor.execute(sql,value_tup)
        db.commit()
    except:
        print('数据库写入失败')
    return    

def close_sql():
    db.close()