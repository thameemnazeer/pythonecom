from shop.models import Category


def link(request):
    c=Category.objects.all()#retrieves all category records from Table Category
    return {'links':c}