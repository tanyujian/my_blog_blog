from django.core.paginator import Paginator
from django.db.models import Count
from .models import BlogType,Blog

def get_classify(request,blog_data):
    content = {}
    dates = {}

    blog_num = request.GET.get("page",1)  # 得到当前页的网址
    paginator = Paginator(blog_data, 10)  # 对数据进行分页
    num = paginator.get_page(blog_num)  # 对当前页分配内容
    blog_page = list(range(max(num.number - 2, 1), min(num.number + 2, paginator.num_pages + 1)))
    if blog_page[0] - 2 - 1 >= 0:
        blog_page.insert(0, "...")
    if paginator.num_pages - num.number - 2 > 0:
        blog_page.append("...")
    if blog_page[0] != 1:
        blog_page.insert(0, 1)
    if blog_page[-1] != paginator.num_pages:
        blog_page.append(paginator.num_pages)
    # 按类别分类
    classify = BlogType.objects.annotate(blog_count=Count("blog"))
    # 日期分类
    blog_date = Blog.objects.dates("blog_date", "month", order="DESC")
    for date in blog_date:
        dates[date] = Blog.objects.filter(blog_date__year=date.year, blog_date__month=date.month).count()

    content["num"] = num
    content["classify"] = classify
    content["date"] = dates
    content["blog_page"] = blog_page
    return content

