from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .models import *
from django.contrib.auth.forms import UserCreationForm

# Register your models here.

class InLineUser(admin.StackedInline):
  model = User


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'middle_name', 'last_name',
                  'phone_number', 
                  'user_type', 
                  'is_admin', 'is_staff')


class RoleAdmin(admin.ModelAdmin):
  #inlines=[InLineUser]
  def get_actions(self, request):
    actions = super().get_actions(request)
    if 'delete_selected' in actions:
        del actions['delete_selected']
    return actions
  def change_to_lecturer(modeladmin, request, queryset):
    for object in queryset:
      object.user_id.user_type = "lecturer"
      object.save()
  def change_to_student(model,request,queryset):
    for object in queryset:
      object.user_id.user_type = "student"
      object.save()
  def remove_role(model,request,queryset):
    for object in queryset:
      object.user_id.user_type = ""
      object.save()
  def delete_selected(model,request,queryset):
    for object in queryset:
      object.user_id.user_type = ""
      object.save()
    queryset.delete()
  actions=[change_to_lecturer,change_to_student,remove_role,delete_selected]

class NewUserAdmin(UserAdmin):
    add_form = UserCreateForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'middle_name', 'last_name', 
            'user_type', 
            'password1', 'password2', 'phone_number'),
        }),
    )
    list_display = ('email', 'first_name', 'is_admin', 
    'user_type'
    )
    search_fields = ('email','first_name')
    readonly_fields = ('id',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    ordering = ('email',)
    def change_to_lecturer(self, request, queryset):
      for user in queryset:
        user.user_type = "Lecturer"
        user.save()
    def change_to_student(self,request,queryset):
      for user in queryset:
        user.user_type = "Student"
        user.save()
    def remove_role(self,request,queryset):
      for user in queryset:
        user.user_type = ""
        user.save()
    actions=[change_to_lecturer,change_to_student,remove_role]

admin.site.register(User, NewUserAdmin)
admin.site.register(Student)
admin.site.register(Lecturer)
admin.site.unregister(Group)