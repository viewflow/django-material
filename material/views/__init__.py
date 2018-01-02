from .create import CreateModelView
from .delete import DeleteModelView
from .detail import DetailModelView
from .list import ListModelView
from .update import UpdateModelView
from .viewset import ModelViewset

__all__ = (
    'ModelViewset', 'ListModelView', 'CreateModelView',
    'DeleteModelView', 'DetailModelView', 'UpdateModelView'
)
