# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
import re
from ..items import ThudatazhipinItem


class ZhipinSpider(scrapy.Spider):
    name = "zhipin"
    allowed_domains = ["zhipin.com"]
    start_urls = ['https://www.zhipin.com/c101010100/h_101010100/?'
                  'query=%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90&page=1&ka=page-1']

    def parse(self, response):
        sel = Selector(response)
        url_prefix = 'https://www.zhipin.com'
        job_urls = sel.xpath('//div[@class="job-list"]/ul/li/a/@href').extract()
        for job_url in job_urls:
            url = url_prefix + job_url
            yield scrapy.Request(url=url, callback=self.parse_job_info)

    def parse_job_info(self, response):
        sel = Selector(response)
        item = ThudatazhipinItem()
        print("parse job info from %s" % response.url)

        job_info = sel.xpath('//div[@class="job-primary"]')
        item['job_position'] = job_info.xpath('div[@class="info-primary"]/div[@class="name"]/text()').extract()
        item['job_tag'] = sel.xpath('//div[@class="info-primary"]/div[@class="job-tags"]/span/text()').extract()
        item['department_name'] = 'NULL'

        # 对工作地址进行处理，地址只要精确到区即可。同时用-分隔
        job_location = sel.xpath('//div[@class="location-address"]/text()').extract()[0]
        item['job_location'] = job_location[:re.match('\S+区', job_location).span()[1]]

        item['job_attribute'] = 'NULL'
        item['experience'] = job_info.xpath('div[@class="info-primary"]/p/text()[2]').extract()
        item['education'] = job_info.xpath('div[@class="info-primary"]/p/text()[3]').extract()

        # 对薪资格式进行更改，将5k-10k转换成5000-10000
        job_salary = job_info.xpath('div[@class="info-primary"]/div[@class="name"]/span/text()').extract()
        item['job_salary'] = job_salary[0].replace('K', '000')

        item['professional_requirement'] = 'NULL'
        item['recruiting_num'] = 'NULL'

        # 职位诱惑要进行判断是否存在第二个job-tags标签，如果存在就证明有职位诱惑这个属性，否则为空
        if len(response.xpath('//div[@class="job-tags"]')) == 2:
            item['position_temptation'] = sel.xpath('//div[@class="job-sec"]/div[@class="job-tags"]/span/text()').extract()
        else:
            item['position_temptation'] = 'NULL'

        item['position_desc'] = sel.xpath('//div[@class="text"]/text()').extract()
        item['company_name'] = job_info.xpath('div[@class="info-comapny"]/p[1]/text()').extract()
        item['company_industry'] = job_info.xpath('div[@class="info-comapny"]/p[2]/text()[1]').extract()
        item['company_attribute'] = 'NULL'

        # 融资阶段需要进行判断，页面右上角的属性如果是三个则第二个表示融资阶段，否则没有融资阶段
        # 公司规模，如果是三个属性，则第三个表示公司规模，如果是两个属性则第二个表示公司规模
        if len(sel.xpath('//div[@class="job-primary"]/div[@class="info-comapny"]/p[2]/text()').extract()) == 3:
            item['financing_stage'] = sel.xpath('//div[@class="job-primary"]/div[@class="info-comapny"]/p[2]/text()[2]').extract()
            item['company_scale'] = job_info.xpath('div[@class="info-comapny"]/p[2]/text()[3]').extract()
        else:
            item['financing_stage'] = 'NULL'
            item['company_scale'] = job_info.xpath('div[@class="info-comapny"]/p[2]/text()[2]').extract()


        item['company_page'] = 'NULL'
        item['posted_date'] = sel.xpath('//div[@class="job-author"]/span/text()').extract()
        item['posted_url'] = 'BOSS直聘'
        item['original_link'] = response.url



        yield item




