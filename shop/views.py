from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from .models import contact, crop_recommend, CropDetail
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as ln, logout
from django.contrib import messages
from django.http import JsonResponse
import joblib
import os
import warnings

# Suppress scikit-learn version warnings
warnings.filterwarnings("ignore", category=UserWarning)

# Global variables - initialized as None
_model = None
_scaler = None
_label_encoder = None

def load_models():
    """Lazy load models to avoid numpy version issues at startup"""
    global _model, _scaler, _label_encoder
    
    if _model is None:
        try:
            MODEL_PATH = os.path.join(settings.BASE_DIR, 'models', 'model.pkl')
            SCALER_PATH = os.path.join(settings.BASE_DIR, 'models', 'scaler.pkl')
            LABEL_ENCODER_PATH = os.path.join(settings.BASE_DIR, 'models', 'label_encoder.pkl')
            
            # Check if model files exist
            if not os.path.exists(MODEL_PATH):
                print(f"❌ Model file not found: {MODEL_PATH}")
                return None, None, None
            
            _model = joblib.load(MODEL_PATH)
            _scaler = joblib.load(SCALER_PATH)
            _label_encoder = joblib.load(LABEL_ENCODER_PATH)
            print("✅ Models loaded successfully!")
        except Exception as e:
            print(f"❌ Error loading models: {e}")
            _model = None
            _scaler = None
            _label_encoder = None
    
    return _model, _scaler, _label_encoder

def index(request):
    """Home page view"""
    return render(request, 'shop/index.html')

def about(request):
    """About page view"""
    return render(request, 'shop/about.html')

def home(request):
    """Home page view"""
    return render(request, 'shop/home.html')

def terms(request):
    """Terms and conditions page view"""
    return render(request, 'shop/terms.html')

def result(request):
    """Result page view"""
    return render(request, 'shop/result.html')

@login_required
def recommendation_history(request):
    """View user's crop recommendation history"""
    history = crop_recommend.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'shop/history.html', {'history': history})

def user_contact(request):
    """Handle contact form submissions"""
    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        
        if not all([name, email, desc]):
            messages.error(request, "Name, Email, and Message are required.")
            return render(request, 'shop/contactus.html')
        
        ncontact = contact(name=name, email=email, phone=phone, desc=desc)
        ncontact.save()
        messages.success(request, "Your message has been sent successfully!")
        return redirect('shop:contact')
    return render(request, 'shop/contactus.html')

@login_required
def Crop_recommend(request):
    """Crop recommendation service with ML model"""
    crop = None
    crop_detail = None
    history = crop_recommend.objects.filter(user=request.user).order_by('-timestamp')
    
    # Load models only when needed
    model, scaler, label_encoder = load_models()
    
    if request.method == 'POST':
        # Check if models are loaded
        if model is None:
            messages.error(request, "Models are not loaded. Please contact administrator.")
            return render(request, 'shop/service.html', {'history': history})
        
        try:
            # Get form data
            N = float(request.POST.get('N', 0))
            P = float(request.POST.get('P', 0))
            K = float(request.POST.get('K', 0))
            temperature = float(request.POST.get('temperature', 0))
            humidity = float(request.POST.get('humidity', 0))
            pH = float(request.POST.get('pH', 0))
            rainfall = float(request.POST.get('rainfall', 0))
            
            # Validate input ranges
            if N < 0 or P < 0 or K < 0 or temperature < -50 or temperature > 60:
                messages.error(request, "Please enter valid values within acceptable ranges.")
                return render(request, 'shop/service.html', {'history': history})
            
            # Prepare features
            features = [[N, P, K, temperature, humidity, pH, rainfall]]
            features_scaled = scaler.transform(features)
            
            # Make prediction
            pred_encoded = model.predict(features_scaled)[0]
            crop = label_encoder.inverse_transform([pred_encoded])[0]
            
            # Save to history
            crop_recommend.objects.create(
                user=request.user,
                nitrogen=N,
                phosphorus=P,
                potassium=K,
                temperature=temperature,
                humidity=humidity,
                ph=pH,
                rainfall=rainfall,
                predicted_crop=crop
            )
            
            # Get crop details
            try:
                crop_detail = CropDetail.objects.get(name__iexact=crop)
            except CropDetail.DoesNotExist:
                crop_detail = None

        except ValueError as e:
            crop = f"Error: Invalid input values"
            messages.error(request, f"Please enter valid numeric values: {str(e)}")
        except Exception as e:
            crop = f"Error: {e}"
            messages.error(request, f"Prediction error: {str(e)}")
            
    context = {
        'crop': crop,
        'crop_detail': crop_detail,
        'N': request.POST.get('N', 60),
        'P': request.POST.get('P', 30),
        'K': request.POST.get('K', 30),
        'temperature': request.POST.get('temperature', 25),
        'humidity': request.POST.get('humidity', 50),
        'pH': request.POST.get('pH', 6.5),
        'rainfall': request.POST.get('rainfall', 100),
        'history': history
    }
    return render(request, 'shop/service.html', context)

