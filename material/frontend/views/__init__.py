from .create import CreateModelView
from .list import ListModelView
from .update import UpdateModelView
from .delete import DeleteModelView
from .details import DetailsModelView
from .viewset import ModelViewSet


__all__ = [
    'CreateModelView', 'ListModelView', 'UpdateModelView',
    'DeleteModelView', 'DetailsModelView', 'ModelViewSet'
]