from pymongo import MongoClient
import parse_hh
from pprint import pprint


class inMongoDB:
    def __init__(self):
        self.client = MongoClient('localhost', 27017)

    def _is_vacancy_in_bd(self, collection, vacancy):
        """Проверять наличие в БД будем по ссылке на вакансию"""
        if collection.find_one({'Ссылка на вакансию': vacancy.get('Ссылка на вакансию')}) is None:
            return True
        return False

    def __init_db(self, db_name, collection_name):
        db = self.client[db_name]
        collection = db[collection_name]
        return db, collection

    def put_inside_mongo(self, db_name: str, collection_name: str, vacancy_data: list):
        db, collection = self.__init_db(db_name, collection_name)

        for vacancy in vacancy_data:
            if self._is_vacancy_in_bd(collection, vacancy):
                collection.insert_one(vacancy)
            else:
                db.garbage.insert_one(vacancy)

    def get_vacancy_from_reward(self, db_name: str, collection_name: str, reward):
        db, collection = self.__init_db(db_name, collection_name)

        for doc in collection.find({'$or': [{'Зарплата.min': {'$gt': reward}}, {'Зарплата.max': {'$gt': reward}}]}):
            pprint(doc)


if __name__ == '__main__':
    # Инициализация и парсинг данных
    parser = parse_hh.Parser()
    vacancy_data = parser.parse_jobs('Python')

    # Инициализация БД
    test = inMongoDB()
    test.put_inside_mongo('hhjobs', 'vacancy', vacancy_data)
    test.get_vacancy_from_reward('hhjobs', 'vacancy', 150000)
