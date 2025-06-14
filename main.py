from pathlib import Path

import yaml
from loguru import logger

from engines.parser_engine import ParserEngine


def load_config(site_name):
    config_path = Path(f"configs/{site_name}.yaml")
    if not config_path.exists():
        raise FileNotFoundError(f"Конфиг для {site_name} не найден")
    logger.info(f"Config for  {site_name} load successfully")
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def main():

    # указываю название сайта ( для получение настроек из yaml файла) и адрес
    site = 'creepypasta'
    url = 'https://www.creepypasta.com/mistress-inviere/'

    try:
        config = load_config(site)
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
