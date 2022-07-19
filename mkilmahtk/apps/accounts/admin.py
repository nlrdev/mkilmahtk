from django.contrib import admin
from .models import ServiceUser, Account, LastLogin


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    pass



@admin.register(ServiceUser)
class ServiceUserAdmin(admin.ModelAdmin):
    pass



@admin.register(LastLogin)
class LastLoginAdmin(admin.ModelAdmin):
    pass



