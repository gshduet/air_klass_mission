from rest_framework import permissions


class IsMasterOrReadOnly(permissions.BasePermission):
    """
        인증받은 사용자 본인의 정보가 아닐 경우 권한 제한
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.headers.get('Authorization', None):
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated and request.headers.get('Authorization', None):
            if hasattr(obj.user, 'email'):
                return obj.user.email == request.user.email
            else:
                return False

        return False


class IsMasterUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.COOKIES['access_token'] and request.COOKIES['is_master'])