from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.contrib.auth import authenticate,login
from .forms import SignUpForm
# Create your views here.
def signup_view(request):
    if request.method == 'POST':
        f = SignUpForm(request.POST)
        if f.is_valid():
            user=f.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('accounts/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            to_email = f.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
            """username=f.cleaned_data.get('username')
            raw_pswd=f.cleaned_data.get('password1')
            email=f.cleaned_data.get('email')
            user=authenticate(username=username, password=raw_pswd)
            login(request,user)
            print(f)
            return render(request,'accounts/layout.html',{'user':username,'email':email})"""
            #return redirect('list')

    else:
        f = SignUpForm()

    return render(request, 'accounts/signup.html', {'form': f})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')