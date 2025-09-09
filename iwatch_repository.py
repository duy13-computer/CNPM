from abc import ABC, abstractmethod
from typing import List, Optional
from .watch import Watch
class IWatchRepository(ABC):
    @abstractmethod
    def add(self, watch: Watch) -> Watch:
        pass

    @abstractmethod
    def get_by_id(self, watch_id: int) -> Optional[Watch]:
        pass

    @abstractmethod
    def list(self) -> List[Watch]:
        pass

    #@abstractmethod
    #def update(self, watch: Watch) -> Course:
    #    pass

    @abstractmethod
    def delete(self, watch_id: int) -> None:
        pass 