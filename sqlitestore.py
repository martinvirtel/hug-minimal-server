"""sqlitedict store for hug

"""

import sqlitedict

from hug.exceptions import StoreKeyNotFound



class SqliteStore:
    """
    store class uwith sqlite
    """
    def __init__(self,filepath,**kwargs):
        self._data = sqlitedict.SqliteDict(filepath,**kwargs)

    def get(self, key):
        """Get data for given store key. Raise hug.exceptions.StoreKeyNotFound if key does not exist."""
        try:
            data = self._data[key]
        except KeyError:
            raise StoreKeyNotFound(key)
        return data

    def exists(self, key):
        """Return whether key exists or not."""
        return key in self._data

    def set(self, key, data):
        """Set data object for given store key."""
        self._data[key] = data
        self._data.commit()

    def delete(self, key):
        """Delete data for given store key."""
        if key in self._data:
            del self._data[key]
            self._data.commit()
