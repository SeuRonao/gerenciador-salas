import pytest

from app.container import criar_container_memória


@pytest.fixture
def container_memoria():
    """Fornece um container em memória novo para cada teste."""
    return criar_container_memória()
