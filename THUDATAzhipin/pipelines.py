# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re
import time
import csv


class ThudatazhipinPipeline(object):
    def process_item(self, item, spider):

        # -----------------提取日期------------------
        # 三类日期形式
        # "发布于昨天"
        # "发布于03月29日"
        # "发布于11:20"
        date1 = "发布于昨天"
        date = item['posted_date'][0]
        if date == date1:
            final_date = '{}/{}/{}'.format(time.localtime().tm_year, time.localtime().tm_mon, time.localtime().tm_mday - 1)
        elif re.findall(':', date) == ':':
            final_date = '{}/{}/{}'.format(time.localtime().tm_year, time.localtime().tm_mon, time.localtime().tm_mday)
        else:
            month = re.findall("[0-9][0-9]", date)[0]
            day = re.findall("[0-9][0-9]", date)[1]
            final_date = '{}/{}/{}'.format(time.localtime().tm_year, month, day)
        item['posted_date'] = final_date
        return item
        # ---------------结果写入CSV文件--------------
        # crawl_time = time.strftime("%Y_%m_%d", time.localtime())
        # with open('THUDataPiCrawler_zhipin' + '_' + crawl_time + '.csv', 'a') as f:
        #     writer = csv.writer(f, dialect='excel')
        #     writer.writerow(
        #             item['job_position'],
        #             item['job_tag'],
        #             item['department_name'],
        #             item['job_location'],
        #             item['job_attribute'],
        #             item['experience'],
        #             item['job_salary'],
        #             item['professional_requirement'],
        #             item['recruiting_num'],
        #             item['position_temptation'],
        #             item['position_desc'],
        #             item['company_name'],
        #             item['company_industry'],
        #             item['company_attribute'],
        #             item['financing_stage'],
        #             item['company_scale'],
        #             item['company_page'],
        #             final_date,
        #             item['posted_url'],
        #             item['original_link']
        #     )
