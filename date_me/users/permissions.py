from rest_framework import permissions

class IsAuthenticatedAndOwner(permissions.BasePermission):

    def has_permission(self,request,view,**kwargs):
        if request.user.is_staff:
            return True
        pk=view.kwargs.get('user_id',None)
        if pk:
            return bool(int(request.user.id)==int(pk))