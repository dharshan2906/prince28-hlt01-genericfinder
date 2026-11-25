"""HTTP API usage analytics."""

from datetime import UTC, datetime, timedelta

from fastapi import APIRouter, Query
from sqlalchemy import case, func, select

from genericfinder.api.deps import SessionDep
from genericfinder.db.models import ApiRequest

router = APIRouter(prefix="/analytics", tags=["analytics"])


def since_time(days: int) -> datetime:
    """Return the start of the requested reporting window."""
    return datetime.now(UTC) - timedelta(days=days)


@router.get("/overview")
async def overview(
    session: SessionDep,
    days: int = Query(default=7, ge=1, le=90),
) -> dict:
    """Total requests, successes, failures and success rate."""
    since = since_time(days)

    statement = select(
        func.count(ApiRequest.id).label("total"),
        func.sum(case((ApiRequest.status_code < 400, 1), else_=0)).label("success"),
        func.sum(case((ApiRequest.status_code >= 400, 1), else_=0)).label("errors"),
    ).where(ApiRequest.created_at >= since)

    row = (await session.execute(statement)).one()

    total = row.total or 0
    success = row.success or 0
    errors = row.errors or 0

    return {
        "period_days": days,
        "total_requests": total,
        "successful_requests": success,
        "failed_requests": errors,
        "success_rate": round(success / total * 100, 2) if total else 0,
    }


@router.get("/endpoints")
async def endpoints(
    session: SessionDep,
    days: int = Query(default=7, ge=1, le=90),
) -> dict:
    """Request counts grouped by HTTP method and endpoint."""
    statement = (
        select(
            ApiRequest.method,
            ApiRequest.path,
            func.count(ApiRequest.id).label("requests"),
        )
        .where(ApiRequest.created_at >= since_time(days))
        .group_by(ApiRequest.method, ApiRequest.path)
        .order_by(func.count(ApiRequest.id).desc())
    )

    rows = (await session.execute(statement)).all()

    return {
        "period_days": days,
        "endpoints": [
            {"method": row.method, "path": row.path, "requests": row.requests} for row in rows
        ],
    }


@router.get("/latency")
async def latency(
    session: SessionDep,
    days: int = Query(default=7, ge=1, le=90),
) -> dict:
    """Average, minimum and maximum request latency."""
    statement = select(
        func.count(ApiRequest.id).label("total"),
        func.avg(ApiRequest.latency_ms).label("average"),
        func.min(ApiRequest.latency_ms).label("minimum"),
        func.max(ApiRequest.latency_ms).label("maximum"),
    ).where(ApiRequest.created_at >= since_time(days))

    row = (await session.execute(statement)).one()

    return {
        "period_days": days,
        "requests": row.total or 0,
        "average_ms": round(float(row.average), 2) if row.average is not None else 0,
        "minimum_ms": row.minimum or 0,
        "maximum_ms": row.maximum or 0,
    }


@router.get("/errors")
async def errors(
    session: SessionDep,
    days: int = Query(default=7, ge=1, le=90),
) -> dict:
    """HTTP error counts grouped by status code."""
    statement = (
        select(
            ApiRequest.status_code,
            func.count(ApiRequest.id).label("count"),
        )
        .where(
            ApiRequest.created_at >= since_time(days),
            ApiRequest.status_code >= 400,
        )
        .group_by(ApiRequest.status_code)
        .order_by(ApiRequest.status_code)
    )

    rows = (await session.execute(statement)).all()

    return {
        "period_days": days,
        "errors": [{"status_code": row.status_code, "count": row.count} for row in rows],
    }


@router.get("/daily")
async def daily(
    session: SessionDep,
    days: int = Query(default=7, ge=1, le=90),
) -> dict:
    """Daily request volume and error counts."""
    day = func.date_trunc("day", ApiRequest.created_at).label("day")

    statement = (
        select(
            day,
            func.count(ApiRequest.id).label("requests"),
            func.sum(case((ApiRequest.status_code >= 400, 1), else_=0)).label("errors"),
        )
        .where(ApiRequest.created_at >= since_time(days))
        .group_by(day)
        .order_by(day)
    )

    rows = (await session.execute(statement)).all()

    return {
        "period_days": days,
        "daily": [
            {
                "date": row.day.date().isoformat(),
                "requests": row.requests,
                "errors": row.errors or 0,
            }
            for row in rows
        ],
    }
