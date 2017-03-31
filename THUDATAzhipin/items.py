# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ThudatazhipinItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    job_position = scrapy.Field()   #职位名称
    job_tag = scrapy.Field()        #职位分类标签
    department_name = scrapy.Field()#职位所属部门
    job_location = scrapy.Field()   #工作地点
    job_attribute = scrapy.Field()  #工作性质
    experience = scrapy.Field()     #经验
    education = scrapy.Field()      #学历
    job_salary = scrapy.Field()     #薪资
    professional_requirement = scrapy.Field()   #专业要求
    recruiting_num = scrapy.Field() #招聘人数
    position_temptation = scrapy.Field()    #职位诱惑
    position_desc = scrapy.Field()  #岗位介绍
    company_name = scrapy.Field()   #公司名称
    company_industry = scrapy.Field()   #公司行业
    company_attribute = scrapy.Field()  #公司性质
    financing_stage = scrapy.Field()    #融资阶段
    company_scale = scrapy.Field()      #公司规模
    company_page = scrapy.Field()       #公司主页
    posted_date = scrapy.Field()        #发布日期
    posted_url = scrapy.Field()         #发布网址
    original_link = scrapy.Field()      #原始地址
