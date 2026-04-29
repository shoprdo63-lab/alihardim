"""
Supabase client for user authentication
"""
from supabase import create_client, Client
from config import Config

# Initialize Supabase client
supabase: Client = None

def get_supabase():
    """Get or create Supabase client."""
    global supabase
    if supabase is None:
        supabase = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)
    return supabase


def sign_up(email: str, password: str, user_data: dict = None):
    """Register a new user with Supabase Auth."""
    try:
        supabase = get_supabase()
        
        # Sign up with Supabase Auth
        response = supabase.auth.sign_up({
            'email': email,
            'password': password,
            'options': {
                'data': user_data or {}
            }
        })
        
        return {
            'success': True,
            'user': response.user,
            'session': response.session
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def sign_in(email: str, password: str):
    """Sign in user with Supabase Auth."""
    try:
        supabase = get_supabase()
        
        response = supabase.auth.sign_in_with_password({
            'email': email,
            'password': password
        })
        
        return {
            'success': True,
            'user': response.user,
            'session': response.session
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def sign_out(access_token: str):
    """Sign out user."""
    try:
        supabase = get_supabase()
        supabase.auth.sign_out()
        return {'success': True}
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def get_user(access_token: str):
    """Get current user from token."""
    try:
        supabase = get_supabase()
        response = supabase.auth.get_user(access_token)
        return {
            'success': True,
            'user': response.user
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def update_user(user_id: str, user_data: dict):
    """Update user profile in Supabase database."""
    try:
        supabase = get_supabase()
        
        response = supabase.table('users').update(user_data).eq('id', user_id).execute()
        
        return {
            'success': True,
            'data': response.data
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def get_user_profile(user_id: str):
    """Get user profile from Supabase database."""
    try:
        supabase = get_supabase()
        
        response = supabase.table('users').select('*').eq('id', user_id).execute()
        
        if response.data:
            return {
                'success': True,
                'profile': response.data[0]
            }
        return {
            'success': False,
            'error': 'User not found'
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }
