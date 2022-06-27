from abc import ABC, abstractmethod
from core.schema import ORJSONModel


class AbstractRepository(ABC):
    """
    Абстрактный класс для общения с бд.
    """
    @abstractmethod
    async def create(self, item: ORJSONModel) -> ORJSONModel:
        """
        Создает запись в бд;
        :param item: объект содержаший информацию для вставки в бд;
        :return: созданный объект.
        """
