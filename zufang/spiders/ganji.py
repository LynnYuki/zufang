import scrapy
from zufang.items import ZufangItem
class GanjiSpider(scrapy.Spider):
	#定义爬虫类

	name = "zufang"
	#爬取域名
	allowed_domain = ['cs.ganji.com']
	#爬取页面地址
	start_urls = ['http://cs.ganji.com/fang1/']
	#解析数据

	def parse(self,response):
		selector = scrapy.Selector(response)
		lenth = len(selector)
		items = []
		item = ZufangItem()
		# description_name = ''
		# address_name = ''
		for info in selector.xpath("//div[@class='f-list-item ershoufang-list']"):
			#租房标题
			item['title'] = info.xpath(" .//dl/dd[1]/a/text()").extract()
			#价格
			item['money'] = info.xpath(".//dl/dd[5]/div[1]/span[1]/text()").extract()
			#地址
			address_info =info.xpath(".//dl/dd[3]/span")
			item['address'] =address_info[0].xpath('string(.)').strip()
			#房屋描述
			description_info = info.xpath(".//dl/dd[2]/span[position()>1]/text()").extract()
			item['description'] = description_info[0].xpath('string(.)').strip()
			#租房类型
			item['type_'] = info.xpath(".//dl/dd[2]/span[1]/text()").extract()
			#图片地址
			item['img'] = info.xpath(".//dl/dt/div/a/img/@src").extract()

			items.append(item)
			yield item
		# #翻页
		# next_page = response.xpath(".//*[@id='f_mew_list']/div[6]/div[1]/div[4]/div/div/ul/li[position()<=5]/a/@href").extract()
		# if next_page:
		# 	url = response.urljoin(next_page[0].extract())
		# 	#爬每一页
		# 	yield  scrapy.Request(url,self.parse)
