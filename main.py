from pathlib import Path

import yaml
from loguru import logger

from core.config_loader import ConfigLoader
from core.parser_engine import ParserEngine


def main():
    # указываю название сайта (для получения настроек из yaml файла) и адрес
    site = 'creepypasta'
    url = 'https://www.creepypasta.com/mistress-inviere/'

    try:
        config = ConfigLoader.load(site)
        logger.info(f'Available configs :{ConfigLoader.list_available()}')
        parser = ParserEngine(config)
        results = parser.parse(url, max_pages=1)

        # Сохранение результатов
        with open(f"output/{site}_text.txt", "w") as f:

            for result in results:
                sentences = result.split('. ')
                # logger.info(f" {sentences = } ")
                for sentence in sentences:
                    if sentence.endswith('.'):
                        sentence = sentence.strip()
                        f.write(sentence + '\n')
                    else:
                        f.write(sentence + '.' + '\n')

        logger.info(f'Parsing {len(results)} sentences successfully')

    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
