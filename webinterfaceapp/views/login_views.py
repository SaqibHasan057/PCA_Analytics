from django.contrib.auth.views import LoginView
from django.utils.http import is_safe_url
from django.urls import reverse, reverse_lazy, resolve
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import REDIRECT_FIELD_NAME, login, logout as auth_logout, authenticate
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.http import HttpResponseRedirect

from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template import loader
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.conf import settings
from django.views.generic import *
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.db.models.query_utils import Q
from django.shortcuts import redirect

from authentication.forms import SignUpForm
from authentication.models import Profile


class SignIn(FormView):
    """
    Provides the ability to login as a user with a username and password
    """
    redirect_url_name = 'financialdataportal:home'
    redirect_url = reverse_lazy(redirect_url_name)
    success_url = redirect_url
    form_class = AuthenticationForm
    redirect_field_name = REDIRECT_FIELD_NAME
    template_name = 'authentication/login.html'

    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        # Sets a test cookie to make sure the user has cookies enabled
        if request.user.is_authenticated:
            redirect_to = request.POST.get('next', request.GET.get('next', ''))
            # check form validity
            # authenticate user
            if redirect_to and is_safe_url(url=redirect_to, host=request.get_host()):
                return redirect(redirect_to)
            else:
                return HttpResponseRedirect('/?next=home')

        request.session.set_test_cookie()

        return super(SignIn, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())

        # If the test cookie worked, go ahead and
        # delete it since its no longer needed
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()

        return super(SignIn, self).form_valid(form)

    def get_success_url(self):
        redirect_to = self.request.GET.get(self.redirect_field_name)
        if not is_safe_url(url=redirect_to, host=self.request.get_host()):
            redirect_to = self.success_url
        return redirect_to

    def get_context_data(self, **kwargs):
        context = super(SignIn, self).get_context_data(**kwargs)
        context['auth_form'] = AuthenticationForm
        login_url_name = 'authentication:sign_in'
        context['login_action'] = reverse(login_url_name)
        return context


class SignOut(RedirectView):
    """
    Provides users the ability to logout
    """
    url = '/?next=home'

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return super(SignOut, self).get(request, *args, **kwargs)


