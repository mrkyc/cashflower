from typing import Iterable
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import platform
import sqlite3
import os


class Base(DeclarativeBase):
    pass


class Database:
    def __init__(self, id: str):
        self.db_path = os.path.join("databases", id, "cashflower.db")
        self.path_exists = os.path.exists(self.db_path)
        self.db_url = f"sqlite:///{self.db_path}"
        self.engine = create_engine(self.db_url)
        self.SessionMaker = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )
        self._add_sqlite_pragma()

    def _add_sqlite_pragma(self):
        if "sqlite" in str(self.engine.url):

            @event.listens_for(self.engine, "connect")
            def set_sqlite_pragma(dbapi_connection, connection_record):
                cursor = dbapi_connection.cursor()
                cursor.execute("PRAGMA foreign_keys=ON;")
                cursor.close()

    @staticmethod
    def _get_platform_specific_extension_path(extension_name, base_path="."):
        """
        Determines the correct path for a shared library based on the OS.
        Example: _get_platform_specific_extension_path("xirr")
        -> returns "./xirr.dll" on Windows
        -> returns "./xirr.dylib" on MacOS
        -> returns "./xirr.so" on Linux
        """
        system = platform.system()
        if system == "Windows":
            return os.path.join(base_path, f"{extension_name}.dll")
        elif system == "Darwin":
            return os.path.join(base_path, f"{extension_name}.dylib")
        else:
            # Fallback for Linux and other Unix-like systems
            return os.path.join(base_path, f"{extension_name}.so")

    def load_extensions(self, extension_names: Iterable[str]):
        if "sqlite" in str(self.engine.url):
            extension_paths = []
            for extension_name in extension_names:
                if not isinstance(extension_name, str):
                    raise TypeError(
                        f"Expected a string for extension name, got {type(extension_name)}"
                    )
                if not extension_name:
                    raise ValueError("Extension name cannot be an empty string.")

                # Get the platform-specific path for the extension
                # This assumes the extensions are located in a directory named 'extensions'
                extension_path = Database._get_platform_specific_extension_path(
                    extension_name,
                    base_path=os.path.join(os.path.dirname(__file__), "extensions"),
                )

                if not os.path.exists(extension_path):
                    raise FileNotFoundError(
                        f"The compiled extension '{extension_path}' was not found. "
                        f"Please run 'make' to compile it for your system ({platform.system()})."
                    )
                if not os.path.isfile(extension_path):
                    raise IsADirectoryError(
                        f"The path '{extension_path}' is not a file. "
                        f"Please ensure it points to the compiled extension."
                    )
                if not os.access(extension_path, os.R_OK):
                    raise PermissionError(
                        f"The extension '{extension_path}' is not readable. "
                        f"Please check the file permissions."
                    )

                extension_paths.append(extension_path)

            # Open a raw DB-API connection to load the extension
            with self.engine.connect() as conn:
                dbapi_connection = conn.connection
                dbapi_connection.enable_load_extension(True)
                try:
                    for extension_path in extension_paths:
                        dbapi_connection.load_extension(extension_path)
                except sqlite3.OperationalError as e:
                    raise f"Error loading extension: {e}"
                finally:
                    dbapi_connection.enable_load_extension(False)

    def get_db_session(self):
        session = self.SessionMaker()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def create_database(self):
        if not self.path_exists:
            os.makedirs(os.path.dirname(self.db_path))
            self.path_exists = True

        Base.metadata.create_all(bind=self.engine)

    def drop_database(self):
        Base.metadata.drop_all(bind=self.engine)

    def recreate_database(self):
        self.drop_database()
        self.create_database()
