from fastapi import Request


async def get_session(request: Request):
    async_sessionmaker = request.app.state.async_sessionmaker
    async with async_sessionmaker() as session:
        yield session
