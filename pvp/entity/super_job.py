from typing import Literal

from pydantic import BaseModel, AnyUrl, Field


__all__ = ['SuperJobAPIVacancies']


class FieldsIDTitle(BaseModel):
    id: int
    title: str


class ObjectsCataloguesPositions(BaseModel):
    id: int
    key: int
    title: str


class ObjectsCatalogues(BaseModel):
    id: int
    key: int
    positions: list[ObjectsCataloguesPositions]
    title: str


class ObjectsTown(BaseModel):
    declension: str
    genitive: str
    hasMetro: bool
    id: int
    title: str


class ObjectsPhones(BaseModel):
    additionalNumber: str | None
    number: str | None


class ObjectsClient(BaseModel):
    address: str | None
    addresses: list | None
    client_logo: AnyUrl | None
    description: str | None
    id: int | None
    industry: list
    is_blocked: bool | None
    link: AnyUrl | None
    registered_date: int | None
    short_reg: bool | None
    staff_count: str | None
    title: str | None
    town: ObjectsTown | None
    url: AnyUrl | None
    vacancy_count: int | None


class SuperJobAPIVacanciesObject(BaseModel):
    address: str | None
    age_from: int
    age_to: int
    agency: FieldsIDTitle
    agreement: bool
    already_sent_on_vacancy: bool
    anonymous: bool
    canEdit: bool
    candidat: str
    catalogues: list[ObjectsCatalogues]
    children: FieldsIDTitle
    client: ObjectsClient
    client_logo: AnyUrl | None
    compensation: None
    contact: str | None
    covid_vaccination_requirement: FieldsIDTitle
    currency: Literal['rub', 'uah', 'uzs']
    date_archived: int
    date_pub_to: int
    date_published: int
    driving_licence: list
    education: FieldsIDTitle
    experience: FieldsIDTitle
    external_url: AnyUrl | None
    favorite: bool
    fax: None
    faxes: None
    firm_activity: str | None
    firm_name: str
    gender: FieldsIDTitle
    highlight: bool
    id: int
    id_client: int
    isBlacklisted: bool
    is_archive: bool
    is_closed: bool
    is_storage: bool
    languages: list
    latitude: float | None
    link: AnyUrl
    longitude: float | None
    maritalstatus: FieldsIDTitle
    metro: list
    moveable: bool
    salary_minimal: int = Field(alias="payment_from")
    salary_maximum: int = Field(alias="payment_to")
    phone: str | None
    phones: list[ObjectsPhones] | None
    place_of_work: FieldsIDTitle
    profession: str
    rejected: bool
    response_info: list
    town: ObjectsTown
    type_of_work: FieldsIDTitle
    vacancyRichText: str
    work: None


class SuperJobAPIVacancies(BaseModel):
    more: bool
    objects: list[SuperJobAPIVacanciesObject]
    subscription_active: bool
    subscription_id: int
    total: int
