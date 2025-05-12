from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from backend.app.models.user import User
from backend.app.schemas.user import UserCreate, UserUpdate

async def get(db: AsyncSession, id: int) -> User | None:
    result = await db.execute(select(User).where(User.id == id))
    return result.scalar_one_or_none()

async def get_by_email(db: AsyncSession, email: str) -> User | None:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()

async def create(db: AsyncSession, user_in: UserCreate) -> User:
    db_user = User(email=user_in.email, hashed_password="contraseña_temporal") # TODO: Hash password
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def update(db: AsyncSession, db_user: User, user_in: UserUpdate) -> User:
    if user_in.full_name is not None:
        db_user.full_name = user_in.full_name
    if user_in.password is not None:
        db_user.hashed_password = "nueva_contraseña_temporal"  # TODO: Hash nueva contraseña
    if user_in.is_active is not None:
        db_user.is_active = user_in.is_active
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user