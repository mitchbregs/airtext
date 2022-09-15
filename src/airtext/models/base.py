import json

from sqlalchemy import inspect
from sqlalchemy.ext.declarative import as_declarative


@as_declarative()
class Base:
    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

    def to_json(self):
        return json.dumps(self.to_dict(), default=str)


metadata = Base.metadata
