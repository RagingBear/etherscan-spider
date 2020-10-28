# etherscan-spider
Ethereum data spider on etherscan

## Targets

- Simulated login cn.etherscan.cn(pending)
- Crawl labeled address(done)
- Tracking transaction links(pending)
- more...

## Dependency
- Python3.5 or higher version
- Scrapy1.7 or higher version

## Crawl labeled address
Using **label keyword**, **etherscan username**, **etherscan password** to start this spider, which means you need to have a account on etherscan(if not, click (here)[https://cn.etherscan.com/register]).
Command format:```scrapy crawl -a label=<label keyword> -a username=<etherscan username> -a password=etherscan password```
Example:```scrapy crawl -a label=phish-hack -a username=geek -a password=123456```
