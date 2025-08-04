
from concurrent.futures import ThreadPoolExecutor
from typing import List
from domain.models.movie import Movie
from domain.interfaces.use_case_interface import UseCaseInterface

class CompositeSaveMovieWithActorsUseCase(UseCaseInterface):
    """
    Caso de uso compuesto que orquesta la ejecución de múltiples casos de uso de guardado
    de forma concurrente.
    """

    def __init__(self, use_cases: List[UseCaseInterface]):
        """
        Constructor del caso de uso compuesto.

        Args:
            use_cases (List[UseCaseInterface]): Una lista de casos de uso que implementan
                                                la UseCaseInterface.
        """
        self.use_cases = use_cases
        # Limita el número de hilos para no saturar recursos. 2 en este caso.
        self.max_workers = len(use_cases)

    def execute(self, movie: Movie) -> None:
        """
        Ejecuta todos los casos de uso de la lista en paralelo usando un pool de hilos.

        Args:
            movie (Movie): Objeto Movie que contiene la información a persistir.
        """
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # executor.map aplica la función execute a cada caso de uso en la lista
            # de forma concurrente, pasando el mismo objeto 'movie' a cada uno.
            list(executor.map(lambda uc: uc.execute(movie), self.use_cases))