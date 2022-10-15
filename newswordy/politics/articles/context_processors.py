from .utils import categories

def custom_ctx(request):
    return {
        'categories': [category for category in categories]
    }