import jwt
from datetime import datetime,timedelta
from django.conf import settings
from user_control.models import *

def get_access_token(payload,days):
    token = jwt.encode(
        {"exp":datetime.now() + timedelta(days=days), **payload},
        settings.SECRET_KEY,
        algorithm='HS256'
    )

    return  token

def decodeJWT(bearer):
    if not bearer:
        return None
    token = bearer[7:]

    try:
        decoded_jwt = jwt.decode(token,key=settings.SECRET_KEY,algorithm='HS256')
    except Exception:
        return None

    if decoded_jwt:
        try:
            return CustomUser.objects.get(id=decoded_jwt["user_id"])
        except Exception:
            return None