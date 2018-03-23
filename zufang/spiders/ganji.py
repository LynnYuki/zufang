import scrapy
from zufang.items import ZufangItem
class GanjiSpider(scrapy.Spider):
	def __init__(self):
		self.headers = {
			'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
			'Accept-Encoding': 'gzip,deflate',
		}
	# 定义爬虫类
	name = "zufang"
	# 爬取域名
	allowed_domain = ['http://cs.ganji.com']
	# 爬取页面地址
	start_urls = ['http://cs.ganji.com/fang1/o86']
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
			address_else = info.xpath('normalize-space(./dl/dd[3]/span/text()[3])').extract()
			# 剔除地址中无用数据
			if len(address) > 2 and ' ' not in address:
				print((len(address)))
				item['address'] = address_0 + '-'.join(address[1:3])
			elif len(address) == 2 and ' ' not in address:
				item['address'] = address_0 + ''.join(address[1]) + '-'.join(address_else)
			else:
				continue
			# 房屋信息描述
			description = info.xpath('./dl/dd[2]/span[position()>1]/text()').extract()
			item['description'] = ','.join(description)
			print(description)

			# 租房类型
			item['typelist'] = info.xpath('./dl/dd[2]/span[1]/text()').extract()[0]

			# 图片地址
			img_url = info.xpath('./dl/dt/div/a/img/@data-original').extract()
			if len(img_url):
				item['img'] = "".join(img_url)
			else:
				item['img'] = info.xpath('./dl/dt/div/a/img/@src').extract()[0]
			items.append(item)
			yield item
		# 翻页
		next_page = response.xpath(".//div[@class='pageBox']/ul/li/a[@class='next']/@href").extract_first()
		if next_page:
			url = response.urljoin(next_page)
			# 爬每一页
			yield scrapy.Request(url, self.parse)
