"""
Authentication routes using Supabase
"""
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session
from app.utils.supabase_client import sign_up, sign_in, sign_out, get_user

auth = Blueprint('auth', __name__)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    """User registration using Supabase."""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        
        # Validate
        if not email or not password:
            return render_template('register.html', error='אנא מלא אימייל וסיסמה')
        
        if len(password) < 6:
            return render_template('register.html', error='הסיסמה חייבת להכיל לפחות 6 תווים')
        
        # Register with Supabase
        result = sign_up(email, password, {
            'first_name': first_name,
            'last_name': last_name
        })
        
        if result['success']:
            # Store session
            session['access_token'] = result['session'].access_token
            session['user'] = {
                'id': result['user'].id,
                'email': result['user'].email,
                'first_name': first_name,
                'last_name': last_name
            }
            return redirect(url_for('main.index'))
        else:
            return render_template('register.html', error=result.get('error', 'שגיאה בהרשמה'))
    
    return render_template('register.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """User login using Supabase."""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            return render_template('login.html', error='אנא מלא אימייל וסיסמה')
        
        # Sign in with Supabase
        result = sign_in(email, password)
        
        if result['success']:
            # Store session
            session['access_token'] = result['session'].access_token
            session['user'] = {
                'id': result['user'].id,
                'email': result['user'].email,
                'first_name': result['user'].user_metadata.get('first_name', ''),
                'last_name': result['user'].user_metadata.get('last_name', '')
            }
            return redirect(url_for('main.index'))
        else:
            return render_template('login.html', error='אימייל או סיסמה שגויים')
    
    return render_template('login.html')


@auth.route('/logout')
def logout():
    """Logout user."""
    access_token = session.get('access_token')
    if access_token:
        sign_out(access_token)
    
    session.clear()
    return redirect(url_for('main.index'))


@auth.route('/profile')
def profile():
    """User profile page."""
    user = session.get('user')
    if not user:
        return redirect(url_for('auth.login'))
    
    return render_template('profile.html', user=user)
