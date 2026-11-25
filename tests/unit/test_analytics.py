"""Tests for HTTP API usage analytics."""

from datetime import UTC
from types import SimpleNamespace


class FakeResult:
    def __init__(self, row=None, rows=None):
        self.row = row
        self.rows = rows or []

    def one(self):
        return self.row

    def all(self):
        return self.rows


class FakeSession:
    def __init__(self, factory):
        self.factory = factory

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        return None

    def add(self, record):
        self.factory.records.append(record)

    async def commit(self):
        pass

    async def execute(self, statement):
        return self.factory.result


class FakeSessionFactory:
    def __init__(self, result):
        self.result = result
        self.records = []

    def __call__(self):
        return FakeSession(self)


def setup_analytics(client, result):
    factory = FakeSessionFactory(result)
    client.app.state.sessionmaker = factory
    return factory


def test_analytics_overview(client):
    setup_analytics(
        client,
        FakeResult(SimpleNamespace(total=100, success=95, errors=5)),
    )

    response = client.get("/v1/analytics/overview")

    assert response.status_code == 200
    assert response.json() == {
        "period_days": 7,
        "total_requests": 100,
        "successful_requests": 95,
        "failed_requests": 5,
        "success_rate": 95.0,
    }


def test_analytics_endpoints(client):
    setup_analytics(
        client,
        FakeResult(
            rows=[
                SimpleNamespace(
                    method="GET",
                    path="/v1/documents",
                    requests=50,
                ),
                SimpleNamespace(
                    method="POST",
                    path="/v1/chat",
                    requests=20,
                ),
            ]
        ),
    )

    response = client.get("/v1/analytics/endpoints")

    assert response.status_code == 200
    assert response.json()["endpoints"] == [
        {"method": "GET", "path": "/v1/documents", "requests": 50},
        {"method": "POST", "path": "/v1/chat", "requests": 20},
    ]


def test_analytics_latency(client):
    setup_analytics(
        client,
        FakeResult(
            SimpleNamespace(
                total=100,
                average=125.456,
                minimum=10,
                maximum=800,
            )
        ),
    )

    response = client.get("/v1/analytics/latency")

    assert response.status_code == 200
    assert response.json()["requests"] == 100
    assert response.json()["average_ms"] == 125.46
    assert response.json()["minimum_ms"] == 10
    assert response.json()["maximum_ms"] == 800


def test_analytics_errors(client):
    setup_analytics(
        client,
        FakeResult(
            rows=[
                SimpleNamespace(status_code=404, count=3),
                SimpleNamespace(status_code=500, count=2),
            ]
        ),
    )

    response = client.get("/v1/analytics/errors")

    assert response.status_code == 200
    assert response.json()["errors"] == [
        {"status_code": 404, "count": 3},
        {"status_code": 500, "count": 2},
    ]


def test_analytics_daily(client):
    from datetime import datetime

    setup_analytics(
        client,
        FakeResult(
            rows=[
                SimpleNamespace(
                    day=datetime(2026, 11, 26, tzinfo=UTC),
                    requests=50,
                    errors=2,
                )
            ]
        ),
    )

    response = client.get("/v1/analytics/daily")

    assert response.status_code == 200
    assert response.json()["daily"] == [{"date": "2026-11-26", "requests": 50, "errors": 2}]


def test_analytics_empty_overview(client):
    setup_analytics(
        client,
        FakeResult(SimpleNamespace(total=0, success=0, errors=0)),
    )

    response = client.get("/v1/analytics/overview")

    assert response.status_code == 200
    assert response.json()["total_requests"] == 0
    assert response.json()["success_rate"] == 0


def test_analytics_rejects_invalid_days(client):
    response = client.get("/v1/analytics/overview?days=100")

    assert response.status_code == 422


def test_middleware_records_api_request(client):
    factory = setup_analytics(client, FakeResult())

    response = client.get(
        "/health",
        headers={"X-Request-ID": "analytics-test-123"},
    )

    assert response.status_code == 200
    assert len(factory.records) == 1

    record = factory.records[0]
    assert record.request_id == "analytics-test-123"
    assert record.method == "GET"
    assert record.path == "/health"
    assert record.status_code == 200
    assert record.latency_ms >= 0
