from abc import ABC, abstractmethod
from domain.models.actor import Actor

class ActorRepository(ABC):
    @abstractmethod
    def save(self, actor: Actor) -> None:
        pass
