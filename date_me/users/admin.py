from django.contrib import admin

from users.models import User,UserInfo,UsersMedia

admin.site.register(User)
admin.site.register(UserInfo)
admin.site.register(UsersMedia)