from abc import ABC, abstractmethod

from core.schema import ORJSONModel


class AbstractRepository(ABC):
    """
    Абстрактный класс для общения с бд.
    """
    @abstractmethod
    async def create(self, item: ORJSONModel) -> ORJSONModel or None:
        """
        Создает запись в бд;
        :param item: объект содержаший информацию для вставки в бд;
        :return: созданный объект.
        """


class AbstractQueuePublisher(ABC):
    """
    Абстрактный класс для работы с очередью.
    """
    @abstractmethod
    def publish(self, message: str) -> None:
        """
        Метод для отправки сообщения в очередь;
        :param message: сообщение в формате json-строки;
        :return: None.
        """
