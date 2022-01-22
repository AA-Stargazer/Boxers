import scrapy
from scrapy.spiders.init import InitSpider
from boxrec.items import BoxrecItem
from scrapy.loader import ItemLoader
from scrapy.shell import inspect_response
import logging
import time
class BoxerFromRatingSpider(InitSpider):
    name = 'boxer'
    custom_settings = {
        'ITEM_PIPELINES': {
            'boxrec.pipelines.SQLitePipeline': 400
        }
    }


    login_page = 'https://boxrec.com/en/login'
    id_list = []
    with open('pro_box_id_0', 'r') as file:
        for _id in file.readlines():
            id_list.append(_id)
    
    start_urls = [f'https://boxrec.com/en/amateurboxer/{_id}' for _id in id_list]

   .
   .
   .



    def parse(self, response):
        website_logo = response.xpath('//div[@class="logo"]')
        if not website_logo:
            yield scrapy.Request(url=response.url, dont_filter=False)
        else:
            print('\n\n') 
            print(response.xpath('/html/body/div[3]/div/div[2]/a[1]/text()').get())
            print('\n\n')
            loader = ItemLoader(item=BoxrecItem(), response=response)
            if response.xpath('(//div/h2/text())[1]').get() == 'Sorry, we could not find that person':
                pass
            else:
                loader.add_xpath('_id', '(//div/h2/text())[1]')
                # loader.add_xpath('circuit', '((//div/h2/text())[1]/following::div)[1]/text()')
                loader.add_xpath('circuit', '((//div/h2/text())[1]/following::div)[2]/text()') # amateur one, if there is.
                loader.add_xpath('name', '//td[@class="defaultTitleAlign"]/h1/text()')

                loader.add_xpath('win', '//tr[@class="profileTable"]/td[1]/div[@class="profileTablePhoto"]//tr[1]/td[1]/text()')
                loader.add_xpath('lose', '//tr[@class="profileTable"]/td[1]/div[@class="profileTablePhoto"]//tr[1]/td[2]/text()')
                loader.add_xpath('other_result', '//tr[@class="profileTable"]/td[1]/div[@class="profileTablePhoto"]//tr[1]/td[3]/text()')
                loader.add_xpath('win_ko', '//tr[@class="profileTable"]/td[1]/div[@class="profileTablePhoto"]//tr[2]/th[1]/text()')
                loader.add_xpath('lose_ko', '//tr[@class="profileTable"]/td[1]/div[@class="profileTablePhoto"]//tr[2]/th[2]/text()')

                loader.add_xpath('division', '//tr[@class="profileTable"]/td[2]//div[1]//tr/td/b[text()="division"]/parent::td/following-sibling::td/text()')
                loader.add_xpath('bouts', '//tr[@class="profileTable"]/td[2]//div[1]//tr/td/b[text()="bouts"]/parent::td/following-sibling::td/text()')
                loader.add_xpath('rounds', '//tr[@class="profileTable"]/td[2]//div[1]//tr/td/b[text()="rounds"]/parent::td/following-sibling::td/text()')
                loader.add_xpath('career', '//tr[@class="profileTable"]/td[2]//div[1]//tr/td/b[text()="career"]/parent::td/following-sibling::td/text()')

                loader.add_xpath('stance', '//tr[@class="profileTable"]/td[2]//div[2]//tr/td/b[text()="stance"]/parent::td/following-sibling::td/text()')
                loader.add_xpath('nationality', 'string(//tr[@class="profileTable"]/td[2]/div[2]//tr/td/b[text()="nationality"]/parent::td/following-sibling::td)')
                loader.add_xpath('height', '//tr[@class="profileTable"]/td[2]//div[2]//tr/td/b[text()="height"]/parent::td/following-sibling::td/text()')
                loader.add_xpath('reach', '//div[2]//tr/td/b[text()="reach"]/parent::td/following-sibling::td/text()')
                
                if response.xpath('//tr[@class="profileTable"]/td[2]//div[1]//tr/td/b[text()="status"]/parent::td/following-sibling::td/text()'):
                    loader.add_xpath('status', '//tr[@class="profileTable"]/td[2]//div[1]//tr/td/b[text()="status"]/parent::td/following-sibling::td/text()')
                else:
                    if response.xpath('//tr[@class="profileTable"]/td[2]//div//tr/td/b[text()="status"]/parent::td/following-sibling::td/text()'):
                        loader.add_xpath('status', '//tr[@class="profileTable"]/td[2]//div//tr/td/b[text()="status"]/parent::td/following-sibling::td/text()')


                yield loader.load_item()
