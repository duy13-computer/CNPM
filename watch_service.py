
from typing import List, Optional
from domain.models.watch import Watch
from domain.models.iwatch_repository import IWatchRepository

class WatchService:
    def __init__(self, repository: IWatchRepository):
        self.repository = repository

    def create_watch(self, name: str, brand: str, price: float, description: str) -> Watch:
        watch = Watch(id=None, name=name, brand=brand, price=price, description=description)
        return self.repository.add(watch)

    def get_watch(self, watch_id: int) -> Optional[Watch]:
        return self.repository.get_by_id(watch_id)

    def list_watches(self) -> List[Watch]:
        return self.repository.list()

    def update_watch(self, watch_id: int, name: str, brand: str, price: float, description: str) -> Watch:
        watch = Watch(id=watch_id, name=name, brand=brand, price=price, description=description)
        return self.repository.update(watch)

    def delete_watch(self, watch_id: int) -> None:
        self.repository.delete(watch_id)

    