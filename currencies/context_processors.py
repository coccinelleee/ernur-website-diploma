from .models import Currency

def currencies(request):
    return {
        'currencies': Currency.objects.all()
    }