# Reset Password
class ResetPasswordRequestView(FormView):

    @staticmethod
    def validate_email_address(email):
        '''
        This method here validates the if the input is an email address or not. Its return type is boolean, True if the input is a email address or False if its not.
        '''

        try:
            validate_email(email)
            return True
        except ValidationError:
            return False

    def post(self, request, *args, **kwargs):
        '''
        A normal post request which takes input from field "email_or_username" (in ResetPasswordRequestForm).
        '''

        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data["email_or_username"]
        if self.validate_email_address(data) is True:  # uses the method written above
            '''
            If the input is an valid email address, then the following code will lookup for users associated with that email address. If found then an email will be sent to the address, else an error message will be printed on the screen.
            '''
            associated_users = User.objects.filter(Q(email=data) | Q(username=data))
            if associated_users.exists():
                for user in associated_users:
                    c = {
                        'email': user.email,
                        'domain': request.META['HTTP_HOST'],
                        'site_name': '127.0.0.1:8000',
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'user': user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    subject_template_name = 'DjangoECommerceApp/Authentication/PasswordReset/password_reset_subject.txt'
                    # copied from django/contrib/admin/templates/registration/password_reset_subject.txt to templates directory
                    email_template_name = 'DjangoECommerceApp/Authentication/PasswordReset/password_reset_email.html'
                    # copied from django/contrib/admin/templates/registration/password_reset_email.html to templates directory
                    subject = loader.render_to_string(subject_template_name, c)
                    # Email subject *must not* contain newlines
                    subject = ''.join(subject.splitlines())
                    email = loader.render_to_string(email_template_name, c)
                    send_mail(subject, email, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)
                result = self.form_valid(form)
                messages.success(request,
                                 'An email has been sent to ' + data + ". Please check its inbox to continue reseting password.")
                return result
            result = self.form_invalid(form)
            messages.error(request, 'No user is associated with this email address')
            return result
        else:
            '''
            If the input is an username, then the following code will lookup for users associated with that user. If found then an email will be sent to the user's address, else an error message will be printed on the screen.
            '''
            associated_users = User.objects.filter(username=data)
            if associated_users.exists():
                for user in associated_users:
                    c = {
                        'email': user.email,
                        'domain': '127.0.0.1:8000',  # or your domain
                        'site_name': 'example',
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'user': user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    subject_template_name = 'DjangoECommerceApp/Authentication/PasswordReset/password_reset_subject.txt'
                    email_template_name = 'DjangoECommerceApp/Authentication/PasswordReset/password_reset_email.html'
                    subject = loader.render_to_string(subject_template_name, c)
                    # Email subject *must not* contain newlines
                    subject = ''.join(subject.splitlines())
                    email = loader.render_to_string(email_template_name, c)
                    send_mail(subject, email, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)
                result = self.form_valid(form)
                messages.success(request,
                                 'Email has been sent to ' + data + "'s email address. Please check its inbox to continue reseting password.")
                return result
            result = self.form_invalid(form)
            messages.error(request, 'This username does not exist in the system.')
            return result
        messages.error(request, 'Invalid Input')
        return self.form_invalid(form)


class PasswordResetConfirmView(FormView):

    def post(self, request, uidb64=None, token=None, *arg, **kwargs):
        """
        View that checks the hash in a password reset link and presents a
        form for entering a new password.
        """
        # UserModel = get_user_model()
        form = self.form_class(request.POST)
        assert uidb64 is not None and token is not None  # checked by URLconf
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            if form.is_valid():
                new_password = form.cleaned_data['new_password2']
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password has been reset.')
                return self.form_valid(form)
            else:
                messages.error(request, 'Password reset has not been unsuccessful.')
                return self.form_invalid(form)
        else:
            messages.error(request, 'The reset password link is no longer valid.')
            return self.form_invalid(form)


class PublicPage(DetailView):
    template_name = 'authentication/profile.html'
    model = Profile

    # def get_context_data(self, **kwargs):
    # context = super(PublicPage, self).get_context_data(**kwargs)
    # current_url_name = resolve(self.request.path_info).url_name
    # context['auth_form'] = AuthenticationForm
    # login_url_name = 'authentication:sign_in'
    # context['login_action'] = reverse(login_url_name)
    # return context


class SignUp(FormView):
    template_name = 'authentication/registration.html'
    form_class = SignUpForm
    redirect_url_name = 'financialdataportal:home'
    redirect_url = reverse_lazy(redirect_url_name)
    success_url = redirect_url

    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        # Sets a test cookie to make sure the user has cookies enabled
        if request.user.is_authenticated:
            redirect_to = request.POST.get('next', request.GET.get('next', ''))
            # check form validity
            # authenticate user
            if redirect_to and is_safe_url(url=redirect_to, host=request.get_host()):
                return redirect(redirect_to)
            else:
                return HttpResponseRedirect('/?next=home')

        return super(SignUp, self).dispatch(request, *args, **kwargs)

    # def post(self, request, *args, **kwargs):
    #     '''
    #     A normal post request which takes input from field "email_or_username" (in ResetPasswordRequestForm).
    #     '''
    #
    #     form = self.form_class(request.POST)
    #     if form.is_valid():
    def form_valid(self, form):
        user = form.save()
        user.refresh_from_db()  # load the profile instance created by the signal
        user.profile.institution = form.cleaned_data.get('institution')
        user.profile.designation = form.cleaned_data.get('designation')
        user.profile.phone = form.cleaned_data.get('phone')
        user.profile.slug = user.username
        user.is_active = True
        group = form.cleaned_data.get('group')

        if group is None:
            group = 'general'

        if group == 'analyst':
            user.is_staff = True
        user.save()

        # raw_password = form.cleaned_data.get('password1')

        g = Group.objects.get(name=group)
        g.user_set.add(user)
        user = authenticate(username=user.username, password=form.cleaned_data.get('password1'))
        login(self.request, user)
        # print(user)
        # return super(SignUp, self).get(request, *args, **kwargs)
        return super(SignUp, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(SignUp, self).get_context_data(**kwargs)
        context['auth_form'] = SignUpForm
        registration_url_name = 'authentication:sign_up'
        context['registration_action'] = reverse(registration_url_name)
        return context


class LoginCancelledView(RedirectView):
    """
    Provides users the ability to logout
    """
    # url = '/?next=home'
    permanent = True

    def get(self, request, args, **kwargs):
        """
        Return the URL redirect to. Keyword arguments from the URL pattern
        match generating the redirect request are provided as kwargs to this
        method.
        """

        current_url_name = resolve(self.request.path_info).url_name
        current_url_name = 'authentication:signin'
        print('current url name')
        print(current_url_name)
        url = reverse(current_url_name)
        print('url')
        print(url)
        self.url = url
        print(url)
        return super(LoginCancelledView, self).get(request, args, **kwargs)
        # current_url_name = resolve(self.request.path_info).url_name
        # current_url_name = 'authentication:signin'
        # url = reverse(current_url_name)
        # print(url)
        # return url


login_cancelled = LoginCancelledView.as_view()
