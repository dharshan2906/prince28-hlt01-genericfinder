"""HTTP API usage analytics."""

from datetime import UTC, datetime, timedelta

from fastapi import APIRouter, Query
from sqlalchemy import case, func, select

from genericfinder.api.deps import SessionDep
from genericfinder.db.models import ApiRequest, LlmCall

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


@router.get("/llm/overview")
async def llm_overview(
    session: SessionDep,
    days: int = Query(default=7, ge=1, le=90),
) -> dict:
    """Overall LLM usage, reliability, latency and estimated cost."""
    statement = select(
        func.count(LlmCall.id).label("total"),
        func.sum(case((LlmCall.status == "ok", 1), else_=0)).label("success"),
        func.sum(case((LlmCall.status == "error", 1), else_=0)).label("errors"),
        func.sum(LlmCall.tokens_in).label("tokens_in"),
        func.sum(LlmCall.tokens_out).label("tokens_out"),
        func.sum(LlmCall.cost_inr).label("cost_inr"),
        func.avg(LlmCall.latency_ms).label("average_latency"),
        func.sum(case((LlmCall.fallback_used.is_(True), 1), else_=0)).label("fallbacks"),
    ).where(LlmCall.created_at >= since_time(days))

    row = (await session.execute(statement)).one()
    total = row.total or 0
    success = row.success or 0

    return {
        "period_days": days,
        "total_calls": total,
        "successful_calls": success,
        "failed_calls": row.errors or 0,
        "success_rate": round(success / total * 100, 2) if total else 0,
        "tokens_in": int(row.tokens_in or 0),
        "tokens_out": int(row.tokens_out or 0),
        "estimated_cost_inr": round(float(row.cost_inr or 0), 4),
        "average_latency_ms": round(float(row.average_latency or 0), 2),
        "fallback_calls": row.fallbacks or 0,
    }


@router.get("/llm/providers")
async def llm_providers(
    session: SessionDep,
    days: int = Query(default=7, ge=1, le=90),
) -> dict:
    """Compare LLM provider usage, reliability and cost."""
    statement = (
        select(
            LlmCall.provider,
            LlmCall.model,
            func.count(LlmCall.id).label("calls"),
            func.sum(case((LlmCall.status == "error", 1), else_=0)).label("errors"),
            func.sum(LlmCall.tokens_in).label("tokens_in"),
            func.sum(LlmCall.tokens_out).label("tokens_out"),
            func.sum(LlmCall.cost_inr).label("cost_inr"),
            func.avg(LlmCall.latency_ms).label("average_latency"),
        )
        .where(LlmCall.created_at >= since_time(days))
        .group_by(LlmCall.provider, LlmCall.model)
        .order_by(func.count(LlmCall.id).desc())
    )

    rows = (await session.execute(statement)).all()

    return {
        "period_days": days,
        "providers": [
            {
                "provider": row.provider,
                "model": row.model,
                "calls": row.calls,
                "errors": row.errors or 0,
                "tokens_in": int(row.tokens_in or 0),
                "tokens_out": int(row.tokens_out or 0),
                "estimated_cost_inr": round(float(row.cost_inr or 0), 4),
                "average_latency_ms": round(float(row.average_latency or 0), 2),
            }
            for row in rows
        ],
    }


@router.get("/llm/usage")
async def llm_usage(
    session: SessionDep,
    days: int = Query(default=7, ge=1, le=90),
) -> dict:
    """Daily LLM calls, token usage and estimated cost in India time."""
    local_day = func.date_trunc("day", func.timezone("Asia/Kolkata", LlmCall.created_at)).label(
        "day"
    )

    statement = (
        select(
            local_day,
            func.count(LlmCall.id).label("calls"),
            func.sum(LlmCall.tokens_in).label("tokens_in"),
            func.sum(LlmCall.tokens_out).label("tokens_out"),
            func.sum(LlmCall.cost_inr).label("cost_inr"),
        )
        .where(LlmCall.created_at >= since_time(days))
        .group_by(local_day)
        .order_by(local_day)
    )

    rows = (await session.execute(statement)).all()

    return {
        "period_days": days,
        "daily": [
            {
                "date": row.day.date().isoformat(),
                "calls": row.calls,
                "tokens_in": int(row.tokens_in or 0),
                "tokens_out": int(row.tokens_out or 0),
                "estimated_cost_inr": round(float(row.cost_inr or 0), 4),
            }
            for row in rows
        ],
    }


@router.get("/llm/failures")
async def llm_failures(
    session: SessionDep,
    days: int = Query(default=7, ge=1, le=90),
    limit: int = Query(default=20, ge=1, le=100),
) -> dict:
    """Show the most recent failed LLM calls."""
    statement = (
        select(
            LlmCall.created_at,
            LlmCall.provider,
            LlmCall.model,
            LlmCall.purpose,
            LlmCall.error,
        )
        .where(
            LlmCall.created_at >= since_time(days),
            LlmCall.status == "error",
        )
        .order_by(LlmCall.created_at.desc())
        .limit(limit)
    )

    rows = (await session.execute(statement)).all()

    return {
        "period_days": days,
        "failures": [
            {
                "timestamp": row.created_at.isoformat(),
                "provider": row.provider,
                "model": row.model,
                "purpose": row.purpose,
                "error": row.error[:200] if row.error else "Unknown error",
            }
            for row in rows
        ],
    }
