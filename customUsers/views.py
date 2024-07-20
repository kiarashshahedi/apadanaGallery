from django.shortcuts import render, redirect
from .click_api import login, register, get_user_info, update_user, change_password
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .models import CustomUser
from django.contrib.auth.decorators import login_required

def login_view(request):
    """
    ویو ورود کاربر. اگر درخواست POST باشد، تلاش می‌کند کاربر را با استفاده از API کلید وارد کند.
    در غیر این صورت، فرم ورود را نمایش می‌دهد.
    """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        mac_address = request.POST['mac_address']
        otp = request.POST['otp']
        response = login(username, password, mac_address, otp)
        if response.get('success'):
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('home')
    return render(request, 'login.html')

def register_view(request):
    """
    ویو ثبت‌نام کاربر. اگر درخواست POST باشد، تلاش می‌کند کاربر را با استفاده از API کلید ثبت‌نام کند.
    در غیر این صورت، فرم ثبت‌نام را نمایش می‌دهد.
    """
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        mobile_phone = request.POST['mobile_phone']
        otp = request.POST['otp']
        is_demo = request.POST.get('is_demo', False)
        response = register(first_name, last_name, mobile_phone, otp, is_demo)
        if response.get('success'):
            user = CustomUser.objects.create_user(
                username=mobile_phone,
                first_name=first_name,
                last_name=last_name,
                mobile_phone=mobile_phone,
                is_demo=is_demo
            )
            user.set_password(response.get('password'))  # ذخیره رمز عبور از پاسخ API
            user.save()
            return redirect('login')
    return render(request, 'register.html')

@login_required
def user_info_view(request):
    """
    ویو اطلاعات کاربر. اطلاعات کاربر را با استفاده از API کلید دریافت کرده و نمایش می‌دهد.
    """
    user_guid = request.user.user_guid
    user_info = get_user_info(user_guid)
    return render(request, 'shop/user_info.html', {'user_info': user_info})

@login_required
def update_user_view(request):
    """
    ویو ویرایش اطلاعات کاربر. وضعیت کاربر را با استفاده از API کلید به‌روزرسانی می‌کند.
    """
    if request.method == 'POST':
        user_guid = request.user.user_guid
        status = request.POST['status']
        response = update_user(user_guid, status)
        if response.get('success'):
            return redirect('user_info')
    return render(request, 'update_user.html')

@login_required
def change_password_view(request):
    """
    ویو تغییر رمز عبور کاربر. رمز عبور کاربر را با استفاده از API کلید به‌روزرسانی می‌کند.
    """
    if request.method == 'POST':
        user_guid = request.user.user_guid
        previous_password = request.POST['previous_password']
        new_password = request.POST['new_password']
        response = change_password(user_guid, previous_password, new_password)
        if response.get('success'):
            return redirect('user_info')
    return render(request, 'change_password.html')
