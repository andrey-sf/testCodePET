from django.contrib import admin
from .models import Collect, Payment, Person
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

admin.site.site_header = "App for CodePET"
admin.site.index_title = "Панель администратора"


class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0


@admin.register(Collect)
class CollectAdmin(admin.ModelAdmin):
    list_display = ['title', 'id', 'author', 'occasion', 'target_amount', 'collected_amount', 'contributors_count',
                    'end_datetime']
    inlines = [PaymentInline]


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'collect', 'amount', 'timestamp')
    search_fields = ('user__name', 'collect__title')
    list_filter = ('timestamp', 'collect__title')


class UserModelAdmin(BaseUserAdmin):
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserModelAdmin
    # that reference specific fields on auth.User.
    list_display = ("id", "email", "name", "is_active", "is_admin", "is_verified")
    list_display_links = ("email",)
    list_filter = ("is_admin",)
    fieldsets = (
        ("User Credentials", {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("name", "is_verified")}),
        ("Permissions", {"fields": ("is_admin", "is_active")}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserModelAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "name", "password1", "password2"),
            },
        ),
    )
    search_fields = ("email", "name")
    ordering = ("email", "id")
    filter_horizontal = ()


# Now register the new UserModelAdmin...
admin.site.register(Person, UserModelAdmin)
