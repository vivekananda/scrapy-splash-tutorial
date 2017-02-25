import scrapy

from scrapy.spiders import Spider
from scrapy.selector import Selector
from fara.items import FaraItem
import datetime

from scrapy_splash import SplashRequest


class FaraSpider(scrapy.Spider):
    name = "faraspider"
    allowed_domains = ["www.fara.gov"]
    start_urls = ["https://efile.fara.gov/pls/apex/f?p=171:130:0::NO:RP,130:P130_DATERANGE:N"]

    # allowed_domains  = [ "www.deal70.com" ]
    # start_urls = [ "http://www.deal70.com" ]

    def start_requests(self):
        script = """
function main(splash)
  local url = splash.args.url
  assert(splash:go(url))
  assert(splash:wait(2))
  assert(splash:runjs("gReport.navigate.paginate('pgR_min_row=%dmax_rows=15rows_fetched=15')"))
  assert(splash:wait(20))

  return {
    html = splash:html(),
    png = splash:png(),
    har = splash:har(),
  }
end
        """
        for url in self.start_urls:
            for i in range(511,520,15): #513

                lauscript = script%(i,)
                print(lauscript)
                yield SplashRequest(url, self.parse,
                                    endpoint='http://192.168.43.145:8050/execute',
                                    args={'lua_source': lauscript },
                                # meta={
                                #     'splash': {
                                #         'endpoint': 'http://192.168.43.145:8050/render.html',
                                #         'args': {'renderall': 1, 'iframes': 1, 'script': 1, 'timeout': 60}
                                #     }
                                # }
                                )
        """
        yield scrapy.Request(url, self.parse, meta={
                'splash': {
                    'endpoint': 'http://192.168.43.145:8050/render.html',
                    'args': {'renderall': 1, 'iframes': 1, 'script': 1, 'timeout': 60, 'lua_source': script}
                }
            })
        #"""
    def parse(self, response):
        sel = Selector(response=response)
        cur_country = ""
        for node in sel.xpath('//table[@class="apexir_WORKSHEET_DATA"]//tr'):
            #print "-" * 100
            #print node
            t_country = node.xpath('.//span[@class="apex_break_headers"]/text()').extract_first()
            if t_country:
                cur_country = t_country
                # logger.info()
            if node.xpath('./td//text()').extract():
                faraitem = FaraItem()
                faraitem["country"] = cur_country
                faraitem["url"] = "https://efile.fara.gov/pls/apex/" + node.xpath('.//@href').extract_first()
                faraitem["state"] = node.xpath('.//td[5]/text()').extract_first()
                faraitem["reg_num"] = node.xpath('.//td[7]/text()').extract_first()
                taddress = node.xpath('.//td[4]/text()').extract()
                taddress = ' '.join( [t.strip() for t in taddress])
                faraitem["address"] = taddress
                faraitem["foreign_principal"] = node.xpath('.//td[2]/text()').extract_first()

                tdate = node.xpath('.//td[8]/text()').extract_first()
                if tdate:
                    faraitem["date"] = datetime.datetime.strptime(tdate, "%m/%d/%Y")
                faraitem["registrant"] = node.xpath('.//td[6]/text()').extract_first()
                faraitem["exhibit_url"] = ""  # TODO: go to url and fetch the exhibit url

                yield faraitem

        # sel = Selector(response)
        # print("="*100)
        # for tr_el in sel.xpath('//table[@class="apexir_WORKSHEET_DATA"]/tr'):
        #     print("-"*100)
        #     print(tr_el.extract())
        # print("="*100)
        # print(sel.xpath('//div[@id="page"]/text()').extract())
        # print("came here" + "=" * 20)
        pass
