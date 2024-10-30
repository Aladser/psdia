from django.core.cache import cache


class ManagedCache:
    """Управляемый кэш"""

    _store_key = "_store_key_"

    @staticmethod
    def get(key: str):
        """
        Получает данные из кэша
        :param key: ключ
        """

        return cache.get(key)

    @staticmethod
    def write(key: str, data):
        """
        Записывает данные в кэш
        :param key: ключ
        :param data: данные
        """

        # проверяем существование хранилища ключей кэша
        key_store_list = cache.get(ManagedCache._store_key)
        if key_store_list is None:
            key_store_list = []
            cache.set(ManagedCache._store_key, key_store_list)

        # проверяем наличие ключа в хранилище
        if key not in key_store_list:
            key_store_list.append(key)
            cache.set(ManagedCache._store_key, key_store_list)

        cache.set(key, data)

    @staticmethod
    def remove(key:str = None):
        """
        Удаляет кэш. Если не указан ключ, удаляется весь кэш
        :param key: ключ
        """

        if key:
            cache.delete(key)
        else:
            key_store_list = cache.get(ManagedCache._store_key)
            if key_store_list is not None:
                [cache.delete(key) for key in key_store_list]
            cache.delete(ManagedCache._store_key)
