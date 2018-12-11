# -*- coding: utf-8 -*-
import scrapy
import re
import json
from Fiction.items import FictionItem

class NovelSpider(scrapy.Spider):
    name = 'novel'
    allowed_domains = ['www.quanshuwang.com']
    url = 'http://www.quanshuwang.com/list/1_'
    start = 1
    start1 = '.html'
    start_urls = [url+str(start)+start1]

    def parse(self, response):
        for i in range(1,998):
            # scrapy.Request() 放到调度列的中star_urls列表中，会自动去重
            yield scrapy.Request(self.url+str(i)+self.start1,callback=self.parse1)
    
    def parse1(self,response):
        # 获取每页所有小说的URL列表
        book_urls = response.xpath('//li/a[@class="l mr10"]/@href').extract()
        for book_url in book_urls:
            yield scrapy.Request(book_url,callback=self.parse_read)

    #获取马上阅读按钮的URL，进入章节目录
    def parse_read(self,response):
        item = FictionItem()
        # 马上阅读的URL
        read_url = response.xpath('//a[@class="reader"]/@href').extract()[0]
        # 小说图片的URL
        self.img_url = response.xpath('//div/a/img/@src').extract()[0]
        
        # print(1111111111111,item['image'])
        yield scrapy.Request(read_url,callback=self.parse_chapter)

    #获取小说章节的URL
    def parse_chapter(self,response):
        chapter_urls = response.xpath('//div[@class="clearfix dirconone"]/li/a/@href').extract()
        for chapter_url in chapter_urls:
            yield scrapy.Request(chapter_url,callback=self.parse_content)

    #获取小说名字,章节的名字和内容
    def parse_content(self, response):
        # 小说名字
        name = response.xpath('//div[@class="main-index"]/a[@class="article_title"]/text()').extract()[0]
        # 小说章节名字
        chapter_name = response.xpath('//strong[@class="l jieqi_title"]/text()').extract()[0]

        # 小说内容
        # chapter_content = response.xpath('//div[@class="mainContenr"]/text()').extract()[0]

        chapter_content_reg = r'style5\(\);</script>(.*?)<script type="text/javascript">'
        
        result = response.text
        chapter_content_2 = re.findall(chapter_content_reg, result, re.S)[0]
        chapter_content = chapter_content_2.replace('    ', '').replace('<br />', '').replace('&nbsp;', '')

        item = FictionItem()
        item['name'] = name
        item['chapter_name'] = chapter_name
        item['chapter_content'] = chapter_content
        # item['image'] = self.img_url
        yield item
