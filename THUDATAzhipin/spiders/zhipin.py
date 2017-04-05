# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
import re
from ..items import ThudatazhipinItem
import time
import sys
import io


class ZhipinSpider(scrapy.Spider):
    name = "zhipin"
    allowed_domains = ["zhipin.com"]
    # start_urls = ['https://www.zhipin.com/c101010100/h_101010100/?'
    #               'query=%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90&page=1&ka=page-1']

    def start_requests(self):
        search_fields = ['hadoop', 'spark', 'hbase', 'hive', r'大数据',
                         r'数据分析', r'数据运营', r'数据挖掘', r'爬虫', r'抓取', r'可视化', r'数据开发', r'数据工程',
                         r'数据处理', r'数据科学家', r'数据工程师', r'数据架构师', r'数据采集', r'数据建模', r'数据平台',
                         r'数据研发', r'数据管理', r'数据统计', r'数据产品', r'数据方向', r'数据仓库', r'数据研究',
                         r'数据算法', r'数据蜘蛛', r'数据应用', r'数据技术', r'数据运维', r'数据支撑', r'数据安全',
                         r'数据爬取', r'数据经理', r'金融数据', r'数据专员', r'数据主管', r'数据项目经理', r'数据整合',
                         r'数据模型', r'财务数据', r'数据专家', r'数据报送', r'数据中心', r'数据移动', r'数据标准',
                         r'数据推广', r'数据质量', r'数据检索', r'数据服务', r'数据搭建', r'数据实施', r'数据风控']

        # 城市 北京|上海|广州|深圳|杭州|天津|西安|苏州|武汉|厦门|长沙|成都|重庆|哈尔滨|沈阳
        city_list = ['101010100', '101020100', '101280100', '101280600', '101210100', '101030100', '101110100',
                     '101190400', '101200100', '101230200', '101250100', '101270100', '101040100', '101050100','101070100']

        urls = []
        for city in city_list:
            for job in search_fields:
                url = 'https://www.zhipin.com/job_detail/?query=%s&scity=%s' % (job, city)
                urls.append(url)
        for job_url in urls:
            yield scrapy.Request(url=job_url, callback=self.parse)

    def parse(self, response):
        sel = Selector(response)
        url_prefix = 'https://www.zhipin.com'
        job_urls = sel.xpath('//div[@class="job-list"]/ul/li/a/@href').extract()
        for job_url in job_urls:
            url = url_prefix + job_url
            yield scrapy.Request(url=url, callback=self.parse_job_info)

        next_page_url = sel.xpath('//a[@class="next"]/href').extract()
        if len(next_page_url) != 0:
            next_page_url = url_prefix + ''.join(next_page_url)
            yield scrapy.Request(url=next_page_url, callback=self.parse)


    def parse_job_info(self, response):
        sel = Selector(response)
        item = ThudatazhipinItem()
        print("parse job info from %s" % response.url)
        # sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')

        job_info = sel.xpath('//div[@class="job-primary"]')
        item['job_position'] = ''.join(job_info.xpath('div[@class="info-primary"]/div[@class="name"]/text()').extract())
        item['job_tag'] = ','.join(sel.xpath('//div[@class="info-primary"]/div[@class="job-tags"]/span/text()').extract())
        item['department_name'] = 'NULL'

        # 对工作地址进行处理，地址只要精确到区即可。同时用-分隔,比如 北京-海淀区
        # 由于本网站中部分工作直给出了区，但是市的位置可以在job-info中获取
        # 所以采用job-info获取市，在工作地址提取区
        job_location_city = ''.join(job_info.xpath('div[@class="info-primary"]/p/text()[1]').extract()) # 工作地址 市
        job_location = ''.join(sel.xpath('//div[@class="location-address"]/text()').extract())
        job_location_area = re.findall('\S.??区', job_location)   # 工作地址 区
        if len(job_location_area) != 0:
            item['job_location'] = job_location_city + '-' + job_location_area[0]
        else:
            item['job_location'] = job_location_city + '-' + 'NULL'

        item['job_attribute'] = 'NULL'
        item['experience'] = ''.join(job_info.xpath('div[@class="info-primary"]/p/text()[2]').extract())
        item['education'] = ''.join(job_info.xpath('div[@class="info-primary"]/p/text()[3]').extract())

        # 对薪资格式进行更改，将5k-10k转换成5000-10000
        job_salary = ''.join(job_info.xpath('div[@class="info-primary"]/div[@class="name"]/span/text()').extract())
        item['job_salary'] = job_salary.replace('K', '000')

        item['professional_requirement'] = 'NULL'
        item['recruiting_num'] = 'NULL'

        # 职位诱惑要进行判断是否存在第二个job-tags标签，如果存在就证明有职位诱惑这个属性，否则为空
        if len(response.xpath('//div[@class="job-tags"]')) == 2:
            item['position_temptation'] = ','.join(sel.xpath('//div[@class="job-sec"]/div[@class="job-tags"]/span/text()').extract())
        else:
            item['position_temptation'] = 'NULL'

        item['position_desc'] = ','.join(sel.xpath('//div[@class="text"]/text()').extract())
        item['company_name'] = ''.join(job_info.xpath('div[@class="info-comapny"]/p[1]/text()').extract())
        item['company_industry'] = ''.join(job_info.xpath('div[@class="info-comapny"]/p[2]/text()[1]').extract())
        item['company_attribute'] = 'NULL'

        # 融资阶段需要进行判断，页面右上角的属性如果是三个则第二个表示融资阶段，否则没有融资阶段
        # 公司规模，如果是三个属性，则第三个表示公司规模，如果是两个属性则第二个表示公司规模
        if len(sel.xpath('//div[@class="job-primary"]/div[@class="info-comapny"]/p[2]/text()').extract()) == 3:
            item['financing_stage'] = ''.join(sel.xpath('//div[@class="job-primary"]/div[@class="info-comapny"]/p[2]/text()[2]').extract())
            item['company_scale'] = ''.join(job_info.xpath('div[@class="info-comapny"]/p[2]/text()[3]').extract())
        else:
            item['financing_stage'] = 'NULL'
            item['company_scale'] = ''.join(job_info.xpath('div[@class="info-comapny"]/p[2]/text()[2]').extract())

        item['company_page'] = 'NULL'
        item['posted_date'] = ''.join(sel.xpath('//div[@class="job-author"]/span/text()').extract())
        item['posted_url'] = 'BOSS直聘'
        item['original_link'] = response.url

        yield item




