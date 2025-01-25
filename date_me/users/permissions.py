from rest_framework import permissions

class IsAuthenticatedAndOwner(permissions.BasePermission):

    def has_permission(self,request,view,**kwargs):
        if request.user.is_staff:
            return True
        request.query_params.get("user_id")