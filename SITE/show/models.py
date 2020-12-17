from django.db import models
import pickle
# Create your models here.


class Actor(models.Model):
    name = models.CharField(max_length=30, verbose_name=u"名字", null=True)
    desc = models.CharField(max_length=500, verbose_name=u"人物简介", null=True)
    pic_link = models.CharField(max_length=500, verbose_name=u"照片", null=True)
    otherinfo = models.CharField(max_length=500, verbose_name=u"其他信息", null=True)
    other=models.CharField(max_length=500, verbose_name=u"其他", null=True)

    def __str__(self):
        return self.name

    @staticmethod
    def get_actor():
        filename = "./show/movie.pkl"
        i=0
        with open(filename, 'rb') as f:
            while True:
                try:
                    i=i+1
                    data = pickle.load(f)
                    for actor in data['actorinfo']:
                        if actor!=None:
                            obj, b = Actor.objects.update_or_create(name=actor['name'],desc=actor['description'],
                                                                pic_link=actor['img'],other=list(actor.keys())[3],
                                                                otherinfo=list(actor.values())[3])

                except EOFError:
                    break

    @staticmethod
    def dere():
        filename = "./show/movie.pkl"
        i = 0
        with open(filename, 'rb') as f:
            while True:
                try:
                    i = i + 1
                    data = pickle.load(f)
                    for actor in data['actorinfo']:
                        if actor != None:
                            obj= Actor.objects.filter(name=actor['name'])
                            if len(obj)>1:
                                j=0
                                for a in obj:
                                    j=j+1
                                    if j>1:
                                        a.delete()

                except EOFError:
                    break

class Movie(models.Model):
    title = models.CharField(max_length=30, verbose_name=u"电影标题", null=True)
    desc = models.CharField(max_length=500, verbose_name=u"电影简介", null=True)
    pic_link = models.CharField(max_length=500, verbose_name=u"海报", null=True)
    actors = models.ManyToManyField(Actor, through = "MemberShip")
    director = models.CharField(max_length=500, verbose_name=u"导演", null=True)
    screenwriter = models.CharField(max_length=500, verbose_name=u"编剧", null=True)
    type = models.CharField(max_length=500, verbose_name=u"类型", null=True)
    comment1 = models.CharField(max_length=500, verbose_name=u"短评1", null=True)
    comment2 = models.CharField(max_length=500, verbose_name=u"短评2", null=True)
    comment3 = models.CharField(max_length=500, verbose_name=u"短评3", null=True)
    comment4 = models.CharField(max_length=500, verbose_name=u"短评4", null=True)
    comment5 = models.CharField(max_length=500, verbose_name=u"短评5", null=True)

    def __str__(self):
        return self.title

    @staticmethod
    def get_movie():
        filename = "./show/movie.pkl"
        i=0
        with open(filename, 'rb') as f:
            while True:
                try:
                    i=i+1
                    data = pickle.load(f)
                    m, b = Movie.objects.update_or_create(title=data['title'], desc=data['description'], pic_link=data['img'],
                                                       comment1=data['comments'][0],
                                                       comment2=data['comments'][1],
                                                       comment3=data['comments'][2],
                                                       comment4=data['comments'][3],
                                                       comment5=data['comments'][4])
                    if len(data['director'])!=0:
                        m.director=data['director'][0]
                        m.save()
                    if len(data['screenwriter'])!=0:
                        m.screenwriter=data['screenwriter'][0]
                        m.save()
                    if len(data['type']) != 0:
                        m.type = data['type'][0]
                        m.save()
                except EOFError:
                    break


class MemberShip(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE)

    @staticmethod
    def add_relationship():
        filename = "./show/movie.pkl"
        i = -1
        movie = Movie.objects.all()
        with open(filename, 'rb') as f:
            while True:
                try:
                    i = i + 1
                    data = pickle.load(f)
                    m=movie[i]
                    for ac in data['actorinfo']:
                        if ac != None:
                            a=Actor.objects.filter(name=ac['name'])
                            if len(a)>0:
                                a=a[0]
                                MemberShip.objects.create(movie=m,actor=a)

                except Exception as e:
                    print(e)
                    break




