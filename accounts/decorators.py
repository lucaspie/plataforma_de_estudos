from django.core.exceptions import PermissionDenied


def role_required(tipo_permitido):

    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):

            if request.user.tipo != tipo_permitido:
                raise PermissionDenied

            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator