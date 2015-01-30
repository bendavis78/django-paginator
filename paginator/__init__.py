from django.core.paginator import Paginator, EmptyPage


def paginate(queryset, request, count=10, page_var='p'):
    count = request.GET.get('count', count)
    page = request.GET.get(page_var, 1)
    paginator = Paginator(queryset, count)

    try:
        page = int(page)
    except TypeError:
        page = 1

    try:
        paginated = paginator.page(page)
    except EmptyPage:
        paginated = paginator.page(paginator.num_pages)

    paginated.page_var = page_var
    return paginated
