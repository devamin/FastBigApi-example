from __future__ import annotations

import copy
import inspect
import json
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel
from sqlalchemy import Column, DateTime, Integer, func
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.inspection import inspect as sql_inspect
from sqlalchemy.orm import Session, class_mapper


def default_json_encoder(obj):
    if isinstance(obj, datetime.date):
        return obj.isoformat()
    else:
        raise TypeError("Object of type %s is not JSON serializable" % type(obj))

@as_declarative()
class BaseDBModel:
    # fields to hide in str repr
    _repr_hide = []  # type: ignore

    @classmethod
    def from_schema(cls, schema_instance):
        model_mapper = class_mapper(cls)
        _dict = schema_instance.dict()
        return cls(**{k: v for k, v in _dict.items() if k in model_mapper.attrs.keys()})

    def update_from_model(self, model_instance, accept_empty_str=False):
        insp = sql_inspect(self)
        model_columns_and_relations = insp.mapper.column_attrs.keys() + insp.mapper.relationships.keys()
        for attr in model_columns_and_relations:
            if attr in model_columns_and_relations:
                if not hasattr(model_instance, attr):
                    continue
                mi_attr_value = getattr(model_instance, attr)
                if mi_attr_value is not None and (mi_attr_value != "" or accept_empty_str):
                    setattr(self, attr, mi_attr_value)  # noqa: FKA01

    def deep_to_dict(self):
        dict_ = self.to_dict()
        insp = sql_inspect(self)
        for complex, relation in insp.mapper.relationships.items():
            if complex not in insp.unloaded:
                if relation.uselist:
                    dict_[complex] = [record.deep_to_dict() for record in getattr(self, complex)]
                elif not relation.uselist and getattr(self, complex) is not None:
                    dict_[complex] = getattr(self, complex).deep_to_dict()
        return dict_

    def to_dict(self):
        return self._asdict()

    def to_json_str(self, indent: int = 0) -> str:
        return json.dumps(self.to_dict(), indent=indent)

    def to_deep_json_str(self, indent: int = 0) -> str:
        return json.dumps(self.deep_to_dict(), indent=indent, default=default_json_encoder)

    def make_detached_copy(self, session: Session):
        session.expunge(self)
        model_copy = copy.deepcopy(self)
        session.add(self)
        return model_copy

    def _asdict(self):
        return {c.key: getattr(self, c.key) for c in sql_inspect(self).mapper.column_attrs}

    def __repr__(self):
        values = ", ".join("%s=%r" % (n, getattr(self, n)) for n in self.__table__.c.keys() if n not in self._repr_hide)
        return "%s(%s)" % (self.__class__.__name__, values)

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__


class TimedModel(BaseDBModel):
    """TimedModel is any model that we would like to track record creation and update."""

    __abstract__ = True

    created_at = Column(DateTime(), server_default=func.now())
    updated_at = Column(DateTime(), onupdate=func.now())

