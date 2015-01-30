from django import template

register = template.Library()


@register.inclusion_tag('paginator/pagination.html', takes_context=True)
def paginator(context, page, adjacent=3):
    """
    Renders pagination links for `page` object. Shows up to `pages` page links,
    with at least `adjacent` visible links on each side of the current page
    """
    if not hasattr(page, 'paginator'):
        return {'hide': True}
    paginator = page.paginator
    num_pages = paginator.num_pages
    if num_pages <= 1:
        return {'hide': True}

    # show PAGE with Adj on each side, plus first and last
    # If adj is 3, we show 3*2 + 3 = 9 pages

    page_var = getattr(page, 'page_var', 'p')

    l_elipse = r_elipse = False
    size = adjacent * 2 + 1
    start = max(page.number - adjacent, 2)
    end = start + size - 1

    if end > num_pages - 1:
        end = num_pages - 1
        start = num_pages - size

    if start > 2 and num_pages > size:
        l_elipse = True
    else:
        start = max(start - 1, 2)
        end = min(start + size, num_pages - 1)

    if end < num_pages - 2 and num_pages > size:
        r_elipse = True
    else:
        end = min(end + 1, num_pages - 1)
        start = max(end - size, 2)

    page_numbers = range(start, end + 1)

    request = context['request']
    get = request.GET.copy()
    if get.get(page_var):
        del get[page_var]
    current_qs = get.urlencode()
    qs = ''
    if current_qs:
        qs = '{}&'.format(current_qs)

    count_choices = context.get('count_choices', (10, 25, 50, 100))
    count_choices = map(str, count_choices)

    return {
        'l_elipse': l_elipse,
        'r_elipse': r_elipse,
        'count': request.GET.get('count', None),
        'count_choices': context.get('count_choices', count_choices),
        'page_var': page_var,
        'page': page,
        'paginator': paginator,
        'page_numbers': page_numbers,
        'show_first': 1 not in page_numbers,
        'show_last': num_pages not in page_numbers,
        'qs': qs,
    }