def user_login(request):
    """User login view"""
    # If user is already logged in, redirect to service
    if request.user.is_authenticated:
        messages.info(request, f"You are already logged in as {request.user.username}")
        return redirect('shop:service')
    
    if request.method == 'POST':
        loginusername = request.POST.get('loginusername', '').strip()
        loginpassword = request.POST.get('loginpassword', '').strip()
        
        if not loginusername or not loginpassword:
            messages.error(request, "Please enter both username and password.")
            return redirect('shop:login')
        
        # Check if user exists
        try:
            user_exists = User.objects.filter(username=loginusername).exists()
            if not user_exists:
                messages.error(request, 'Invalid Credentials. Please Enter Valid Credentials.')
                return redirect('shop:login')
        except Exception:
            messages.error(request, 'Invalid Credentials. Please Enter Valid Credentials.')
            return redirect('shop:login')
        
        # Authenticate user
        user = authenticate(request, username=loginusername, password=loginpassword)
        
        if user is not None:
            ln(request, user)
            # Set session to persist
            request.session.set_expiry(1209600)  # 2 weeks
            
            # Check if user is active
            if user.is_active:
                messages.success(request, f"Successfully Logged In. Welcome {user.username}!")
                return redirect('shop:service')
            else:
                messages.error(request, "Your account is disabled. Please contact support.")
                return redirect('shop:login')
        else:
            messages.error(request, 'Invalid Credentials. Please Enter Valid Credentials.')
            return redirect('shop:login')
    
    return render(request, 'shop/login.html')

def user_logout(request):
    """User logout view - handles both GET and POST requests"""
    # Clear session data completely
    request.session.flush()
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('shop:login')

def user_signup(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('shop:service')
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        fname = request.POST.get('fname', '').strip()
        lname = request.POST.get('lname', '').strip()
        email = request.POST.get('email', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        
        # Validate inputs
        if not all([username, fname, email, password1, password2]):
            messages.error(request, "All fields are required.")
            return redirect('shop:signup')
        
        if len(username) < 3:
            messages.error(request, 'Username must be at least 3 characters long')
            return redirect('shop:signup')
        
        if len(username) > 30:
            messages.error(request, 'Username must be less than 30 characters')
            return redirect('shop:signup')
        
        if not username.isalnum():
            messages.error(request, 'Username must be Alphanumeric')
            return redirect('shop:signup')
            
        if password1 != password2:
            messages.error(request, "Password doesn't match")
            return redirect('shop:signup')
        
        if len(password1) < 6:
            messages.error(request, "Password must be at least 6 characters long")
            return redirect('shop:signup')
        
        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists. Please choose a different username.")
            return redirect('shop:signup')
        
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered. Please use a different email.")
            return redirect('shop:signup')
        
        try:
            myuser = User.objects.create_user(
                username=username, 
                email=email, 
                password=password1
            )
            myuser.first_name = fname
            myuser.last_name = lname
            myuser.save()
            
            messages.success(request, 'Your account has been created successfully! Please login.')
            return redirect('shop:login')
        except Exception as e:
            messages.error(request, f'Error creating account: {str(e)}')
            return redirect('shop:signup')
    
    return render(request, 'shop/signup.html')

@login_required
def delete_history(request):
    """Delete user's crop recommendation history"""
    if request.method == 'POST':
        if 'delete_all' in request.POST:
            deleted_count, _ = crop_recommend.objects.filter(user=request.user).delete()
            if deleted_count > 0:
                messages.success(request, "All history records deleted successfully.")
            else:
                messages.info(request, "No history records found to delete.")
        else:
            recommend_id = request.POST.get('recommend_id')
            if recommend_id:
                try:
                    obj = crop_recommend.objects.get(recommend_id=recommend_id, user=request.user)
                    obj.delete()
                    messages.success(request, "History deleted successfully.")
                except crop_recommend.DoesNotExist:
                    messages.error(request, "Record not found or permission denied.")
            else:
                messages.error(request, "Invalid history ID.")
    return redirect('shop:history')

# Debug view - optional, remove in production
def debug_models(request):
    """Debug view to check model loading status"""
    if not request.user.is_staff:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    
    model, scaler, label_encoder = load_models()
    
    import numpy as np
    return JsonResponse({
        'model_loaded': model is not None,
        'scaler_loaded': scaler is not None,
        'label_encoder_loaded': label_encoder is not None,
        'numpy_version': np.__version__,
        'joblib_version': joblib.__version__,
        'model_path': os.path.join(settings.BASE_DIR, 'models', 'model.pkl'),
        'scikit_learn_version': __import__('sklearn').__version__
    })