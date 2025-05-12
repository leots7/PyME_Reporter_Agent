from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db.session import get_async_session
from backend.app.schemas.user import User, UserCreate, UserUpdate
from backend.app.crud import user as user_crud

router = APIRouter()

@router.post("/users/", response_model=User, status_code=201)
async def create_user(user_in: UserCreate, db: AsyncSession = Depends(get_async_session)):
    db_user = await user_crud.get_by_email(db, email=user_in.email)
    if db_user:
        raise HTTPException(status_code=400, detail="El usuario con este correo electrónico ya existe")
    return await user_crud.create(db=db, user_in=user_in)

@router.get("/users/{user_id}", response_model=User)
async def read_user(user_id: int, db: AsyncSession = Depends(get_async_session)):
    db_user = await user_crud.get(db, id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_user

@router.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, user_in: UserUpdate, db: AsyncSession = Depends(get_async_session)):
    db_user = await user_crud.get(db, id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    updated_user = await user_crud.update(db=db, db_user=db_user, user_in=user_in)
    return updated_user

@router.delete("/users/{user_id}", response_model=dict)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_async_session)):
    db_user = await user_crud.get(db, id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    await db.delete(db_user)
    await db.commit()
    return {"message": "Usuario eliminado exitosamente"}