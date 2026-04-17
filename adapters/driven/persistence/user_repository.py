from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from adapters.driven.persistence.models import UserModel
from domain.entities.user import User


class SqlAlchemyUserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def save(self, user: User) -> User:
        model = UserModel.from_entity(user)
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return model.to_entity()

    async def find_by_email(self, email: str) -> User | None:
        result = await self.session.execute(
            select(UserModel).where(UserModel.email == email)
        )
        model = result.scalars().first()
        if model is None:
            return None
        return model.to_entity()

    async def find_by_id(self, user_id: int) -> User | None:
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        model = result.scalars().first()
        if model is None:
            return None
        return model.to_entity()
