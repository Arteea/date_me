from rest_framework import permissions

class IsAuthenticatedAndOwner(permissions.BasePermission):


    # def has_object_permission(self,request,view,obj):
    #     print(obj.user==request.user)
    
    
    def has_permission(self,request,view):
        if request.user.is_staff:
            return True
        pk=view.kwargs.get('pk',None)
        print(request.data)
        return bool(int(request.user.id)==int(pk))