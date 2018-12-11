# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import scrapy
from scrapy.pipelines.images import ImagesPipeline

class FictionPipeline(object):
    def process_item(self, item, spider):
        # print('****************************')
        # print(item['name'])
        # # print(item['image'])
        # print(item['chapter_name'])
        # print(item['chapter_content'])
        # print('****************************')
        
        curPath = 'D:\全书网小说'
        tempPath = str(item['name'])
        targetPath = curPath + os.path.sep + tempPath
        if not os.path.exists(targetPath):
            # 创建目录
            os.makedirs(targetPath)
 
        filename_path = 'D:\全书网小说'+ os.path.sep + str(item['name'])+ os.path.sep + str(item['chapter_name']) + '.txt'
        with open(filename_path, 'w', encoding='utf-8') as f:
            f.write(item['chapter_content'] + "\n")
            print(item['chapter_name'],'存储完成')
        return item

# class FictionImagePipeline(ImagesPipeline):
#     def get_media_requests(self,item,info):
#         imageLink = item['image']
#         # 向图片链接发请求，响应会保存在settings.py中的 IMAGES_STORE 路径中
#         print('图片保存完成')
#         yield scrapy.Request(imageLink)