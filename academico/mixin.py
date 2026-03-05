from django.core.exceptions import PermissionDenied

class RoleRequiredMixin:
    required_role = None

    def dispatch(self, request, *args, **kwargs):
        if request.user.tipo != self.required_role:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)