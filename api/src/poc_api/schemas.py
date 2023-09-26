"""
This module defines the pydantic models for the API. The schemas are used to
validate the data sent to the API and to define the structure of the data
returned by the API.

For each model there is typically a response model and a "Create" model, e.g.
`Dataset` and `DatasetCreate`. The create models define the structure of data
we expect the user to pass to the API.
"""

from enum import Enum
from pydantic import BaseModel, Field
from typing import Literal


class Frequency(Enum):
    triennial = "triennial"
    biennial = "biennial"
    annual = "annual"
    semiannual = "semiannual"
    threeTimesAYear = "three_times_a_year"
    quarterly = "quarterly"
    bimonthly = "bimonthly"
    monthly = "monthly"
    semimonthly = "semimonthly"
    biweekly = "biweekly"
    threeTimesAMonth = "three_times_a_week"
    weekly = "weekly"
    semiweekly = "semiweekly"
    threeTimesAWeek = "three_times_a_week"
    daily = "daily"
    continuous = "continuous"
    irregular = "irregular"


class ContactPoint(BaseModel):
    name: str
    email: str = Field(pattern=r"^mailto:[\w\.-]+@[\w\.-]+\.\w{2,}$")
    telephone: str | None = Field(default=None)


class PeriodOfTime(BaseModel):
    start: str = Field(
        pattern=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(Z|[+-]\d{2}:\d{2})?$",
    )
    end: str = Field(
        pattern=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(Z|[+-]\d{2}:\d{2})?$",
    )


class Column(BaseModel):
    name: str
    title: str
    label: str
    description: str
    datatype: str
    aboutUrl: str | None = Field(default=None)
    propertyUrl: str | None = Field(default=None)
    valueUrl: str | None = Field(default=None)


class TableSchema(BaseModel):
    columns: list[Column]
    aboutUrl: str | None = Field(default=None)


class DistributionCreate(BaseModel):
    id: str = Field(alias="@id")
    type: Literal["dcat:DatasetSeries"] = Field(alias="@type")
    identifier: str
    media_type: str
    download_url: str


class Distribution(DistributionCreate):
    id: str = Field(alias="@id")
    type: Literal["dcat:DatasetSeries"] = Field(alias="@type")
    media_type: str
    download_url: str
    table_schema: TableSchema


# If we wanted to provide the ability to attach arbitrary RDF we might want to
# look at https://github.com/pydantic/pydantic/discussions/5853
class DatasetCreate(BaseModel):
    context: Literal["https://data.ons.gov.uk/ns#"] = Field(alias="@context")
    id: str = Field(alias="@id")
    type: Literal["dcat:DatasetSeries"] = Field(alias="@type")
    identifier: str
    title: str = Field(max_length=90)
    summary: str = Field(max_length=200)
    description: str = Field(max_length=250)
    issued_date: str = Field(
        pattern=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(Z|[+-]\d{2}:\d{2})?$"
    )
    next_release_date: str = Field(
        pattern=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(Z|[+-]\d{2}:\d{2})?$",
    )
    publisher: str
    creator: str
    contact_point: ContactPoint
    theme: str | list[str]
    frequency: Frequency
    keywords: list[str]
    licence: str
    spatial_coverage: str = Field(pattern=r"^[EJKLMNSW]{1}\d{8}$")
    temporal_coverage: PeriodOfTime
    temporal_resolution: str = Field(pattern=r"^P(\d{1,2}Y)?(\d{1,2}M)?(\d{1,2}D)?$")


class Dataset(DatasetCreate):
    # distribution: list[Distribution]
    pass


class EditionCreate(BaseModel):
    context: Literal["https://data.ons.gov.uk/ns#"] = Field(alias="@context")
    id: str = Field(alias="@id")
    type: Literal["dcat:Dataset"] = Field(alias="@type")
    identifier: str
    in_series: str
    title: str = Field(max_length=90)
    summary: str = Field(max_length=200)
    description: str = Field(max_length=250)
    issued_date: str = Field(
        pattern=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(Z|[+-]\d{2}:\d{2})?$"
    )
    distribution: Distribution


class Edition(EditionCreate):
    pass
