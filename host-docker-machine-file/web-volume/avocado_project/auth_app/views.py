from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login, logout

from .forms import LoginForm

# Create your views here.

# Show Login Page and if login failed, show error message / if login successed, back to the last page
def loginview(request, redirect_url="/finder/"):

    #### 1. Login Data Passed
    if request.method == 'POST':
        # form instance with data
        form = LoginForm(request.POST)
        #### 1-1. Form Data Valid -> Check if it is user
        if form.is_valid():
            # process the data in form.cleaned_data as required
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Custom EmailBackend in auth_app.backends.py
            user = authenticate(username=email, password=password)

            #### (1) Authenticated Successfully -> go to index home
            if user is not None :
                login(request, user)
                return redirect(redirect_url)

            #### (2) Not a user -> go to login page with not-user message
            else :
                return render(request, "auth_app/login.html",{'form':form, 'message':"아이디 또는 패스워드가 일치하지 않습니다"})


        #### 1-2. Form Data invalid -> Show Field Error Message
        else :
            # "form.errors" contains error message and form_snippet.html template has spaces for the error messages, (So Just Pass "form")
            return render(request, "auth_app/login.html",{'form':form})

    #### 2. Login Data Not! Passed (New Login)
    else:
        form = LoginForm()

    return render(request, 'auth_app/login.html', {'form': form})

# Do Logout And Redirect to the first page
# TODO : logoutview 완성
def logoutview(request):
    logout(request)
    return redirect(to="/")