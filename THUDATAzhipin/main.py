# -*- coding: utf-8 -*-

from scrapy import cmdline
import time

crawl_time = time.strftime("%Y_%m_%d", time.localtime())
filename = 'THUDataPiCrawler_zhipin' + '_' + crawl_time + '.csv'
command = "scrapy crawl zhipin -o " + filename + " -t csv -s CLOSESPIDER_ITEMCOUNT=500"
cmdline.execute(command.split())
