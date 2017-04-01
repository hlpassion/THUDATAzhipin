# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re
import time
import datetime
import csv


class ThudatazhipinPipeline(object):
    def process_item(self, item, spider):

        # -----------------工作经验------------------
        # 三类工作经验格式
        # 3-5年 | 应届生 | 经验不限 | 1年以内   对应格式
        # 3-5年经验 | 0年经验 | NULL | 1年经验
        experience = item['experience']
        if experience == '应届生':
            item['experience'] = "0年经验"
        elif experience == "经验不限":
            item['experience'] = "NULL"
        elif experience == "1年以内":
            item['experience'] = "1年经验"
        else:
            item['experience'] = experience.replace('年', '年经验')


        # -----------------提取日期------------------
        # 三类日期形式
        # "发布于昨天" | "发布于03月29日" | # "发布于11:20"
        date1 = "发布于昨天"
        date = item['posted_date']
        if date == date1:
            if  (time.localtime().tm_mday - 1) == 0:
                pre_day = str(datetime.date.today() - datetime.timedelta(days=1))
                final_date = '{}/{}/{}'.format(pre_day[:4], pre_day[5:7], pre_day[8:])
            else:
                final_date = '{}/{}/{}'.format(time.localtime().tm_year, time.localtime().tm_mon, time.localtime().tm_mday - 1)
        elif len(re.findall(':', date)) != 0:
            final_date = '{}/{}/{}'.format(time.localtime().tm_year, time.localtime().tm_mon, time.localtime().tm_mday)
        else:
            month = re.findall("[0-9][0-9]", date)[0]
            day = re.findall("[0-9][0-9]", date)[1]
            final_date = '{}/{}/{}'.format(time.localtime().tm_year, month, day)

        item['posted_date'] = final_date
        # ---------------结果写入CSV文件--------------
        crawl_time = time.strftime("%Y_%m_%d", time.localtime())
        with open('THUDataPiCrawler_zhipin' + '_' + crawl_time + '.csv', 'a') as f:
            writer = csv.writer(f, dialect='excel')
            writer.writerow(
                [
                    item['job_position'],
                    item['job_tag'],
                    item['department_name'],
                    item['job_location'],
                    item['job_attribute'],
                    item['experience'],
                    item['education'],
                    item['job_salary'],
                    item['professional_requirement'],
                    item['recruiting_num'],
                    item['position_temptation'],
                    item['position_desc'],
                    item['company_name'],
                    item['company_industry'],
                    item['company_attribute'],
                    item['financing_stage'],
                    item['company_scale'],
                    item['company_page'],
                    final_date,
                    item['posted_url'],
                    item['original_link']
                ]
            )
