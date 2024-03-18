import datetime
from typing import List

from tz.client.api.base import BaseAPI
from tz.client.api.schemas import Record, RecordsResponse


class RecordsAPI(BaseAPI):
    def get(
        self,
        node_id: list[str] | str | None = None,
        public: bool = True,
        timestamp: datetime.datetime | str | None = None,
        valid_timestamp_start: datetime.datetime | str | None = None,
        valid_timestamp_end: datetime.datetime | str | None = None,
        provenance_slug: list[str] | str | None = None,
        technology: str | None = None,
        datum_type: list[str] | str | None = None,
        datum_detail: list[str] | str | None = None,
        node_type: list[str] | str | None = None,
        value: float | None = None,
        unit: list[str] | str | None = None,
        properties: dict | None = None,
        limit: int | None = None,
        page: int | None = None,
    ) -> List[Record]:
        params = dict(
            node_id=node_id,
            public=public,
            timestamp=timestamp,
            valid_timestamp_start=valid_timestamp_start,
            valid_timestamp_end=valid_timestamp_end,
            provenance_slug=provenance_slug,
            technology=technology,
            datum_type=datum_type,
            datum_detail=datum_detail,
            node_type=node_type,
            value=value,
            unit=unit,
            properties=properties,
            limit=limit,
            page=page,
        )

        resp = self.client.get("/records", params=params)
        resp.raise_for_status()

        return RecordsResponse(**resp.json()).records

    def post_csv(self, csv_path: str, publisher_slug: str, source_slug: str) -> dict:
        """
        POST a CSV file of records to the records API.
        The CSV file must have a header row with the following columns:

        - "public": bool
        - "node_id": str, optional
        - "source_node_id": str, optional
        - "target_node_id": str, optional
        - "timestamp": datetime
        - "valid_timestamp_start": datetime
        - "valid_timestamp_end": datetime
        - "datum_type": str
        - "datum_detail": str
        - "value": float
        - "unit": str
        - "properties": dict, optional
        - "technology_slug": dict, optional

        Args:
            csv_path (str): The path to the CSV file.
            publisher_slug (str): The slug of the publisher.
            source_slug (str): The slug of the data source.

        Returns:
            dict: The JSON response from the API.

        Raises:
            RefreshTokenError: If the refresh token is invalid.
            HTTPError: If the POST request fails. Note that if the
            error code is 401, this is likely due to invalid credentials.
        """

        provenance_slug = f"{publisher_slug}:{source_slug}"
        with open(csv_path, "rb") as f:
            files = {"file": (csv_path, f)}
            resp = self.client.post(
                f"/records/{provenance_slug}/data",
                files=files,
            )
        resp.raise_for_status()

        return resp.json()

        """

        """
