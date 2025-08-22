from .settings_model import Settings


class SettingsRepository:
    def __init__(self, session):
        self.session = session

    def create_one(self, settings):
        self.session.add(settings)
        self.session.flush()
        self.session.refresh(settings)
        return settings

    def get_one(self, user_id):
        return self.session.query(Settings).filter(Settings.user_id == user_id).first()

    def get_all(self):
        return self.session.query(Settings).all()

    def update_one(self, settings):
        return self.session.merge(settings)

    def delete_one(self, settings):
        self.session.delete(settings)
        self.session.flush()
        return settings

    def delete_all(self):
        deleted_count = self.session.query(Settings).delete()
        self.session.flush()
        return deleted_count

    def execute_custom_query(self, query):
        result = self.session.execute(query)
        self.session.flush()
        return result
