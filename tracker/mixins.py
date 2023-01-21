from django.core.exceptions import PermissionDenied
from bug_tracker.constants import DEMO


class GroupsRequiredMixin:
    """
    :param groups: list of group strings
    """
    groups = None

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.groups.filter(name__in=self.groups).exists():
                return super().dispatch(request, *args, **kwargs)
            else:
                raise PermissionDenied  # if not in group
        else:
            raise PermissionDenied  # if not logged in


class DemoGroupNotAlowed:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.groups.filter(name=DEMO).exists():
                raise PermissionDenied  # if in DEMO group
            else:
                return super().dispatch(request, *args, **kwargs)  # not in demo group and logged in
        else:
            raise PermissionDenied  # if not logged in
