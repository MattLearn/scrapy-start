import scrapy
from  scrapytutorial.items import BookProduct
from scrapytutorial.itemsloader import BookProductLoader


class BooksSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ['chocolate.co.uk']
    start_urls = ["https://www.chocolate.co.uk/collections/all"]

    def parse(self, response):
         products = response.css('product-item')
         #product_item = BookProduct()
         for product in products:
              #using an item loader
              bookloader = BookProductLoader(item = BookProduct(), selector = product)
              bookloader.add_css('name','a.product-item-meta__title::text')
              bookloader.add_css('price', 'span.price', re='<span class="price">\n              <span class="visually-hidden">Sale price</span>(.*)</span>')
              bookloader.add_css('url', 'div.product-item-meta a::attr(href)')
              yield bookloader.load_item()
              
              #scrapy items info grab
              #product_item['name'] = product.css('a.product-item-meta__title::text').get()
              #product_item['price'] = product.css('span.price').get().replace('<span class="price">\n              <span class="visually-hidden">Sale price</span>','').replace('</span>','')
              #product_item['url'] = product.css('div.product-item-meta a').attrib['href']
              #yield product_item
              
              #base tutorial info grab
              #yield{
              #          'name':product.css('a.product-item-meta__title::text').get(),
              #          'price':product.css('span.price').get().replace('<span class="price">\n              <span class="visually-hidden">Sale price</span>','').replace('</span>',''),
              #          'url':product.css('div.product-item-meta a').attrib['href']
              #}
         
         next_page = response.css('[rel="next"] ::attr(href)').get()
         
         if next_page is not None:
            next_page_url = 'https://www.chocolate.co.uk' +next_page
            yield response.follow(next_page_url, callback=self.parse)