import requests


class WikipediaClient:
    """
    Клиент для взаимодействия с Wikipedia API.
    """

    BASE_URL = f"https://ru.wikipedia.org/w/api.php"

    HEADERS = {
        "User-Agent": "Mozilla/5.0"
    }
    TIMEOUT = 10

    def _make_request(self, params, url: str | None = None):
        try:
            response = requests.get(url=url, params=params, headers=self.HEADERS, timeout=self.TIMEOUT)
            response.raise_for_status()
            return response.json()
        except requests.ConnectionError as e:
            # print(f'Ошибка подключения: {e}')
            return None
        except requests.Timeout as e:
            # print(f'Время ожидания превышено: {e}')
            return None
        except requests.HTTPError as e:
            # print(f'Ошибка HTTP: {e}')
            return None


    def get_summary(self, term, lang="ru", chars=500):
        url = f'https://{lang}.wikipedia.org/w/api.php'
        params = {
            "action": "query",
            "format": "json",
            "prop": "extracts",
            "exintro": True,
            "explaintext": True,
            "redirects": 1,
            "titles": term
        }

        data = self._make_request(params=params, url=url)
        if not data:
            # print(f'Определение по запросу {term} на языке {lang} не найдено')
            return None
        
        pages = data.get("query", {}).get("pages", {})
        if not pages or '-1' in pages:
            # print(f'Определение по запросу {term} на языке {lang} не найдено')
            return None
        else:
            for content in pages.values():
                extract = content.get("extract")
                if extract:
                    return extract[:chars]
            return None


    def get_full_article(self, term, lang="ru"):
        url = f'https://{lang}.wikipedia.org/w/api.php'
        params = {
            "action": "query",
            "format": "json",
            "prop": "extracts",
            "exintro": False,
            "explaintext": True,
            "redirects": 1,
            "titles": term
        }

        data = self._make_request(params=params, url=url)
        if not data:
            # print(f'Определение по запросу {term} на языке {lang} не найдено')
            return None
        
        pages = data.get("query", {}).get("pages", {})
        if not pages or '-1' in pages:
            # print(f'Определение по запросу {term} на языке {lang} не найдено')
            return None
        else:
            for content in pages.values():
                extract = content.get("extract")
                if extract:
                    return extract
            return None


    def get_article_url(self, term: str, lang="ru"):
        url = f'https://{lang}.wikipedia.org/w/api.php'
        params = {
            "action": "query",
            "format": "json",
            "prop": "info",
            "inprop": "url",
            "redirects": 1,
            "titles": term
        }
        data = self._make_request(params=params, url=url)
        if not data:
            # print(f'Определение по запросу {term} на языке {lang} не найдено')
            return None
        
        pages = data.get("query", {}).get("pages", {})
        if not pages or '-1' in pages:
            # print(f'Определение по запросу {term} на языке {lang} не найдено')
            return None
        else:
            for content in pages.values():
                fullurl = content.get("fullurl")
                if fullurl:
                    return fullurl
            return None
