from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login
from .forms import SignUpForm
# Create your views here.
def signup_view(request):
    if request.method == 'POST':
        f = SignUpForm(request.POST)
        if f.is_valid():
            f.save()
            username=f.cleaned_data.get('username')
            raw_pswd=f.cleaned_data.get('password1')
            email=f.cleaned_data.get('email')
            user=authenticate(username=username, password=raw_pswd)
            login(request,user)
            print(f)
            return render(request,'accounts/layout.html',{'user':username,'email':email})
            #return redirect('list')

    else:
        f = SignUpForm()

    return render(request, 'accounts/signup.html', {'form': f})

