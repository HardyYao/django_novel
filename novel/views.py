from django.shortcuts import render
from django.http import HttpResponse
from novel.models import NovelCopy, ChapterCopy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def index(request):
    novelcopys = NovelCopy.objects.filter().order_by('?')[:4]
    hotnovelcopys = NovelCopy.objects.filter().order_by('novelid')[:5]
    xuanhuannovels = NovelCopy.objects.filter(sort="玄幻").order_by('?')[:6]
    wuxianovels = NovelCopy.objects.filter(sort="武侠").order_by('?')[:6]
    context = {'novelcopys': novelcopys, 'xuanhuannovels': xuanhuannovels,
               'wuxianovels': wuxianovels, 'hotnovelcopys': hotnovelcopys}
    return render(request, 'index.html', context)

def detail(request, novelid):
    chaptercopys = ChapterCopy.objects.filter(novelid=novelid)
    novelcopy = NovelCopy.objects.get(novelid=novelid)
    context = {'chaptercopys': chaptercopys, 'novelcopy': novelcopy}
    return render(request, 'detail.html', context)

def chapter(request, chapterid):
    chaptertitle = ChapterCopy.objects.get(chapterid=chapterid) # ChapterCopy Object
    chapters = ChapterCopy.objects.filter(novelid=chaptertitle.novelid) # QuerySet
    nextchapter = int(chapterid) + 1
    lastchapter = int(chapterid) - 1
    if lastchapter == 0:
        lastchapter = 1
    # 获取当前ChapterCopy的Queryset，并提取novelid的值（一个tuple），这里novelid都是一样的，取一个即可
    chapter_query = chapters.values_list('novelid')[0]
    thenovelid = chapter_query[0]     #提取tuple中的数值，即小说的id
    thenovelname = NovelCopy.objects.get(novelid=thenovelid)
    context = {'chaptertitle': chaptertitle,'chapters': chapters, 'thenovelid': thenovelid,
               'lastchapter': lastchapter, 'nextchapter': nextchapter, 'thenovelname': thenovelname}
    return render(request, 'chapter.html', context)

def more(request, type, page):
    novellists = NovelCopy.objects.filter(type=type).order_by('novelid')  # QuerySet
    sortquery = list(novellists.values_list('sort')[0])
    novelsort = sortquery[0]
    typequery = list(novellists.values_list('type')[0])
    noveltype = typequery[0]
    paginator = Paginator(novellists, 20)   # Show 10 novels per page
    try:
        novels = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        novels = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        novels = paginator.page(paginator.num_pages)

    context = {'novellists': novellists, 'novels': novels,
               'novelsort': novelsort, 'noveltype': noveltype }
    return render(request, 'more.html', context)

def search(request):
    novelname = request.GET.get('kw')   # 获取所要搜索的小说名
    searchnovels = NovelCopy.objects.filter(novelname=novelname)    # 从数据库中查找小说
    random_recommends = NovelCopy.objects.filter().order_by('?')[:6]    # 随机抽取6本小说
    context = {'novelname': novelname, 'searchnovels': searchnovels,
               'random_recommends': random_recommends}
    return render(request, 'search.html', context)