import scrapy


class StaffDirectory(scrapy.Spider):
    name = "isd110"
    custom_settings = {
        "FEED_FORMAT": "csv",  # Set the output format to CSV
        "FEED_URI": "staff directory.csv",  # Specify the file path for CSV output
    }

    def clean_text(self, text):
        """
        Strip leading and trailing whitespace from the text.
        """
        if text:
            return text.strip()
        return None

    def clean_and_join(self, text_list):
        """
        Strip leading and trailing whitespace from each item in the list and join them with newline.
        """
        if text_list:
            return "\n".join([item.strip() for item in text_list])
        return None

    def start_requests(self):
        """
        Method to initiate the spider by sending a request to the starting URL.
        """
        url = "https://isd110.org/our-schools/laketown-elementary/staff-directory"
        self.headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "en-GB,en;q=0.9",
            "sec-ch-ua": '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        }

        yield scrapy.Request(
            url=url,
            method="GET",
            dont_filter=True,
            headers=self.headers,
        )

    def parse(self, response):
        """
        Parses the response and extracts staff directory information.
        """
        item = {}
        item["SchoolName"] = self.clean_text(
            response.xpath(
                './/*[@title="Home"]/text()[normalize-space()]'
            ).extract_first()
        )
        item["Address"] = self.clean_and_join(
            response.xpath('.//*[@class="address"]/text()[normalize-space()]').extract()
        )
        item["State"] = response.xpath(
            './/*[@class="address"]/text()[normalize-space()]'
        ).re_first(r",\s([A-Za-z]{2})\s")
        item["Zip"] = response.xpath(
            './/*[@class="address"]/text()[normalize-space()]'
        ).re_first(r"\s(\d{5})")
        for res in response.xpath('.//*[@class="views-row"]'):
            FullName = self.clean_text(
                res.xpath('.//*[@class="title"]/text()').extract_first()
            )
            parts = FullName.split(", ")
            if len(parts) == 2:
                item["FirstName"] = self.clean_text(parts[1])
                item["LastName"] = self.clean_text(parts[0])
            else:
                print(
                    "\n\nUnable to extract first name and last name from the given string."
                )
                item["FirstName"] = None
                item["LastName"] = None
            item["Title"] = self.clean_text(
                res.xpath('.//*[@class="field job-title"]/text()').extract_first()
            )
            item["Phone"] = self.clean_text(
                res.xpath(
                    './/*[@class="field phone"]//text()[normalize-space()]'
                ).extract_first()
            )
            item["Email"] = self.clean_text(
                res.xpath(
                    './/*[@class="field email"]//text()[normalize-space()]'
                ).extract_first()
            )
            yield item

        # Handling pagination
        next_page = response.xpath(
            './/*[*[@title="Current page"]]/following-sibling::li[1]/a/@href'
        ).extract_first()
        if next_page:
            url = response.urljoin(next_page)
            yield scrapy.Request(url, headers=self.headers, callback=self.parse)
