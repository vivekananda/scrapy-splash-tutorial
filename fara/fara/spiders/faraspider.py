import scrapy

from scrapy.spiders import Spider
from scrapy.selector import Selector
from fara.items import FaraItem
import datetime

from scrapy_splash import SplashRequest
from fara.settings import SPLASH_REQUEST_ENDPOINT, SCRAPY_REQUEST_ENDPOINT


class FaraSpider(scrapy.Spider):
    name = "faraspider"
    allowed_domains = ["www.fara.gov"]
    start_urls = ["https://efile.fara.gov/pls/apex/f?p=171:130:0::NO:RP,130:P130_DATERANGE:N"]

    script = """
function main(splash)
  local url = splash.args.url
  assert(splash:go(url))
  assert(splash:wait(2))
  assert(splash:runjs("gReport.navigate.paginate('pgR_min_row=%dmax_rows=15rows_fetched=15')"))
  assert(splash:wait(2))

  return {
    html = splash:html(),
    png = splash:png(),
    har = splash:har(),
  }
end
        """

    def start_requests(self):
        for url in self.start_urls:
            for i in range(1, 10, 15):
                lauscript = self.script % (i,)
                yield SplashRequest(url, self.parse,
                                    endpoint=SPLASH_REQUEST_ENDPOINT,
                                    args={'lua_source': lauscript},
                                    )

    def parse(self, response):

        sel = Selector(response=response)

        pagination_data = sel.xpath('//td[@class="pagination"]/span[@class="fielddata"]//text()').extract()
        if pagination_data:
            tokens = (" ".join([p.strip() for p in pagination_data])).split()
            if int(tokens[0].strip()) == 1 and len(tokens) >= 5:
                total_recods = int(tokens[4].strip())

                for i in range(16, total_recods + 1, 15):  # 513
                    lauscript = self.script % (i,)
                    yield SplashRequest(response.url, self.parse,
                                        endpoint=SPLASH_REQUEST_ENDPOINT,
                                        args={'lua_source': lauscript},
                                        dont_filter=True
                                        )

        cur_country = ""
        for node in sel.xpath('//table[@class="apexir_WORKSHEET_DATA"]//tr'):
            t_country = node.xpath('.//span[@class="apex_break_headers"]/text()').extract_first()
            if t_country:
                cur_country = t_country
            if node.xpath('./td//text()').extract():
                faraitem = FaraItem()
                faraitem["country"] = cur_country
                item_url = "https://efile.fara.gov/pls/apex/" + node.xpath('.//@href').extract_first()
                faraitem["url"] = item_url
                faraitem["state"] = node.xpath('.//td[5]/text()').extract_first()
                faraitem["reg_num"] = node.xpath('.//td[7]/text()').extract_first()
                taddress = node.xpath('.//td[4]/text()').extract()
                taddress = ' '.join([t.strip() for t in taddress])
                faraitem["address"] = taddress
                faraitem["foreign_principal"] = node.xpath('.//td[2]/text()').extract_first()

                tdate = node.xpath('.//td[8]/text()').extract_first()
                if tdate:
                    faraitem["date"] = datetime.datetime.strptime(tdate, "%m/%d/%Y").isoformat()
                faraitem["registrant"] = node.xpath('.//td[6]/text()').extract_first()

                new_req = SplashRequest(item_url, self.parse_page2,
                                        endpoint=SCRAPY_REQUEST_ENDPOINT,
                                        args={},
                                        dont_filter=True)

                new_req.meta['faraitem'] = faraitem
                yield new_req

    def parse_page2(self, response):
        faraitem = response.meta["faraitem"]
        sel = Selector(response=response)
        faraitem["exhibit_url"] = ",".join(sel.xpath('//td[@headers="DOCLINK"]/a/@href').extract())
        yield faraitem
