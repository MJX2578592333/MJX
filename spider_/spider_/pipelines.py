# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3
import csv
import xlwt

class SpiderPipeline(object):
    def process_item(self, item, spider):


        with open('vul_data.csv','a',encoding='utf-8',newline='') as f:
            # 2. 基于文件对象构建 csv写入对象
            csv_writer = csv.writer(f)

            # 4. 写入csv文件内容
            csv_writer.writerow([
                item['vul_name'],
                item['vul_cnnvd_id'],
                item['vul_cve'],
                item['vul_gongji'],
                item['vul_date'],
                item['vul_solution'],
                item['vul_link'],
                item['vul_detail_info'],
            ])

        return item

