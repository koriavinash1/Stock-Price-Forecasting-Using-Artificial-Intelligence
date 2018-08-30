from essentials.views import randomString,getCurrentTime,errorResp
from models import authToken,verificationCode
from constants import AUTH_EXPIRY_MINS
from StockNest.settings import LOGIN_URL
from django.http import HttpResponseRedirect,JsonResponse,HttpRequest
from django.db.models import Q
from school.funcs import isDemoUser, demoError

# server = "https://eduhubweb.com"
# if DEBUG:
#     server = "http://localhost:8000"

def getNewAuth():
    while(1):
        new_auth = randomString(50)
        existing = authToken.objects.filter(Q(mauth = new_auth)|Q(wauth = new_auth)|Q(pmauth = new_auth)|Q(pwauth = new_auth)).count()
        if existing == 0:
            return new_auth

def getUserAuth(typeVal,u):
    if typeVal == 'm':
        try:
            at = authToken.objects.get(user=u)
            at.misExpired = False
            at.mlastUpdated = getCurrentTime()
            at.pmauth = at.mauth
            at.mauth = getNewAuth()
            at.save()
            return at.mauth
        except authToken.DoesNotExist:#first login
            at = authToken.objects.create(user=u, mauth = getNewAuth(),wauth= getNewAuth(),pmauth = getNewAuth(),pwauth= getNewAuth())
            return at.mauth
        
    elif typeVal == 'w':
        try:
            at = authToken.objects.get(user=u)
            at.wisExpired = False
            at.wlastUpdated = getCurrentTime()
            at.pwauth = at.wauth
            at.wauth = getNewAuth()
            at.save()
            return at.wauth
        except authToken.DoesNotExist:#first login
            at = authToken.objects.create(user=u, mauth = getNewAuth(),wauth= getNewAuth(),pmauth = getNewAuth(),pwauth= getNewAuth())
            return at.wauth


