from .user_model import User


class UserRepository:
    def __init__(self, session):
        self.session = session

    def create_one(self, user):
        self.session.add(user)
        self.session.flush()
        self.session.refresh(user)
        return user

    def get_one(self, id):
        return self.session.query(User).filter(User.id == id).first()

    def get_one_by_session_id(self, session_id):
        return self.session.query(User).filter(User.session_id == session_id).first()

    def get_all(self):
        return self.session.query(User).all()

    def update_one(self, user):
        return self.session.merge(user)

    def delete_one(self, user):
        self.session.delete(user)
        self.session.flush()
        return user

    def delete_all(self):
        deleted_count = self.session.query(User).delete()
        self.session.flush()
        return deleted_count

    def execute_custom_query(self, query):
        result = self.session.execute(query)
        self.session.flush()
        return result
