from django import template

register = template.Library()


@register.inclusion_tag('paginator/pagination.html', takes_context=True)
def paginator(context, page_obj=None, paginator=None, adjacent=3,
              per_page_choices=None):
    """
    Renders pagination links for `page` object. Shows up to `pages` page links,
    with at least `adjacent` visible links on each side of the current page
    """
    if page_obj is None:
        page_obj = context.get('page_obj')

    if paginator is None:
        paginator = context.get('paginator')

    if page_obj is None:
        raise template.TemplateSyntaxError(
            "A `page_obj` variable must be present in the template context or "
            "passed explicitly to the template tag, eg: "
            "`{% paginator page_obj=my_page_obj %}`."
        )

    if paginator is None:
        raise template.TemplateSyntaxError(
            "A `paginator` variable must be present in the template context "
            "or passed explicitly to the template tag, eg: "
            "`{% paginator paginator=my_paginator %}`."
        )

    if per_page_choices is None:
        per_page_choices = context.get('per_page_choices')

    if hasattr(per_page_choices, 'split'):
        try:
            per_page_choices = (int(i) for i in per_page_choices.split(','))
        except TypeError:
            raise template.TemplateSyntaxError(
                "`per_page_choices` must consist of only integers seprated "
                "by commas.")

    if per_page_choices:
        per_page_choices = map(str, per_page_choices)

    num_pages = paginator.num_pages
    if num_pages <= 1:
        return {'hide': True}

    # show PAGE with Adj on each side, plus first and last
    # If adj is 3, we show 3*2 + 3 = 9 pages

    page_var = getattr(page_obj, 'page_var', 'page')

    l_elipse = r_elipse = False
    size = adjacent * 2 + 1
    start = max(page_obj.number - adjacent, 2)
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

    qs = ''
    request = context.get('request')
    if request:
        get = request.GET.copy()
        if get.get(page_var):
            del get[page_var]
        current_qs = get.urlencode()
        if current_qs:
            qs = '{}&'.format(current_qs)

    return {
        'l_elipse': l_elipse,
        'r_elipse': r_elipse,
        'per_page': paginator.per_page,
        'per_page_choices': context.get('per_page_choices', per_page_choices),
        'page_var': page_var,
        'page_obj': page_obj,
        'paginator': paginator,
        'page_numbers': page_numbers,
        'show_first': 1 not in page_numbers,
        'show_last': num_pages not in page_numbers,
        'qs': qs,
    }
