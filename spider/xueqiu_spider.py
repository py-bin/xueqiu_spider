# -*- coding: utf-8 -*-
"""
Created on Wed Aug  1 09:34:28 2018

@author: bin
"""

import css_craw
import zhuti_craw
import mysqls

def main():
    mysqls.creat_table() #在数据库建立表格用于存储雪球**讨论**数据
    mysqls.creat_table_comment() #在数据库建立表格用于存储雪球**评论**数据
    css_craw.main_craw() #爬取长生生物讨论数据
    zhuti_craw.main_craw() #爬取长生生物评论数据
    #**注意**如需要得到更多的评价，需要更改排序，在craw_html()中paras的sort
    mysqls.close_sql() #切断与数据库的连接

if __name__ == '__main__':
	main()