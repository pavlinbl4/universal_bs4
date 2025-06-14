from bs4 import BeautifulSoup
import requests
from loguru import logger


class ParserEngine:
    def __init__(self, config):
        self.config = config
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ..."
        })

    def _parse_page(self, soup):
        items = []
        for item in soup.select(self.config['selectors']['items']['list']):
            # logger.debug(item.text)
            items.append(item.text)
            # data = {}
            # for key, selector in self.config['selectors'].items():
            #     if key == 'items': continue
            #     logger.info(f'{key = }')
            #     if '::attr(' in selector:
            #         css_sel, attr = selector.split('::attr(')
            #         attr = attr.rstrip(')')
            #         elem = item.select_one(css_sel)
            #         data[key] = elem[attr] if elem else None
            #     else:
            #         elem = item.select_one(selector)
            #         data[key] = elem.get_text(strip=True) if elem else None
            # items.append(data)
            # logger.info(f'{data = }')
        return items

    def parse(self, url, max_pages=1):
        current_page = 1
        all_items = []

        while url and current_page <= max_pages:
            logger.info(f"Parsing page {current_page}")
            response = self.session.get(url)
            logger.info(f"Responce {response}")
            soup = BeautifulSoup(response.text, 'lxml')
            # посмотреть содержимое объекта soup
            # logger.info(f"Soup {soup}")

            all_items.extend(self._parse_page(soup))
            logger.info(f" {all_items  = } ")

            # Обработка пагинации
            if self.config['pagination']['type'] == 'url_param':
                current_page += 1
                url = f"{self.config['base_url']}?{self.config['pagination']['param']}={current_page}"
            else:
                url = None  # Реализация для других типов

            current_page += 1

        return all_items
