from crud.crud_base import CrudBase

from models import Location


class LocationCrud(CrudBase):
    pass

location_crud = LocationCrud(Location)