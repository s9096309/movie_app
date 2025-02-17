from abc import ABC, abstractmethod


class IStorage(ABC):
    @abstractmethod
    def list_movies(self):
        pass

    @abstractmethod
    def add_movie(self, title, rating, year, poster_url):
        pass

    @abstractmethod
    def delete_movie(self, title):
        pass

    @abstractmethod
    def update_movie(self, title, rating, poster_url):
        pass