### authentication decorative for our website
### time based 
def stocknestAPI(loginRequired=False,function=None):
    def _dec(view_func):
        def _view(request, *args, **kwargs):
            request.user = None
            headers = request.META
            if loginRequired:#if required, return 401/412
                if 'HTTP_AUTHORIZATION' in headers:
                    value = headers['HTTP_AUTHORIZATION'] #format keyw/m=auth
                    elements = value.split('=')
                    if len(elements) != 2:
                        return errorResp(401)
                    auth_val = elements[1]
                    if elements[0]  == 'keym':
                        try:
                            obj = authToken.objects.get(mauth=auth_val)
                            if not checkAuthTimestamp(obj.mlastUpdated):
                                obj.misExpired = True
                                obj.save()
                                return errorResp(412,"Auth expired")
                            request.user = obj.user
                            if request.method in ['POST','PUT','PATCH','DELETE']:
                                if isDemoUser(request.user):
                                    return demoError()
                            return view_func(request, *args, **kwargs)
                        except authToken.DoesNotExist:
                            try:
                                obj = authToken.objects.get(pmauth=auth_val)
                                if not checkAuthTimestamp(obj.mlastUpdated):
                                    obj.misExpired = True
                                    obj.save()
                                    return errorResp(412,"Auth expired")
                                request.user = obj.user
                                if request.method in ['POST','PUT','PATCH','DELETE']:
                                    if isDemoUser(request.user):
                                        return demoError()
                                return view_func(request, *args, **kwargs)
                            except authToken.DoesNotExist:
                                return errorResp(401,"Token not found")
                    elif elements[0] == 'keyw':
                        try:
                            obj = authToken.objects.get(wauth=auth_val)
                            if not checkAuthTimestamp(obj.wlastUpdated):
                                obj.wisExpired = True
                                obj.save()
                                return errorResp(412,"Auth expired")
                            request.user = obj.user
                            if request.method in ['POST','PUT','PATCH','DELETE']:
                                if isDemoUser(request.user):
                                    return demoError()
                            return view_func(request, *args, **kwargs)
                        except authToken.DoesNotExist:
                            try:
                                obj = authToken.objects.get(pwauth=auth_val)
                                if not checkAuthTimestamp(obj.wlastUpdated):
                                    obj.wisExpired = True
                                    obj.save()
                                    return errorResp(412,"Auth expired")
                                request.user = obj.user
                                if request.method in ['POST','PUT','PATCH','DELETE']:
                                    if isDemoUser(request.user):
                                        return demoError()
                                return view_func(request, *args, **kwargs)
                            except authToken.DoesNotExist:
                                return errorResp(401,"Token not found")
                    else:
                        return errorResp(401)
                else:
                    return errorResp(401)
            else:#not required send 412
                if 'HTTP_AUTHORIZATION' in headers:
                    value = headers['HTTP_AUTHORIZATION'] #format key=auth
                    elements = value.split('=')
                    if len(elements) != 2:
                        return errorResp(401)
                    auth_val = elements[1]
                    if elements[0]  == 'keym':
                        try:
                            obj = authToken.objects.get(mauth=auth_val)
                            if not checkAuthTimestamp(obj.mlastUpdated):
                                obj.misExpired = True
                                obj.save()
                                return errorResp(412,"Auth expired")
                            request.user = obj.user
                            if request.method in ['PATCH','DELETE']:
                                if isDemoUser(request.user):
                                    return demoError()
                            return view_func(request, *args, **kwargs)
                        except authToken.DoesNotExist:
                            try:
                                obj = authToken.objects.get(pmauth=auth_val)
                                if not checkAuthTimestamp(obj.mlastUpdated):
                                    obj.misExpired = True
                                    obj.save()
                                    return errorResp(412,"Auth expired")
                                request.user = obj.user
                                if request.method in ['PATCH','DELETE']:
                                    if isDemoUser(request.user):
                                        return demoError()
                                return view_func(request, *args, **kwargs)
                            except authToken.DoesNotExist:
                                return errorResp(401,"Token not found")
                    elif elements[0] == 'keyw':
                        try:
                            obj = authToken.objects.get(wauth=auth_val)
                            if not checkAuthTimestamp(obj.wlastUpdated):
                                obj.wisExpired = True
                                obj.save()
                                return errorResp(412,"Auth expired")
                            request.user = obj.user
                            if request.method in ['PATCH','DELETE']:
                                if isDemoUser(request.user):
                                    return demoError()
                            return view_func(request, *args, **kwargs)
                        except authToken.DoesNotExist:
                            try:
                                obj = authToken.objects.get(pwauth=auth_val)
                                if not checkAuthTimestamp(obj.wlastUpdated):
                                    obj.wisExpired = True
                                    obj.save()
                                    return errorResp(412,"Auth expired")
                                request.user = obj.user
                                if request.method in ['PATCH','DELETE']:
                                    if isDemoUser(request.user):
                                        return demoError()
                                return view_func(request, *args, **kwargs)
                            except authToken.DoesNotExist:
                                return errorResp(401,"Token not found")
                return view_func(request, *args, **kwargs)
        _view.__name__ = view_func.__name__
        _view.__dict__ = view_func.__dict__
        _view.__doc__ = view_func.__doc__

        return _view

    if function is None:
        return _dec
    else:
        return _dec(function)

def checkAuthTimestamp(timestamp):
    current_time = getCurrentTime()
    return ((current_time - timestamp).days == 0 and (current_time - timestamp).seconds < AUTH_EXPIRY_MINS*60)

def getRequestUser(request):
    user = None
    if 'wauth' in request.COOKIES :
        wauth = request.COOKIES['wauth']
        try:
            obj = authToken.objects.get(wauth=wauth)
            user = obj.user     
        except authToken.DoesNotExist:
            try:
                obj = authToken.objects.get(pwauth=wauth)
                user = obj.user 
            except authToken.DoesNotExist:
                pass
    return user

def getVerificationToken(u,ty):
    if ty == 'ev' or ty == 'pr':
        try:
            vc = verificationCode.objects.get(user= u,ctype=ty)
        except verificationCode.DoesNotExist:
            code = randomString(6)
            token = randomString(50)
            vc = verificationCode.objects.create(code = code,user= u,token=token,ctype=ty)
        return vc
    else:
        raise ValueError