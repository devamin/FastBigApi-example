
import asyncio

from dependency_injector.wiring import Provide, inject
from sqlalchemy.orm import Session

from hrflow.database.connection.sql_connection_manager import SQLConnectionManager


def inject_db_session(func):
    def wrapper(*args, **kwargs):
        return inject_session_wrapper(func, *args, **kwargs)

    @inject
    def inject_session_wrapper(
        func,
        *args,
        sql_connection_manager: SQLConnectionManager = Provide["db_di_container.sql_connection_manager"],
        **kwargs,
    ):
        if asyncio.iscoroutinefunction(func):

            async def _async(func=func, args=args, kwargs=kwargs):
                if "session" in kwargs or any(isinstance(arg, Session) for arg in args):
                    return await func(*args, **kwargs)
                with sql_connection_manager.begin() as session:
                    kwargs.update({"session": session})
                    value = await func(*args, **kwargs)
                    session.flush()
                    session.expunge_all()
                    return value

            return _async()
        else:

            def _sync(func=func, args=args, kwargs=kwargs):
                if "session" in kwargs or any(isinstance(arg, Session) for arg in args):
                    return func(*args, **kwargs)
                with sql_connection_manager.begin() as session:
                    kwargs.update({"session": session})
                    value = func(*args, **kwargs)
                    session.flush()
                    session.expunge_all()
                    return value

            return _sync()

    return wrapper