import asyncio

from sqlalchemy import func, select

from genericfinder.config import get_settings
from genericfinder.db.models import LlmCall
from genericfinder.db.session import make_engine, make_sessionmaker


async def main():
    settings = get_settings()
    engine = make_engine(settings)
    SessionLocal = make_sessionmaker(engine)

    try:
        async with SessionLocal() as session:
            # 1. Overall usage
            total = await session.scalar(select(func.count()).select_from(LlmCall)) or 0

            failed = (
                await session.scalar(
                    select(func.count()).select_from(LlmCall).where(LlmCall.status == "error")
                )
                or 0
            )

            tokens_in = (
                await session.scalar(select(func.coalesce(func.sum(LlmCall.tokens_in), 0))) or 0
            )

            tokens_out = (
                await session.scalar(select(func.coalesce(func.sum(LlmCall.tokens_out), 0))) or 0
            )

            total_cost = (
                await session.scalar(select(func.coalesce(func.sum(LlmCall.cost_inr), 0))) or 0
            )

            print("\n========== LLM USAGE REPORT ==========")
            print(f"Total requests : {total}")
            print(f"Successful     : {total - failed}")
            print(f"Failed         : {failed}")
            print(f"Input tokens   : {tokens_in}")
            print(f"Output tokens  : {tokens_out}")
            print(f"Total cost     : ₹{float(total_cost):.6f}")

            # 2. Provider breakdown
            print("\n========== PROVIDER BREAKDOWN ==========")

            providers = await session.execute(
                select(
                    LlmCall.provider,
                    func.count(LlmCall.id),
                    func.sum(LlmCall.tokens_in),
                    func.sum(LlmCall.tokens_out),
                    func.sum(LlmCall.cost_inr),
                )
                .group_by(LlmCall.provider)
                .order_by(LlmCall.provider)
            )

            for provider, count, input_tokens, output_tokens, cost in providers:
                print(f"\nProvider      : {provider}")
                print(f"Requests      : {count}")
                print(f"Input tokens  : {input_tokens or 0}")
                print(f"Output tokens : {output_tokens or 0}")
                print(f"Total cost    : ₹{float(cost or 0):.6f}")

            # 3. Daily usage history
            print("\n========== DAILY USAGE HISTORY ==========")

            history = await session.execute(
                select(
                    func.date(LlmCall.created_at),
                    func.count(LlmCall.id),
                    func.sum(LlmCall.tokens_in),
                    func.sum(LlmCall.tokens_out),
                    func.sum(LlmCall.cost_inr),
                )
                .group_by(func.date(LlmCall.created_at))
                .order_by(func.date(LlmCall.created_at).desc())
                .limit(30)
            )

            for day, requests, input_tokens, output_tokens, cost in history:
                print(
                    f"{day} | Requests: {requests} | "
                    f"In: {input_tokens or 0} | "
                    f"Out: {output_tokens or 0} | "
                    f"Cost: ₹{float(cost or 0):.6f}"
                )

            # 4. Recent request history
            print("\n========== RECENT REQUEST HISTORY ==========")

            recent = await session.execute(
                select(
                    LlmCall.created_at,
                    LlmCall.provider,
                    LlmCall.model,
                    LlmCall.purpose,
                    LlmCall.status,
                    LlmCall.tokens_in,
                    LlmCall.tokens_out,
                    LlmCall.cost_inr,
                    LlmCall.fallback_used,
                )
                .order_by(LlmCall.created_at.desc())
                .limit(20)
            )

            for row in recent:
                (
                    created_at,
                    provider,
                    model,
                    purpose,
                    status,
                    input_tokens,
                    output_tokens,
                    cost,
                    fallback_used,
                ) = row

                print(f"\nTime: {created_at} | Provider: {provider} | Model: {model}")
                print(f"Purpose: {purpose} | Status: {status} | Fallback: {fallback_used}")
                print(
                    f"Tokens: {input_tokens or 0} in / "
                    f"{output_tokens or 0} out | "
                    f"Cost: ₹{float(cost or 0):.6f}"
                )

    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
