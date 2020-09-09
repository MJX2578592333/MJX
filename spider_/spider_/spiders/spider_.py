# coding : utf-8

import scrapy
import re
from ..items import SpiderItem




class DemoSpider(scrapy.Spider):
    name = 'spider_'

    def start_requests(self):

        for page in range(26863):
            url = 'https://www.anquanke.com/vul?page={}'.format(page)

            yield scrapy.Request(url=url,callback=self.parse_1)

    def parse_1(self, response):

        html = response.text

        vul_ids = re.findall(r'href=\"(/vul/id/\d+)\">',html)

        for vul_id in vul_ids:
            vul_detail_url = 'https://www.anquanke.com{}'.format(vul_id)

            yield  scrapy.Request(url=vul_detail_url,callback=self.parse_2)


    def parse_2(self,response):

        html = response.text

        cnnvd_url = re.findall(r'<a href=\"(http://www\.cnnvd\.org\.cn/web/xxk/ldxqById\.tag\?CNNVD=CNNVD-\d+-\d+)\"',html)

        # print(cnnvd_url)
        if cnnvd_url != []:
            print(cnnvd_url[0])

            yield scrapy.Request(url=cnnvd_url[0],callback=self.parse_3)

    def parse_3(self, response):

        html = response.text

        #漏洞名称
        vul_name = re.findall(r'<div class="detail_xq w770" >\n\s*<h2>(.*)\n\s*</h2>',html)

        #漏洞cnnvd id
        vul_cnnvd_id = re.findall(r'<li><span>CNNVD编号：(CNNVD-\d+-\d+)</span></li>', html)

        #漏洞 cve id
        vul_cve = re.findall(r'<a href="http://cve\.mitre\.org/cgi-bin/cvename\.cgi\?name=(CVE-\d+-\d+)"', html)

        #漏洞 发布日期
        vul_date = re.findall(r'<a style=\"color:#4095cc;cursor:pointer;\" href=\"/web/vulnerability/querylist\.tag\?qstartdateXq=(\d{4}-\d+-\d+)\" >',html)

        vul_gongji = re.findall(r'<a style="color:#4095cc;cursor:pointer;">\s*\n\s*(.*)\n\s*</a>', html)

        #漏洞详情

        vul_detailss = []
        vul_detail_1 = re.findall(r'<p style="text-indent:2em">\n\s*(.*)</p><p style="text-indent:2em">\n\s*(.*)',html)
        if vul_detail_1 != []:
            vul_detail = "".join(vul_detail_1[0])
            vul_detailss.append(vul_detail)
        else:

            vul_detail_2 = re.findall(r'<p\s*style="text-indent:2em">\n\s*(.*)\s*\n\s*</p>',html)
            if vul_detail_2 !=[]:
                vul_detailss.append(vul_detail_2[0])

        vul_solutions = re.findall(
            r'<p style="text-indent:2em">\n\s*(.*)</p><p style="text-indent:2em" class="ldgg">\n\s*(.*)', html)

        #漏洞解决方案
        vul_solution = []
        if vul_solutions != []:
            vul_solution_1 = "".join(vul_solutions[0])
            # vul_solution_1 = vul_solution_1.replace('')
            vul_solution.append(vul_solution_1)
        #漏洞连接
        vul_linka = []

        vul_links = re.findall(r'</p><p style="text-indent:2em;width: 890px;" class="ckwz">\s*\n\s*链接:(http.*)[<\n]',
                              html)
        if vul_links != []:
            for link in vul_links:
                vul_linka.append(link.replace('</p><p style="text-indent:2em;width: 890px;" class="ckwz">',''))
        vul_link = ','.join(vul_linka)
        vulss = []
        vulss.append('"'+vul_link+'"')
        item = SpiderItem()


        for name,cnnvd_id,cve,date,solution,detail_info,link,gonji in zip(vul_name,vul_cnnvd_id,vul_cve,vul_date,vul_solution,vul_detailss,vulss,vul_gongji):

            item['vul_name'] = name
            item['vul_cnnvd_id'] = cnnvd_id
            item['vul_cve'] = cve
            item['vul_date'] = date
            item['vul_solution'] = solution
            item['vul_link'] = link
            item['vul_detail_info'] = detail_info
            item['vul_gongji'] = gonji
            yield item












