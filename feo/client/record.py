from datetime import datetime
from typing import List, Optional

import pandas as pd

from feo.client import api
from feo.client.api import schemas


class Record(schemas.RecordBase):
    pass


class RecordCollection(pd.DataFrame):
    """An RecordCollection is an extention of a Pandas DataFrame.

    It can be used in precisely the same way as a Pandas DataFrame
    but has a few extra useful constructors.

    Args:
        _scope (schemas.CollectionScope | None): params for generating api query for pagination
        _page (int | None): if generated from an API query, the current page of the query.
    """

    _scope: Optional[schemas.CollectionScope] = None
    _page: Optional[int] = None

    @property
    def _constructor(self):
        return RecordCollection

    @property
    def _constructor_sliced(self):
        return RecordCollectionRow

    @classmethod
    def search(
        cls,
        node_id: list[str] | None = None,
        public: bool = True,
        valid_timestamp_start: datetime | None = None,
        valid_timestamp_end: datetime | None = None,
        provenance_slug: list[str] | None = None,
        datum_type: list[str] | None = None,
        datum_detail: list[str] | None = None,
        node_type: list[str] | None = None,
    ):
        """Instantiate an RecordCollection from a parent node.

        Args:
            node_id (str): the id of the parent node to retieve records for.
            sector (str): the name of the sector to retireve records for.

        Returns:
            RecordCollection: A pandas-dataframe extension for FEO records.
        """
        records = api.records.get(
            node_id=node_id,
            public=public,
            valid_timestamp_start=valid_timestamp_start,
            valid_timestamp_end=valid_timestamp_end,
            provenance_slug=provenance_slug,
            datum_type=datum_type,
            datum_detail=datum_detail,
            node_type=node_type,
        )

        obj = cls.from_feo_records(records)
        obj._scope = schemas.CollectionScope(node_id=node_id)
        obj._page = 0
        return obj

    @classmethod
    def from_feo_records(cls, records: List[Record]):
        """Instiate an RecordCollection from a list of Records."""
        # pd.DataFrame.from_records
        return cls.from_records([record.model_dump() for record in records])

    def next_page(self):
        """Paginate through records. The Record collection must have a `_scope`.

        Returns the next page of records and concatenates them in-place to the current collection.
        """
        if not self._scope:
            raise ValueError("Cant iterate an unscoped RecordCollection")
        new_collection = self.__class__.from_feo_records(
            api.records.get(parent_node_id=self._scope.parent_node_id, page=self._page + 1)
        )
        self._page += 1

        self.__dict__.update(pd.concat([self, new_collection], ignore_index=True).__dict__)
        return len(new_collection)

    def to_feo_records(self):
        """Instantiate a list of Records from an RecordCollection."""
        return [Record(**row) for idx, row in self.iterrows()]


class RecordCollectionRow(pd.Series):
    @property
    def _constructor(self):
        return RecordCollectionRow

    @property
    def _constructor_expanddim(self):
        return RecordCollection

    def to_records(self):
        return Record(
            **self.to_dict(),
        )