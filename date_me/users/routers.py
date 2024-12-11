from rest_framework import routers

UserProfileRouter=routers.SimpleRouter()
UserProfileRouter.register('profile',viewset='users.views.UserProfileView',basename='profile')