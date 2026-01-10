import os
import dotenv

from contextlib import asynccontextmanager
from .dependencies import get_session
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio.engine import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession
from .schema import Product
from .dto import ProductCreateDto
from sqlmodel import select, SQLModel

dotenv.load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("'DATABASE_URL' environment variable is not set.")


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application is starting up")
    engine = create_async_engine(
        DATABASE_URL if DATABASE_URL is not None else "",
        future=True,
    )
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    async_sessionmaker = sessionmaker(
        bind=engine,
        expire_on_commit=False,
        autoflush=True,
        class_=AsyncSession,
    )
    app.state.db_engine = engine
    app.state.async_sessionmaker = async_sessionmaker
    try:
        yield
    finally:
        await engine.dispose()
    print("Tearing down application")


app = FastAPI(lifespan=lifespan)


@app.get("/products")
async def read_products(
    session: AsyncSession = Depends(get_session), response_model=list[Product]
):
    products = await session.exec(select(Product))
    return products.fetchall()


@app.post("/products", response_model=Product)
async def create_product(
    product: ProductCreateDto, session: AsyncSession = Depends(get_session)
):
    new_product = Product(name=product.name)
    session.add(new_product)
    await session.commit()
    await session.refresh(new_product)
    return new_product
