# -*- coding: utf-8 -*-
import re

import scrapy
import json

from ..items import LabelAddressItem

LABEL_DATA_URL = 'https://cn.etherscan.com/accounts.aspx/GetTableEntriesBySubLabel'
LOGIN_API_URL = 'https://cn.etherscan.com/login'
COOKIES = {
    '__cfduid': 'd021d4449bf83793d3b61aba8d73a58db1603881846',
    'ASP.NET_SessionId': 'mahxdjvbksrkgqxm1gobad45',
    '_pk_ses.10.1f5c': 1,
    '_pk_id.10.1f5c': 'ab8c241b68e8b2c8.1603881859.1.1603884775.1603881859.'
}


class LabelSpider(scrapy.Spider):
    name = 'label_spider'
    allowed_domains = ['*']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # 读取命令行用户名、密码、爬取的标签
        self.username = kwargs.get('username')
        self.password = kwargs.get('password')
        self.label = kwargs.get('label')
        self.data = json.loads(
            '{"dataTableModel":{"draw":1,"columns":[{"data":"address","name":"","searchable":true,"orderable":false,"search":{"value":"","regex":false}},{"data":"nameTag","name":"","searchable":true,"orderable":false,"search":{"value":"","regex":false}},{"data":"balance","name":"","searchable":true,"orderable":true,"search":{"value":"","regex":false}},{"data":"txnCount","name":"","searchable":true,"orderable":true,"search":{"value":"","regex":false}}],"order":[{"column":1,"dir":"asc"}],"start":0,"length":25,"search":{"value":"","regex":false}},"labelModel":{"label":"%s"}}' % self.label
        )

    def start_requests(self):
        # 判断参数是否齐全
        if self.username is None or self.password is None or self.label is None:
            self.crawler.engine.close_spider(self, 'arguments lost')

        # TODO:模拟登录获取cookie

        # 尝试发起第一页请求，并获取到总页数
        yield scrapy.Request(
            url=LABEL_DATA_URL,
            method='POST',
            body=json.dumps(self.data),
            callback=self.parse_start_page,
        )

    def parse_start_page(self, response):
        rsp_data = json.loads(response.body.decode())
        for i in range(int(rsp_data['d']['currentPage']) + 1, int(rsp_data['d']['totalPage']) + 1):
            self.data['dataTableModel']['draw'] = i
            self.data['dataTableModel']['start'] = (i - 1) * 25
            yield scrapy.Request(
                url=LABEL_DATA_URL,
                method='POST',
                body=json.dumps(self.data),
                callback=self.parse_page,
                dont_filter=True,
                cookies=COOKIES,
            )

    def parse_page(self, response):
        rsp_data = json.loads(response.body.decode())
        for row in rsp_data['d']['data']:
            item = LabelAddressItem()
            item['address'] = re.sub('<.*?>', '', row['address'])
            item['name_tag'] = row['nameTag']
            item['balance'] = re.sub(' Ether|<.*?>', '', row['balance'])
            item['txn_count'] = row['txnCount']
            item['label'] = self.label
            yield item
