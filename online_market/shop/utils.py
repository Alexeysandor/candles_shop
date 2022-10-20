from django.core.paginator import Paginator


def paginator(list, number_of_posts):
    paginator = Paginator(list, number_of_posts)
    return paginator
