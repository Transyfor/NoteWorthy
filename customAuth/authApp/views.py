from django.shortcuts import render, redirect
from .models import MyUser, Stickies
from .forms import RegisterForm, LoginForm

# Create your views here.

def register(request): #registering using form
 form = RegisterForm()
 success = None
 if request.method=='POST':
  if MyUser.objects.filter(username=request.POST['username']).exists():
   error = "This username is already taken"
   return render(request, 'authApp/register.html', {'form': form, 'error': error})
  if MyUser.objects.filter(email=request.POST['email']).exists():
   error = "This email is already taken"
   return render(request, 'authApp/register.html', {'form': form, 'error': error})
  form = RegisterForm(request.POST) #How to add a new user with forms. Optional!
  new_user = form.save(commit=False)
  new_user.save()
  success = "New User Created Successfully !"
 return render(request, 'authApp/register.html', {'form': form, 'success': success})

def register2(request): #registering without using forms
    form= RegisterForm #Still necessary as the form in the HTML is made based off the form we pass.
    success=None
    if request.session.get('user_id'):
     return redirect('authApp:home')
    if request.method=='POST':
        if MyUser.objects.filter(username=request.POST['username']).exists():
          error = "This username is already taken"
          return render(request, 'authApp/register.html', {'form': form, 'error': error, 'username':request.POST['username'],'password':request.POST['password'],'email':request.POST['email'],'name':request.POST['name']})
        if MyUser.objects.filter(email=request.POST['email']).exists():
            error = "This email is already taken"
            return render(request, 'authApp/register.html', {'form': form, 'error': error, 'username':request.POST['username'],'password':request.POST['password'],'email':request.POST['email'],'name':request.POST['name']})
        guy= MyUser(name=request.POST['name'],email=request.POST['email'],username=request.POST['username'],password=request.POST['password'])
        guy.save()
        success="New User Created Successfully !"
    return render(request, 'authApp/register.html', {'form': form, 'success': success, 'username':"",'password':"",'email':"",'name':""})


def login(request):
 form = LoginForm()
 error=None
 if request.method=='POST':
  username = request.POST['username']
  password = request.POST['password']
  if MyUser.objects.filter(username=username, password=password).exists():
   user = MyUser.objects.get(username=username)
   request.session['user_id'] = user.id # This is a session variable and will remain existing as long as you don't delete this manually or clear your browser cache
   return redirect('authApp:home')
  else:
    error="Account does not exist."
    return render(request, 'authApp/login.html', {'form': form, 'error':error})
 if request.session.get('user_id'):
   return redirect('authApp:home')
 return render(request, 'authApp/login.html', {'form': form})


def home(request):
 success=None
 userStickies=None
 if 'user_id' in request.session:
  user = MyUser.objects.get(id=request.session['user_id'])
  request.session['name']=user.name
  request.session['email']=user.email
  request.session['username']=user.username
  request.session['password']=user.password
  userStickies= Stickies.objects.filter(creatorId=request.session['user_id']).order_by('-created_at')
  if request.method=='POST':
    Stickies(creatorId=request.session['user_id'], sticky=request.POST['stickyData']).save()
    success="Sticky Created!"
  return render(request, 'authApp/home.html', {'user': user, 'session':request.session, 'success': success, 'userStickies':userStickies}) # If we don't want to give the session
 # a bunch of sensitive information accessible anytime, we can instead make a user object which exists only for this page
 # Here, we passed both a one-time user object, and also session which holds everything for the duration of the browser's cache. 
 else:
  return redirect('authApp:login')
 
def logout(request):
 if 'user_id' in request.session:
  del request.session['user_id'] # delete user session
 return redirect('authApp:login')

def deleteSticky(request, sticky_id):
  Stickies.objects.get(id=sticky_id, creatorId= request.session['user_id']).delete()
  return redirect('authApp:home')