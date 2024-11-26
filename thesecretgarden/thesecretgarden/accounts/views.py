from django.contrib.auth import get_user_model, login
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView

from thesecretgarden.accounts.forms import AppUserCreateForm, AppUserLoginForm, ProfileEditForm
from thesecretgarden.accounts.models import Profile

UserModel = get_user_model()

class AppUserLoginView(LoginView):
    template_name = 'accounts/login-page.html'
    form_class = AppUserLoginForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['exclude_user_options'] = True

        return context


class AppUserRegisterView(CreateView):
    model = UserModel
    form_class = AppUserCreateForm
    template_name = 'accounts/register-page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['exclude_user_options'] = True

        return context

    def get_success_url(self):
        profile = self.object.profile
        if profile.is_complete():
            return reverse_lazy('plants-list')
        else:
            return reverse_lazy('profile-edit')

    def form_valid(self, form):
        super().form_valid(form)
        login(self.request, self.object)
        return redirect(self.get_success_url())

    # def form_valid(self, form):
    #     response = super().form_valid(form)
    #     login(self.request, self.object)
    #
    #     return response


class ProfileDetailsView(DetailView):
    model = Profile
    template_name = 'accounts/profile-details.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Profile, user__slug=self.kwargs['slug'])


class ProfileEditView(UpdateView):
    model = Profile
    form_class = ProfileEditForm
    template_name = 'accounts/profile-edit.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Profile, user__slug=self.kwargs['slug'])

    def get_success_url(self):
        return reverse_lazy('profile-details', kwargs={'slug': self.object.user.slug})
