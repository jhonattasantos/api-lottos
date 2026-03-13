async def test_health_returns_200(client):
    ac, _ = client
    response = await ac.get("/health")
    assert response.status_code == 200


async def test_health_returns_ok(client):
    ac, _ = client
    response = await ac.get("/health")
    assert response.json() == {"status": "ok"}


async def test_health_executes_db_query(client):
    ac, mock_session = client
    await ac.get("/health")
    mock_session.execute.assert_called_once()
