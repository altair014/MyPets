# from django.contrib.auth.views import redirect_to_login

# from django.contrib.messages import info, debug, success, warning, error

# from django.contrib.auth import logout #It has nothing to do with the Permissions.

# class SomeLoginRequiredMixin:

#     some_login_url = '/pets/user_login_route'
#     redirect_field_name = 'next'

#     # def dispatch(self, request, *args, **kwargs):
#     #     path = self.request.path
#     #     if request.user.is_authenticated == False:
#     #         return redirect_to_login(path, self.some_login_url, self.redirect_field_name,)
#     #     return super().dispatch(request, *args, **kwargs)
    
#     def dispatch(self, request, *args, **kwargs):
#         print(self.__class__.__name__)
#         path = self.request.path
#         if not request.user.is_authenticated:
#             info(request=request, message='Please provide your credentials.')
#             return redirect_to_login(path, self.some_login_url, self.redirect_field_name,)
#         elif request.user.is_authenticated and (request.user.is_superuser or request.user.is_staff):
#             error(request=request, message='You are not authorized.')
#             logout(request=request)
#             return redirect_to_login(path, self.some_login_url, self.redirect_field_name,)
#         else:
#             success(request=request, message='You have successfully logged in.')
#             return super().dispatch(request, *args, **kwargs)


from django.contrib.auth import REDIRECT_FIELD_NAME, logout

from django.contrib.auth.views import redirect_to_login

from django.contrib.messages import info, debug, success, warning, error, add_message

from django.shortcuts import redirect


class SomeAccessMixin:
    login_url = '/pets/user_login_route'
    redirect_field_name = REDIRECT_FIELD_NAME

    def get_login_url(self):
        login_url = self.login_url
        return str(login_url)

    def handle_no_permission(self):
        path = self.request.path        
        return redirect_to_login(path, self.login_url, self.redirect_field_name,)    

class SomeLoginRequiredMixin(SomeAccessMixin):
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        # elif request.user.is_authenticated and (request.user.is_superuser or request.user.is_staff):
        #     self.request.session.flush()
        #     error(request=request, message='You are not authorized.')
        #     return self.handle_no_permission()
        else:
            return super().dispatch(request, *args, **kwargs)


class SomePermissionRequiredMixin(SomeAccessMixin):

    permission_required = None

    def get_permission_required(self):

        if isinstance(self.permission_required, str):
            perms = (self.permission_required,)
        else:
            perms = self.permission_required
        return perms

    def has_permission(self):
        perms = self.get_permission_required()
        return self.request.user.has_perms(perms)

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            add_message(request=request, message='You do not have the required permissions to perform this action, please contact your system administrator.', level=40, extra_tags='danger')
            logout(request=request)
            if self.request.GET.get('next') != None:
                return redirect(self.request.GET.get('next'))
            return redirect(self.login_url)
        return super().dispatch(request, *args, **kwargs)