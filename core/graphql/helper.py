import django_filters
from graphql_relay import to_global_id
from graphql_relay.utils import unbase64

from core.django.models import ArchiveModel


def from_global_id(global_id):
    """return a db int id"""
    if isinstance(global_id, int) or global_id.isdigit():
        return global_id

    unbased_global_id = unbase64(global_id)
    _type, _id = unbased_global_id.split(':', 1)
    return _type, _id


class NodeModelMixin(object):
    """used for django model to get global base64 id"""

    @property
    def global_id(self):
        if not self.id:
            return None
        # regulation: { model name}Node
        return to_global_id(f'{self.__class__.__name__}Node', self.id)


class ArchiveModelFilter(django_filters.FilterSet):
    def filter_queryset(self, queryset):
        queryset = super(ArchiveModelFilter, self).filter_queryset(queryset)
        if issubclass(self._meta.model, ArchiveModel):
            fields = list(filter(lambda x: x.startswith(ArchiveModel.archive_field_name),
                                 self.form.cleaned_data.keys()))
            is_archive_conditions = list(filter(lambda x: self.form.cleaned_data.get(x) in [True, False], fields))
            if not is_archive_conditions:
                queryset = queryset.filter(is_archived=False)
        return queryset
