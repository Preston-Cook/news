from .utils import categories

def custom_ctx(request):
    return {
        'categories': [category.title() for category in categories]
    }