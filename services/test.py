from scrapy.crawler import CrawlerRunner
from craigslist.craigslist.spiders.craigbot import CraigbotSpider
from twisted.internet import reactor

from twisted.internet.task import LoopingCall
from scrapy.utils.log import configure_logging

# def run_crawl():
#     """
#     Run a spider within Twisted. Once it completes,
#     wait 5 seconds and run another spider.
#     """
#     runner = CrawlerRunner({
#         'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
#     })
#     deferred = runner.crawl(CraigbotSpider)
#     # you can use reactor.callLater or task.deferLater to schedule a function
#     deferred.addCallback(reactor.callLater, 5, run_crawl)
#     return deferred


# run_crawl()
# reactor.run()


configure_logging()
runner = CrawlerRunner()
task = LoopingCall(lambda: runner.crawl(CraigbotSpider()))
task.start(5)
reactor.run()
