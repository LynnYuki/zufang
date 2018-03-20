import scrapy
from zufang.items import ZufangItem
class GanjiSpider(scrapy.Spider):
	# 定义爬虫类
	name = "zufang"
	# 爬取域名
	allowed_domain = ['http://cs.ganji.com']
	# 爬取页面地址
	start_urls = ['http://cs.ganji.com/fang1/']
	# 解析数据

	def parse(self, response):
		selector = scrapy.Selector(response)
		items = []
		item = ZufangItem()
		for info in selector.xpath('//div[@class="f-list-item ershoufang-list"]'):
			# 租房标题
			item['title'] = info.xpath('./dl/dd[1]/a/text()').extract()[0]

			# 价格
			item['money'] = info.xpath('./dl/dd[5]/div[1]/span[1]/text()').extract()[0]

			# 地址
			address = info.xpath('./dl/dd[3]/span/a/text()').extract()
			address_0 = address[0]+'区'
			address_else = info.xpath('./dl/dd[3]/span/text()[3]').extract()
			# if len(address)<2:
			# 	print((len(address)))
			item['address'] = address_0 + ''.join(address_else)
			# else:
			# 	item['address'] = address_0 + ''.join(address[1:3])


			# 房屋信息描述
			description = info.xpath('./dl/dd[2]/span[position()>1]/text()').extract()
			item['description'] = ','.join(description)
			print(description)

			# 租房类型
			item['typelist'] = info.xpath('./dl/dd[2]/span[1]/text()').extract()[0]

			# 图片地址
			img_url = info.xpath('./dl/dt/div/a/img/@data-original ').extract()
			if len(img_url):
				item['img'] = "".join(img_url)
			else:
				item['img'] = info.xpath('./dl/dt/div/a/img/@src ').extract()[0]
			items.append(item)
			yield item
		# #翻页
		# next_page = response.xpath(".//*[@id='f_mew_list']/div[6]/div[1]/div[4]/div/div/ul/li[position()<=5]/a/@href").extract()
		# if next_page:
		# 	url = response.urljoin(next_page[0].extract())
		# 	#爬每一页
		# 	yield  scrapy.Request(url,self.parse)
