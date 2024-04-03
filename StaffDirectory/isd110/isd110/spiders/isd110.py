import scrapy
from scrapy.shell import inspect_response


class StaffDirectory(scrapy.Spider):
	name = 'isd110'

	def start_requests(self):
		url = 'https://isd110.org/our-schools/laketown-elementary/staff-directory?s=&page=0'

		# url = 'https://isd110.org/our-schools/laketown-elementary/staff-directory?s=&page=2'

		headers = {
		    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
		    "accept-language": "en-GB,en;q=0.9",
		    "sec-ch-ua": "\"Google Chrome\";v=\"123\", \"Not:A-Brand\";v=\"8\", \"Chromium\";v=\"123\"",
		    "sec-ch-ua-mobile": "?0",
		    "sec-ch-ua-platform": "\"Windows\"",
		    "sec-fetch-dest": "document",
		    "sec-fetch-mode": "navigate",
		    "sec-fetch-site": "none",
		    "sec-fetch-user": "?1",
		    "upgrade-insecure-requests": "1",
		    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
		}

		yield scrapy.Request(
		    url=url,
		    method='GET',
		    dont_filter=True,
		    headers=headers,
		)

	def parse(self, response):
		# inspect_response(response, self)
		for res in response.xpath('.//*[@class="views-row"]'):
			