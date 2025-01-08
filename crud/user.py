from crud.crud_base import CrudBase

from models import User


class UserCrud(CrudBase):
    pass

user_crud = UserCrud(User)