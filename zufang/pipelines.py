# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

from zufang import settings


class ZufangPipeline(object):
	def __init__(self):
		# 连接数据库
		self.connect = pymysql.connect(
			host=settings.MYSQL_HOST,
			port=3306,
			db=settings.MYSQL_DBNAME,
			user=settings.MYSQL_USER,
			passwd=settings.MYSQL_PASSWD,
			charset='utf8',
			use_unicode=True)

		# 使用cursor执行增删改查
		self.cursor = self.connect.cursor()

	def process_item(self, item, spider):
		print(spider.name, 'pipelines')
		try:
			# 查重处理
			self.cursor.execute(
				"SELECT *  FROM zufanginfo WHERE img = %s", item['img'])
			# 是否有重复数据
			repetition = self.cursor.fetchone()

			# 重复
			if repetition:
				pass
			else:
				# 插入数据
				insert_sql = "insert into zufanginfo(title,money,description,typelist,address,img)values('{}','{}','{}','{}','{}','{}')".format(
					item['title'], item['money'], item['description'], item['typelist'], item['address'], item['img'])
			print(insert_sql)
			# 执行SQL语句
			self.cursor.execute(insert_sql)
			# 提交数据
			self.connect.commit()
		except Exception as error:
			# 打印错误信息
			print(error)
			return item

	def spider_close(self, spider):
		self.connect.close()
