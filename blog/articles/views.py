#from models import Article
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import Http404
from articles.models import Article

def archive(request):
    return render(request, 'archive.html', {"posts": Article.objects.all()}) 

def get_article(request, article_id):
    try:
        post = Article.objects.get(id=article_id)
        return render(request, 'article.html', {"post": post})
    except Article.DoesNotExist:
        raise Http404

def create_post(request):
    if not request.user.is_anonymous():
        if request.method == 'POST':
            form = {
                'text': request.POST['text'],
                'title': request.POST['title']
            }
            if form['text'] and form['title']:
                try:
                    Article.objects.get(title=form['title'])
                    form['errors'] = u'There is already a topic with the same name'
                    return render(request, 'create_post.html', {'form': form})
                except:
                    pass
                Article.objects.create(text=form['text'],
                                       title=form['title'],
                                       author=request.user)
                article = Article.objects.get(title=form['title'])
                return redirect('get_article', article_id=article.id)
            else:
                form['errors'] = u'Not all the columns are filled'
                return render(request, 'create_post.html', {'form': form})
        else:
            return render(request, 'create_post.html', {})
 
    else:
        raise Http404

