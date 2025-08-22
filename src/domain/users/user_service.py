from .user_model import User
from .user_repository import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def create_one(self, session_id):
        user = User(session_id=session_id)
        return self.user_repository.create_one(user=user)

    def upsert_one(self, session_id: str):
        user = self.get_one_by_session_id(session_id=session_id)
        if user:
            return user
        else:
            return self.create_one(session_id=session_id)

    def get_one(self, id):
        return self.user_repository.get_one(id=id)

    def get_one_by_session_id(self, session_id) -> User:
        return self.user_repository.get_one_by_session_id(session_id=session_id)

    def get_all(self):
        return self.user_repository.get_all()

    def delete_one(self, id):
        user = self.get_one(id=id)
        if user is None:
            return None
        else:
            return self.user_repository.delete_one(user=user)

    def delete_all(self):
        return self.user_repository.delete_all()
