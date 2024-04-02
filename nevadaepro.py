import scrapy
import os


class NevadaEPro(scrapy.Spider):
    name = "nevadaepro"
    attachments_directory = "Attachments Files"
    custom_settings = {"FEED_FORMAT": "json", "FEED_URI": "nevadaepro.json"}

    def start_requests(self):
        """
        Method to initiate the spider by sending a request to the starting URL.
        """
        url = "https://nevadaepro.com/bso/view/search/external/advancedSearchBid.xhtml?openBids=true"

        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
            "cache-control": "max-age=0",
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
            headers=headers,
            meta={"num": 0},
        )

    def parse(self, response):
        half_urls = response.xpath('//*[@id="bidSearchResultsForm:bidResultId"]').re(
            r'role="row"&gt;&lt;td role="gridcell"&gt;&lt;a href="(.*?)"'
        ) or response.xpath('//*[@id="bidSearchResultsForm:bidResultId_data"]').re(
            r'role\="row"><td role\="gridcell"><a href\="(.*?)"'
        )
        num = response.meta.get("num")
        next_page = response.xpath(
            './/*[contains(@class,"ui-paginator-next") and not(contains(@class,"disabled"))]'
        ).extract_first()
        _csrf = response.xpath('//form/input[@name="_csrf"]/@value').extract_first()
        javaxFacesViewState = response.xpath(
            '//form/input[@name="javax.faces.ViewState"]/@value'
        ).extract_first()

        for h_url in half_urls:
            url = response.urljoin(h_url)
            headers = {
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
                "cache-control": "max-age=0",
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
                url, method="GET", headers=headers, callback=self.detail_page
            )

        if next_page:
            headers = {
                "accept": "application/xml, text/xml, */*; q=0.01",
                "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
                "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                "faces-request": "partial/ajax",
                "origin": "https://nevadaepro.com",
                "referer": "https://nevadaepro.com/bso/view/search/external/advancedSearchBid.xhtml?openBids=true",
                "sec-ch-ua": '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": '"Windows"',
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
                "x-requested-with": "XMLHttpRequest",
            }
            num += len(half_urls)
            body = f"javax.faces.partial.ajax=true&javax.faces.source=bidSearchResultsForm%3AbidResultId&javax.faces.partial.execute=bidSearchResultsForm%3AbidResultId&javax.faces.partial.render=bidSearchResultsForm%3AbidResultId&bidSearchResultsForm%3AbidResultId=bidSearchResultsForm%3AbidResultId&bidSearchResultsForm%3AbidResultId_pagination=true&bidSearchResultsForm%3AbidResultId_first={num}&bidSearchResultsForm%3AbidResultId_rows=25&bidSearchResultsForm%3AbidResultId_encodeFeature=true&bidSearchResultsForm=bidSearchResultsForm&_csrf={_csrf}&openBids=true&javax.faces.ViewState={javaxFacesViewState}"
            yield scrapy.Request(
                response.url,
                method="POST",
                body=body,
                dont_filter=True,
                headers=headers,
                meta={"num": num},
                callback=self.parse,
            )

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

    def create_directory_if_not_exists(self, directory):
        """
        Create a directory if it doesn't exist.
        """
        if not os.path.exists(directory):
            os.makedirs(directory)

    def save_file_in_directory(self, directory, filename, content):
        """
        Save content in a file within the specified directory.
        """
        with open(os.path.join(directory, filename), "wb") as f:
            f.write(content)

    def add_pdf_extension(self, filename):
        # Check if the filename has an extension
        if "." not in filename:
            # If not, add '.pdf' extension
            filename += ".pdf"
        return filename

    def detail_page(self, response):
        """
        Parses the details page response and extracts relevant information.
        """
        item = {}
        item["Bid Number"] = self.clean_text(
            response.xpath(
                './/*[contains(text(),"Bid Number:")]/following-sibling::td[1]/text()'
            ).extract_first()
        )
        item["Description"] = self.clean_text(
            response.xpath(
                './/*[contains(text(),"Description:")]/following-sibling::td[1]/text()'
            ).extract_first()
        )
        item["Bid Opening Date"] = self.clean_text(
            response.xpath(
                './/*[contains(text(),"Bid Opening Date:")]/following-sibling::td[1]/text()'
            ).extract_first()
        )
        item["Purchaser"] = self.clean_text(
            response.xpath(
                './/*[contains(text(),"Purchaser:")]/following-sibling::td[1]/text()'
            ).extract_first()
        )
        item["Organization"] = self.clean_text(
            response.xpath(
                './/*[contains(text(),"Organization:")]/following-sibling::td[1]/text()'
            ).extract_first()
        )
        item["Department"] = self.clean_text(
            response.xpath(
                './/*[contains(text(),"Department:")]/following-sibling::td[1]/text()'
            ).extract_first()
        )
        item["Location"] = self.clean_text(
            response.xpath(
                './/*[contains(text(),"Location:")]/following-sibling::td[1]/text()'
            ).extract_first()
        )
        item["Fiscal Year"] = self.clean_text(
            response.xpath(
                './/*[contains(text(),"Fiscal Year:")]/following-sibling::td[1]/text()'
            ).extract_first()
        )
        item["Type Code"] = self.clean_text(
            response.xpath(
                './/*[contains(text(),"Type Code:")]/following-sibling::td[1]/text()'
            ).extract_first()
        )
        item["Allow Electronic Quote"] = self.clean_text(
            response.xpath(
                './/*[contains(text(),"Allow Electronic Quote:")]/following-sibling::td[1]/text()'
            ).extract_first()
        )
        item["Alternate Id"] = self.clean_text(
            response.xpath(
                './/*[contains(text(),"Alternate Id:")]/following-sibling::td[1]/text()'
            ).extract_first()
        )
        item["Required Date"] = self.clean_text(
            response.xpath(
                './/*[contains(text(),"Required Date:")]/following-sibling::td[1]/text()'
            ).extract_first()
        )
        item["Available Date"] = self.clean_text(
            response.xpath(
                './/*[contains(text(),"Available Date")]/following-sibling::td[1]/text()'
            ).extract_first()
        )
        item["Info Contact"] = self.clean_text(
            response.xpath(
                './/*[contains(text(),"Info Contact:")]/following-sibling::td[1]/text()'
            ).extract_first()
        )
        item["Bid Type"] = self.clean_text(
            response.xpath(
                './/*[contains(text(),"Bid Type:")]/following-sibling::td[1]/text()'
            ).extract_first()
        )
        item["Informal Bid Flag"] = self.clean_text(
            response.xpath(
                './/*[contains(text(),"Informal Bid Flag:")]/following-sibling::td[1]/text()'
            ).extract_first()
        )
        item["Purchase Method"] = self.clean_text(
            response.xpath(
                './/*[contains(text(),"Purchase Method:")]/following-sibling::td[1]/text()'
            ).extract_first()
        )
        item["Blanket/Contract Begin Date"] = self.clean_text(
            response.xpath(
                './/*[contains(text(),"Blanket/Contract Begin Date:")]/following-sibling::td[1]/text()'
            ).extract_first()
        )
        item["Blanket/Contract End Date"] = self.clean_text(
            response.xpath(
                './/*[contains(text(),"Blanket/Contract End Date:")]/following-sibling::td[1]/text()'
            ).extract_first()
        )
        item["Ship-to Address"] = self.clean_and_join(
            response.xpath(
                './/*[contains(text(),"Ship-to Address:")]/following-sibling::td[1]/text()'
            ).extract()
        )
        item["Bill-to Address"] = self.clean_and_join(
            response.xpath(
                './/*[contains(text(),"Bill-to Address:")]/following-sibling::td[1]/text()'
            ).extract()
        )

        yield item

        url = "https://nevadaepro.com/bso/external/bidDetail.sdo"
        _csrf = response.xpath('//form/input[@name="_csrf"]/@value').get()
        mode = response.xpath('//form/input[@name="mode"]/@value').get() or "download"
        bidId = response.xpath('//form/input[@name="bidId"]/@value').get()
        docId = response.xpath('//form/input[@name="docId"]/@value').get()
        currentPage = response.xpath('//form/input[@name="currentPage"]/@value').get()
        querySql = response.xpath('//form/input[@name="querySql"]/@value').get()
        downloadFileNbr = response.xpath(
            '//*[contains(text(),"File Attachments:")]//following::*[1]//a'
        )
        file_data = {}
        for files in downloadFileNbr:
            FileNum = files.xpath("./@href").re_first(r"downloadFile\('(\d+)'\)")
            FileName = files.xpath("./text()").extract_first()
            file_data[FileNum] = self.add_pdf_extension(FileName)
        itemNbr = response.xpath('//form/input[@name="itemNbr"]/@value').get()
        parentUrl = response.xpath('//form/input[@name="parentUrl"]/@value').get()
        fromQuote = response.xpath('//form/input[@name="fromQuote"]/@value').get()
        destination = response.xpath('//form/input[@name="destination"]/@value').get()
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
            "cache-control": "max-age=0",
            "content-type": "application/x-www-form-urlencoded",
            "cookie": f"XSRF-TOKEN={_csrf};",
            "origin": "https://nevadaepro.com",
            "referer": "https://nevadaepro.com/bso/external/bidDetail.sdo?docId=04SOS-S2794&external=true&parentUrl=close",
            "sec-ch-ua": '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        }
        for FileNbr, FileName in file_data.items():
            body = f"_csrf={_csrf}&mode={mode}&bidId={bidId}&docId={docId}&currentPage={currentPage}&querySql={querySql}&downloadFileNbr={FileNbr}&itemNbr={itemNbr}&parentUrl={parentUrl}&fromQuote={fromQuote}&destination={destination}"
            formdata = {
                element.split("=")[0]: element.split("=")[1]
                for element in body.split("&")
            }
            yield scrapy.FormRequest(
                url,
                method="POST",
                formdata=formdata,
                headers=headers,
                cookies={
                    "XSRF-TOKEN": _csrf,
                },
                meta={
                    "dont_merge_cookies": True,
                    "BidNumber": item["Bid Number"],
                    "FileName": FileName,
                },
                callback=self.saving_files,
            )

    def saving_files(self, response):
        """
        Saves the downloaded files in the appropriate directory.
        """
        BidNumber = response.meta.get("BidNumber")
        FileName = response.meta.get("FileName")
        bid_directory = os.path.join(self.attachments_directory, BidNumber)
        self.create_directory_if_not_exists(bid_directory)
        self.save_file_in_directory(bid_directory, FileName, response.body)
