import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.database import get_db


@pytest.fixture
async def client():
    mock_session = AsyncMock()

    async def override_get_db():
        yield mock_session

    app.dependency_overrides[get_db] = override_get_db

    # AsyncEngine.connect is read-only, so patch the whole engine object
    mock_engine = MagicMock()
    mock_engine.connect.return_value = AsyncMock()
    mock_engine.dispose = AsyncMock()

    with patch("app.main.engine", mock_engine):
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as ac:
            yield ac, mock_session

    app.dependency_overrides.clear()
