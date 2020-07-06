from allauth.account.views import SignupView
from allauth.account.forms import SignupForm
from captcha.fields import ReCaptchaField

class EguideSignupForm(SignupForm):
    captcha = ReCaptchaField()
    
class EguideSignupView(SignupView):
    form_class = EguideSignupForm