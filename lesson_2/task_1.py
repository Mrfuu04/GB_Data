import requests
from bs4 import BeautifulSoup
from pandas import DataFrame, concat as pconcat


class MyError(Exception):
    def __init__(self, message='Что-то пошло не так'):
        self.message = message
        super().__init__(self.message)


class Parser:

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/98.0.4758.102 Safari/537.36'}

    def export_to_csv(self, file_name, vacancy_name):
        hh = self._parse_hh(vacancy_name)
        superjob = self._parse_superjob(vacancy_name)

        price_hh = []
        for i in hh:
            price_hh.append(i.pop('Зарплата'))
        res_hh = DataFrame(hh).join(DataFrame(price_hh))

        price_super = []
        for i in superjob:
            price_super.append(i.pop('Зарплата'))
        res_super = DataFrame(superjob).join(DataFrame(price_super))

        res_super = res_super[['Название', 'min', 'max', 'valute', 'Сайт', 'Ссылка на вакансию']]
        res_hh = res_hh[['Название', 'min', 'max', 'valute', 'Сайт', 'Ссылка на вакансию']]

        for_export = pconcat([res_super, res_hh])
        for_export.to_csv(file_name+'.csv', encoding='utf-8-sig')


    def _check_connection(self, url, headers, params):
        try:
            response = requests.get(url, headers=self.headers, params=params)
            if response.ok:
                return True
            else:
                raise MyError(message=f'Проблемы, {response.ok}')
        except Exception:
            raise MyError

    def _parse_superjob(self, vacancy_name):
        base_url = 'https://volgograd.superjob.ru/'
        vacancy_search = '/vacancy/search'
        params = {'keywords': {vacancy_name}, 'page': 1}

        self._check_connection(base_url + vacancy_search, headers=self.headers, params=params)

        result = []
        while True:
            response = requests.get(base_url + vacancy_search, headers=self.headers, params=params)
            dom = BeautifulSoup(response.text, 'html.parser')
            item = dom.find_all('div', {'class': 'f-test-search-result-item'})

            if len(item) == 0:
                break

            for vacancy in item:
                main_data = {}
                try:
                    link_title = vacancy.find('a', {'class': 'icMQ_'})
                    title = link_title.getText()
                    link = base_url + link_title.get('href')

                    try:
                        price = vacancy.find('span', {'class': '_2Wp8I'}).getText()
                        if price.startswith('от'):
                            checker = price.replace(' ', '').split()
                            min_price = int(''.join([x for x in checker if x.isdigit()]))
                            reward = {'min': min_price, 'max': None, 'valute': checker[-1]}

                        elif price.startswith('до'):
                            checker = price.replace(' ', '')
                            max_price = int(''.join([x for x in checker if x.isdigit()]))
                            reward = {'min': None, 'max': max_price, 'valute': checker.split()[-1]}

                        else:
                            checker = price.replace(' ', '').split('—')
                            if len(checker) > 1:
                                min_price, max_price = int(checker[0]), int(
                                    ''.join([x for x in checker if x.isdigit()]))
                                valute = price.split(' ')[-1]
                                reward = {'min': min_price, 'max': max_price, 'valute': valute}
                            else:
                                min_price, max_price = None, None
                                reward = {'min': min_price, 'max': max_price, 'valute': None}
                    except AttributeError:
                        reward = {'min': None, 'max': None, 'valute': None}

                    main_data['Название'] = title
                    main_data['Зарплата'] = reward
                    main_data['Ссылка на вакансию'] = link
                    main_data['Сайт'] = base_url

                    result.append(main_data)
                except Exception:
                    pass

            params['page'] += 1
        return result

    def _parse_hh(self, vacancy_name):
        base_url = 'https://volgograd.hh.ru'
        vacancy_search = '/search/vacancy'

        params = {'clusters': 'true', 'text': vacancy_name, 'ored_clusters': 'true', 'enable_snippets': 'true',
                  'area': 24,
                  'page': 0, 'hhtmFrom': 'vacancy_search_list'}

        self._check_connection(base_url + vacancy_search, headers=self.headers, params=params)

        result = []
        while True:

            response = requests.get(base_url + vacancy_search, headers=self.headers, params=params)
            dom = BeautifulSoup(response.text, 'html.parser')
            item = dom.find_all('div', {'class': 'vacancy-serp-item'})

            if len(item) == 0:
                break

            for vacancy in item:
                main_data = {}
                link_title = vacancy.find('a', {'data-qa': 'vacancy-serp__vacancy-title'})
                link = link_title.get('href')
                title = link_title.getText()

                try:
                    price = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'}).getText()
                    if price.startswith('от'):
                        checker = price.replace(' ', '')
                        reward = {'min': checker.split()[1], 'max': None, 'valute': checker.split()[-1]}
                    elif price.startswith('до'):
                        checker = price.replace(' ', '')
                        reward = {'min': None, 'max': checker.split()[1], 'valute': checker.split()[-1]}
                    else:
                        checker = price.replace(' ', '').split('–')
                        min_price = checker[0]
                        max_price = checker[1].split()[0]
                        valute = checker[1].split()[1]
                        reward = {'min': min_price, 'max': max_price, 'valute': valute}
                except AttributeError:
                    reward = {'min': None, 'max': None, 'valute': None}
                main_data['Название'] = title
                main_data['Зарплата'] = reward
                main_data['Ссылка на вакансию'] = link
                main_data['Сайт'] = base_url

                result.append(main_data)

            params['page'] += 1

        return result

    def parse_jobs(self, vacancy_name):
        result = [self._parse_hh(vacancy_name), self._parse_superjob(vacancy_name)]
        return result


def check_work(vacancy):
    parser = Parser()
    parser.export_to_csv('main', 'дизайнер')


if __name__ == '__main__':
    check_work('python')
