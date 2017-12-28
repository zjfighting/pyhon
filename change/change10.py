import scrapy
   
class GithubUserSpider(scrapy.Spider):
    name = 'github-user'
   
    @property
    def start_urls(self):
        url_tmpl = 'https://github.com/shiyanlou?page={}&tab=repositories'
        return (url_tmpl.format(i) for i in range(1, 5))
  
    def parse(self, response):
        for github in response.css('li.d-block'):
            yield{
                'name': github.css('div.mb-1 h3 a::text').re_first('\n\s*(.*    )'),
                'update_time': github.css('div.mt-2 relative-time::attr(date    time)').extract_first()
            }             