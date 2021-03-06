from django.db import models

# 模型层 Model
#    为了避免模型层臃肿，复杂业务请放在Service层(views.py)
#
# 关系例图：
#    [实体]       一 -> 一              | 且，和，同时
#    {弱实体}     一 => 多               & 连接(若干个关系式)
#    <关系>      (箭头反向时为反向查询set)
#


# [用户] =>{用户标签} & <=[问题]|[答案]
class User(models.Model):
    uid = models.CharField(max_length=128, primary_key=True, help_text='所依赖的聊天工具平台上用户唯一标识')
    nickname = models.CharField(max_length=64, help_text='昵称')
    name = models.CharField(null=True, blank=True, max_length=64, help_text='实名，或者登录名')
    _GENDER = (
        (0, '未知'),
        (1, '男'),
        (2, '女'),
    )
    gender = models.PositiveSmallIntegerField(blank=True, choices=_GENDER, default=0)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(null=True, blank=True, max_length=11)
    tags = models.ManyToManyField('Tag')

    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.uid

    # 用用户数据字典列表更新数据库的用户信息列表
    @classmethod
    def update_userlist(cls,dict):
        u,created = User.objects.get_or_create(uid=dict['uid'], nickname=dict['nickname'], gender=dict['gender'])
        print(u,created)

# [问题] ->[用户] & =>{问题关键词} & <=[答案]
def keywords_list_cmp(key_1,key_2):
    #key_1 and key_2 are both key words list
    #which came from the function split()
    #return value means the number of words that both appear in key_1 and key_2
    #the value can be zero
    results = 0
    for word_1 in key_1:
        for word_2 in key_2:
            if word_1 == word_2:
                results = results + 1
                break
    return results
# {问题关键词} <=[问题]
class Keyword(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

class Question(models.Model):
    user = models.ForeignKey(User, help_text='题主')
    content = models.TextField(help_text='问题内容')
    keywords = models.ManyToManyField('Keyword', help_text='问题关键字')
    qid = models.AutoField(primary_key=True, help_text='问题ID, 问题的唯一标识')
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '[%s] %s' % (self.user.name, self.content[:10])

    @classmethod
    def find_alike(cls,ques):
        # TODO: 用关键词列表查询已缓存的相似问题返回问题列表，以决定缓存新回答时是否新建问题、遇到问题时取出缓存的备选答案
        # in fact, class answer is defined after class question,we cannot get answer here
        # the return value is the qid
        # qid can be null or false
        keywords=ques['keywords']
        key_list=keywords.split(' ')
        for word in key_list:
            print ("\n key is " + word + "\n")
        try:
            q = Question.objects.filter(keywords__name = keywords)
        except Question.DoesNotExist:
            q = False
        if q:
            if q[0]:
                return q[0].qid
        return False

    @classmethod
    #更新app_question数据库
    def update_questionlist(cls, dist):
        #shall uid is null?
        #if uid cannot be null,comment 'if~~'unknown' '(4 lines) out,and uncomment the line below.
        u = User.objects.get(uid = dist['uid'])
        p,created = Keyword.objects.get_or_create(name = dist['keywords'])
        q,created = Question.objects.get_or_create(user = u,content = dist['question'])
        q.keywords.add(p)
        return q


# [答案] ->[用户]|[问题]
class Answer(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, help_text='答主|为空时意为搜索引擎')
    question = models.ForeignKey(Question, help_text='对应的问题')
    content = models.TextField(help_text='答案内容')
    grade = models.PositiveSmallIntegerField(blank=True, default=3, help_text='评分1-5')
    like = models.PositiveIntegerField(blank=True, default=0, help_text='赞同数')
    dislike = models.PositiveIntegerField(blank=True, default=0, help_text='反对数')

    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '[%s] %s' % (self.user.name, self.content[:10])

    @classmethod
    def update_answerlist(cls, dist):
    #dist { uid,qid,answer }
        try:
            u = User.objects.get(uid = dist['uid'])
            q = Question.objects.get(qid = dist['qid'])
            a, created = Answer.objects.get_or_create(user=u, content=dist['answer'], question=q)
        except:
            print("poinson")

    @classmethod
    def qid_get_ans_con(cls,qid):
    #return the answer's content to the question
    #return value can be null or false ,for the wrong id or someting unexpected
        ans = Answer.objects.get(qid = qid).content
        return ans

# {用户标签} <=[用户]
class Tag(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name




# TODO: 这个表真的有必要吗？
# <发言记录> ->[用户]
class Log(models.Model):
    user = models.ForeignKey(User)
    chat = models.CharField(max_length=1500, help_text='发言内容')

    create_time = models.DateTimeField(auto_now_add=True)
