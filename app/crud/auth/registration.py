from ...dependencies import get_db
from ...shecemas.auth_shecema import *
from sqlalchemy import select
from ...models.user import User
from ...utitilities import generate_salt


async def UserExists(username: str) -> bool:
    async for session in get_db():
        result = await session.execute(select(User).where(User.name == username))

        if result.scalar() == 0:
            return False
        return True

async def TryCreateNewUser(info: RegistrateModel) -> bool:
    async for session in get_db():
        if not UserExists(info.username):
            return False
        
        salt: str = generate_salt()
        hashed_password = hash(info.password + salt)

        user: User = User(name=info.username, surname=info.surename, hashed_password=hashed_password, salt=salt)

        session.add(user)
        await session.commit()
        return True

async def TryLoginUser(info: LoginModel) -> bool:
    async for session in get_db():
        result = await session.execute(select(User).where(User.name == info.username))

        potential_user: User = result.scalar()

        if potential_user is None:
            return False
        
        return hash(info.password + potential_user.salt) == potential_user.hashed_password()