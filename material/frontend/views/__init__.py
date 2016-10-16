from .create import CreateModelView
from .delete import DeleteModelView
from .detail import DetailModelView
from .list import ListModelView
from .update import UpdateModelView
from .viewset import ModelViewSet


__all__ = (
    'CreateModelView', 'ListModelView', 'UpdateModelView',
    'DeleteModelView', 'DetailModelView', 'ModelViewSet',
)
