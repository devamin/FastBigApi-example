from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from contextlib import contextmanager
from typing import Generator, Optional

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


class TransactionBase(ABC):
    @abstractmethod
    def get_new_session(self) -> Session:
        raise NotImplementedError

    @contextmanager
    def begin(self) -> Generator[Session, None, None]:
        sql_session: Optional[Session] = None
        try:
            sql_session = self.get_new_session()
            yield sql_session
            sql_session.commit()
        except SQLAlchemyError as sqlalchemy_error:
            logger.error("Rolling back SQL session due to error.", exc_info=True)
            logger.error(sqlalchemy_error)
            try:
                if sql_session is not None:
                    sql_session.rollback()
            except Exception:
                logger.error("Failed to rollback a transaction!", exc_info=True)
            # Propagate to caller, as it must be aware of it too.
            raise
        finally:
            if sql_session is not None:
                sql_session.close()
