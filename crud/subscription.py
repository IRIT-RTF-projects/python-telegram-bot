from crud.crud_base import CrudBase
from models import Subscription


class SubscriptionCrud(CrudBase):
    pass

subscription_crud = SubscriptionCrud(Subscription)