from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, UserProfileUpdateForm
# Create your views here.

def register(request):

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account is created for {}'.format(username))
            return redirect('blog-home')
    elif request.method == "GET":
        # print('entered!')
        form = RegisterForm()
    return render(request, 'common/register.html', {'form': form})

# only authenticated users can view their profile only
@login_required
def profile(request):
    if request.method == 'POST':
        # image exist within a form so request.FILES is also given
        # instance given because fields should be pre-filled and postdata saved on the instance
        user_form = UserProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Acccount info is updated!')
            return redirect('profile')
    else:
        user_form = UserProfileUpdateForm(instance=request.user)

    context = {'form': user_form}
    return render(request, 'common/profile.html', context)