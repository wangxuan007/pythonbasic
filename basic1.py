AOP
Python中如何在一个函数中加入多个装饰器?

怎么做才能让一个函数同时用两个装饰器,像下面这样:

@makebold
@makeitalic
def say():
   return "Hello"
我希望得到

<b><i>Hello</i></b>
我只是想知道装饰器怎么工作的!

去看看文档,答在下面:

def makebold(fn):
    def wrapped():
        return "<b>" + fn() + "</b>"
    return wrapped

def makeitalic(fn):
    def wrapped():
        return "<i>" + fn() + "</i>"
    return wrapped

@makebold
@makeitalic
def hello():
    return "hello world"

print hello() ## returns <b><i>hello world</i></b>
Answer:2

如果你不想看详细的解释的话请看上面那个答案.

装饰器基础

Python的函数都是对象

要了解装饰器,你必须了解Python中的函数都是对象.这个意义非常重要.让我们看看一个简单例子:

def shout(word="yes"):
    return word.capitalize()+"!"

print shout()
# 输出 : 'Yes!'

# 作为一个对象,你可以把它赋值给任何变量

scream = shout

# 注意啦我们没有加括号,我们并不是调用这个函数,我们只是把函数"shout"放在了变量"scream"里.
# 也就是说我们可以通过"scream"调用"shout":

print scream()
# 输出 : 'Yes!'

# 你可以删除旧名"shout",而且"scream"依然指向函数

del shout
try:
    print shout()
except NameError, e:
    print e
    #输出: "name 'shout' is not defined"

print scream()
# 输出: 'Yes!'
好了,先记住上面的,一会还会用到.

Python函数另一个有趣的特性就是你可以在一个函数里定义另一个函数!

def talk():

    # 你可以在"talk"里定义另一个函数 ...
    def whisper(word="yes"):
        return word.lower()+"..."

    # 让我们用用它!

    print whisper()

# 每次调用"talk"时都会定义一次"whisper",然后"talk"会调用"whisper"
talk()
# 输出:
# "yes..."

# 但是在"talk"意外"whisper"是不存在的:

try:
    print whisper()
except NameError, e:
    print e
    #输出 : "name 'whisper' is not defined"*
函数引用

好,终于到了有趣的地方了...

已经知道函数就是对象.因此,对象:

可以赋值给一个变量
可以在其他函数里定义
这就意味着函数可以返回另一个函数.来看看!☺

def getTalk(kind="shout"):

    # 在函数里定义一个函数
    def shout(word="yes"):
        return word.capitalize()+"!"

    def whisper(word="yes") :
        return word.lower()+"...";

    # 返回一个函数
    if kind == "shout":
        # 这里不用"()",我们不是要调用函数
        # 只是返回函数对象
        return shout
    else:
        return whisper

# 怎么用这个特性呢?

# 把函数赋值给变量
talk = getTalk()

# 可以看到"talk"是一个函数对象
print talk
# 输出 : <function shout at 0xb7ea817c>

# 函数返回的是对象:
print talk()
# 输出 : Yes!

# 不嫌麻烦你也可以这么用
print getTalk("whisper")()
# 输出 : yes...
既然可以return一个函数, 你也可以在把函数作为参数传递:

def doSomethingBefore(func):
    print "I do something before then I call the function you gave me"
    print func()

doSomethingBefore(scream)
# 输出:
#I do something before then I call the function you gave me
#Yes!
学习装饰器的基本知识都在上面了.装饰器就是"wrappers",它可以让你在你装饰函数之前或之后执行程序,而不用修改函数本身.

自己动手实现装饰器

怎么样自己做呢:

# 装饰器就是把其他函数作为参数的函数
def my_shiny_new_decorator(a_function_to_decorate):

    # 在函数里面,装饰器在运行中定义函数: 包装.
    # 这个函数将被包装在原始函数的外面,所以可以在原始函数之前和之后执行其他代码..
    def the_wrapper_around_the_original_function():

        # 把要在原始函数被调用前的代码放在这里
        print "Before the function runs"

        # 调用原始函数(用括号)
        a_function_to_decorate()

        # 把要在原始函数调用后的代码放在这里
        print "After the function runs"

    # 在这里"a_function_to_decorate" 函数永远不会被执行
    # 在这里返回刚才包装过的函数
    # 在包装函数里包含要在原始函数前后执行的代码.
    return the_wrapper_around_the_original_function

# 加入你建了个函数,不想修改了
def a_stand_alone_function():
    print "I am a stand alone function, don't you dare modify me"

a_stand_alone_function()
#输出: I am a stand alone function, don't you dare modify me

# 现在,你可以装饰它来增加它的功能
# 把它传递给装饰器,它就会返回一个被包装过的函数.

a_stand_alone_function_decorated = my_shiny_new_decorator(a_stand_alone_function)
a_stand_alone_function_decorated()
#输出s:
#Before the function runs
#I am a stand alone function, don't you dare modify me
#After the function runs
现在,你或许每次都想用a_stand_alone_function_decorated代替a_stand_alone_function,很简单,只需要用my_shiny_new_decorator返回的函数重写a_stand_alone_function:

a_stand_alone_function = my_shiny_new_decorator(a_stand_alone_function)
a_stand_alone_function()
#输出:
#Before the function runs
#I am a stand alone function, don't you dare modify me
#After the function runs

# 想到了吗,这就是装饰器干的事!
让我们看看装饰器的真实面纱

用上一个例子,看看装饰器的语法:

@my_shiny_new_decorator
def another_stand_alone_function():
    print "Leave me alone"

another_stand_alone_function()
#输出:
#Before the function runs
#Leave me alone
#After the function runs
就这么简单.@decorator就是下面的简写:

another_stand_alone_function = my_shiny_new_decorator(another_stand_alone_function)
装饰器就是 decorator design pattern的pythonic的变种.在Python中有许多经典的设计模式来满足开发者.

当然,你也可以自己写装饰器:

def bread(func):
    def wrapper():
        print "</''''''\>"
        func()
        print "<\______/>"
    return wrapper

def ingredients(func):
    def wrapper():
        print "#tomatoes#"
        func()
        print "~salad~"
    return wrapper

def sandwich(food="--ham--"):
    print food

sandwich()
#outputs: --ham--
sandwich = bread(ingredients(sandwich))
sandwich()
#outputs:
#</''''''\>
# #tomatoes#
# --ham--
# ~salad~
#<\______/>
用Python装饰器语法糖:

@bread
@ingredients
def sandwich(food="--ham--"):
    print food

sandwich()
#outputs:
#</''''''\>
# #tomatoes#
# --ham--
# ~salad~
#<\______/>
改变一下顺序:

@ingredients
@bread
def strange_sandwich(food="--ham--"):
    print food

strange_sandwich()
#outputs:
##tomatoes#
#</''''''\>
# --ham--
#<\______/>
# ~salad~
现在:回答你的问题...

作为结论,相信你现在已经知道答案了:

# 字体变粗装饰器
def makebold(fn):
    # 装饰器将返回新的函数
    def wrapper():
        # 在之前或者之后插入新的代码
        return "<b>" + fn() + "</b>"
    return wrapper

# 斜体装饰器
def makeitalic(fn):
    # 装饰器将返回新的函数
    def wrapper():
        # 在之前或者之后插入新的代码
        return "<i>" + fn() + "</i>"
    return wrapper

@makebold
@makeitalic
def say():
    return "hello"

print say()
#输出: <b><i>hello</i></b>

# 这相当于
def say():
    return "hello"
say = makebold(makeitalic(say))

print say()
#输出: <b><i>hello</i></b>
别轻松太早,看看下面的高级用法

装饰器高级用法

在装饰器函数里传入参数

# 这不是什么黑魔法,你只需要让包装器传递参数:

def a_decorator_passing_arguments(function_to_decorate):
    def a_wrapper_accepting_arguments(arg1, arg2):
        print "I got args! Look:", arg1, arg2
        function_to_decorate(arg1, arg2)
    return a_wrapper_accepting_arguments

# 当你调用装饰器返回的函数时,也就调用了包装器,把参数传入包装器里,
# 它将把参数传递给被装饰的函数里.

@a_decorator_passing_arguments
def print_full_name(first_name, last_name):
    print "My name is", first_name, last_name

print_full_name("Peter", "Venkman")
# 输出:
#I got args! Look: Peter Venkman
#My name is Peter Venkman
装饰方法

在Python里方法和函数几乎一样.唯一的区别就是方法的第一个参数是一个当前对象的(self)

也就是说你可以用同样的方式来装饰方法!只要记得把self加进去:

def method_friendly_decorator(method_to_decorate):
    def wrapper(self, lie):
        lie = lie - 3 # 女性福音 :-)
        return method_to_decorate(self, lie)
    return wrapper


class Lucy(object):

    def __init__(self):
        self.age = 32

    @method_friendly_decorator
    def sayYourAge(self, lie):
        print "I am %s, what did you think?" % (self.age + lie)

l = Lucy()
l.sayYourAge(-3)
#输出: I am 26, what did you think?
如果你想造一个更通用的可以同时满足方法和函数的装饰器,用*args,**kwargs就可以了

def a_decorator_passing_arbitrary_arguments(function_to_decorate):
    # 包装器接受所有参数
    def a_wrapper_accepting_arbitrary_arguments(*args, **kwargs):
        print "Do I have args?:"
        print args
        print kwargs
        # 现在把*args,**kwargs解包
        # 如果你不明白什么是解包的话,请查阅:
        # http://www.saltycrane.com/blog/2008/01/how-to-use-args-and-kwargs-in-python/
        function_to_decorate(*args, **kwargs)
    return a_wrapper_accepting_arbitrary_arguments

@a_decorator_passing_arbitrary_arguments
def function_with_no_argument():
    print "Python is cool, no argument here."

function_with_no_argument()
#输出
#Do I have args?:
#()
#{}
#Python is cool, no argument here.

@a_decorator_passing_arbitrary_arguments
def function_with_arguments(a, b, c):
    print a, b, c

function_with_arguments(1,2,3)
#输出
#Do I have args?:
#(1, 2, 3)
#{}
#1 2 3

@a_decorator_passing_arbitrary_arguments
def function_with_named_arguments(a, b, c, platypus="Why not ?"):
    print "Do %s, %s and %s like platypus? %s" %\
    (a, b, c, platypus)

function_with_named_arguments("Bill", "Linus", "Steve", platypus="Indeed!")
#输出
#Do I have args ? :
#('Bill', 'Linus', 'Steve')
#{'platypus': 'Indeed!'}
#Do Bill, Linus and Steve like platypus? Indeed!

class Mary(object):

    def __init__(self):
        self.age = 31

    @a_decorator_passing_arbitrary_arguments
    def sayYourAge(self, lie=-3): # 可以加入一个默认值
        print "I am %s, what did you think ?" % (self.age + lie)

m = Mary()
m.sayYourAge()
#输出
# Do I have args?:
#(<__main__.Mary object at 0xb7d303ac>,)
#{}
#I am 28, what did you think?
把参数传递给装饰器

好了,如何把参数传递给装饰器自己?

因为装饰器必须接收一个函数当做参数,所以有点麻烦.好吧,你不可以直接把被装饰函数的参数传递给装饰器.

在我们考虑这个问题时,让我们重新回顾下:

# 装饰器就是一个'平常不过'的函数
def my_decorator(func):
    print "I am an ordinary function"
    def wrapper():
        print "I am function returned by the decorator"
        func()
    return wrapper

# 因此你可以不用"@"也可以调用他

def lazy_function():
    print "zzzzzzzz"

decorated_function = my_decorator(lazy_function)
#输出: I am an ordinary function

# 之所以输出 "I am an ordinary function"是因为你调用了函数,
# 并非什么魔法.

@my_decorator
def lazy_function():
    print "zzzzzzzz"

#输出: I am an ordinary function
看见了吗,和"my_decorator"一样只是被调用.所以当你用@my_decorator你只是告诉Python去掉用被变量my_decorator标记的函数.

这非常重要!你的标记能直接指向装饰器.

让我们做点邪恶的事.☺

def decorator_maker():

    print "I make decorators! I am executed only once: "+\
          "when you make me create a decorator."

    def my_decorator(func):

        print "I am a decorator! I am executed only when you decorate a function."

        def wrapped():
            print ("I am the wrapper around the decorated function. "
                  "I am called when you call the decorated function. "
                  "As the wrapper, I return the RESULT of the decorated function.")
            return func()

        print "As the decorator, I return the wrapped function."

        return wrapped

    print "As a decorator maker, I return a decorator"
    return my_decorator

# 让我们建一个装饰器.它只是一个新函数.
new_decorator = decorator_maker()
#输出:
#I make decorators! I am executed only once: when you make me create a decorator.
#As a decorator maker, I return a decorator

# 下面来装饰一个函数

def decorated_function():
    print "I am the decorated function."

decorated_function = new_decorator(decorated_function)
#输出:
#I am a decorator! I am executed only when you decorate a function.
#As the decorator, I return the wrapped function

# Let’s call the function:
decorated_function()
#输出:
#I am the wrapper around the decorated function. I am called when you call the decorated function.
#As the wrapper, I return the RESULT of the decorated function.
#I am the decorated function.
一点都不难把.

下面让我们去掉所有可恶的中间变量:

def decorated_function():
    print "I am the decorated function."
decorated_function = decorator_maker()(decorated_function)
#输出:
#I make decorators! I am executed only once: when you make me create a decorator.
#As a decorator maker, I return a decorator
#I am a decorator! I am executed only when you decorate a function.
#As the decorator, I return the wrapped function.

# 最后:
decorated_function()
#输出:
#I am the wrapper around the decorated function. I am called when you call the decorated function.
#As the wrapper, I return the RESULT of the decorated function.
#I am the decorated function.
让我们简化一下:

@decorator_maker()
def decorated_function():
    print "I am the decorated function."
#输出:
#I make decorators! I am executed only once: when you make me create a decorator.
#As a decorator maker, I return a decorator
#I am a decorator! I am executed only when you decorate a function.
#As the decorator, I return the wrapped function.

#最终:
decorated_function()
#输出:
#I am the wrapper around the decorated function. I am called when you call the decorated function.
#As the wrapper, I return the RESULT of the decorated function.
#I am the decorated function.
看到了吗?我们用一个函数调用"@"语法!:-)

所以让我们回到装饰器的.如果我们在函数运行过程中动态生成装饰器,我们是不是可以把参数传递给函数?

def decorator_maker_with_arguments(decorator_arg1, decorator_arg2):

    print "I make decorators! And I accept arguments:", decorator_arg1, decorator_arg2

    def my_decorator(func):
        # 这里传递参数的能力是借鉴了 closures.
        # 如果对closures感到困惑可以看看下面这个:
        # http://stackoverflow.com/questions/13857/can-you-explain-closures-as-they-relate-to-python
        print "I am the decorator. Somehow you passed me arguments:", decorator_arg1, decorator_arg2

        # 不要忘了装饰器参数和函数参数!
        def wrapped(function_arg1, function_arg2) :
            print ("I am the wrapper around the decorated function.\n"
                  "I can access all the variables\n"
                  "\t- from the decorator: {0} {1}\n"
                  "\t- from the function call: {2} {3}\n"
                  "Then I can pass them to the decorated function"
                  .format(decorator_arg1, decorator_arg2,
                          function_arg1, function_arg2))
            return func(function_arg1, function_arg2)

        return wrapped

    return my_decorator

@decorator_maker_with_arguments("Leonard", "Sheldon")
def decorated_function_with_arguments(function_arg1, function_arg2):
    print ("I am the decorated function and only knows about my arguments: {0}"
           " {1}".format(function_arg1, function_arg2))

decorated_function_with_arguments("Rajesh", "Howard")
#输出:
#I make decorators! And I accept arguments: Leonard Sheldon
#I am the decorator. Somehow you passed me arguments: Leonard Sheldon
#I am the wrapper around the decorated function.
#I can access all the variables
#   - from the decorator: Leonard Sheldon
#   - from the function call: Rajesh Howard
#Then I can pass them to the decorated function
#I am the decorated function and only knows about my arguments: Rajesh Howard
好了,上面就是带参数的装饰器.参数可以设置成变量:

c1 = "Penny"
c2 = "Leslie"

@decorator_maker_with_arguments("Leonard", c1)
def decorated_function_with_arguments(function_arg1, function_arg2):
    print ("I am the decorated function and only knows about my arguments:"
           " {0} {1}".format(function_arg1, function_arg2))

decorated_function_with_arguments(c2, "Howard")
#输出:
#I make decorators! And I accept arguments: Leonard Penny
#I am the decorator. Somehow you passed me arguments: Leonard Penny
#I am the wrapper around the decorated function.
#I can access all the variables
#   - from the decorator: Leonard Penny
#   - from the function call: Leslie Howard
#Then I can pass them to the decorated function
#I am the decorated function and only knows about my arguments: Leslie Howard
你可以用这个小技巧把任何函数的参数传递给装饰器.如果你愿意还可以用*args,**kwargs.但是一定要记住了装饰器只能被调用一次.当Python载入脚本后,你不可以动态的设置参数了.当你运行import x,函数已经被装饰,所以你什么都不能动了.

来练习一下:装饰装饰器

好吧,作为奖励,我就给你讲讲如何怎么让所有的装饰器接收任何参数.为了接收参数,我们用另外的函数来建我们的装饰器.

我们包装装饰器.

还有什么我们可以看到吗?

对了,装饰器!

让我们来为装饰器一个装饰器:

def decorator_with_args(decorator_to_enhance):
    """
    这个函数将被用来作为装饰器.
    它必须去装饰要成为装饰器的函数.
    休息一下.
    它将允许所有的装饰器可以接收任意数量的参数,所以以后你不必为每次都要做这个头疼了.
    saving you the headache to remember how to do that every time.
    """

    # 我们用传递参数的同样技巧.
    def decorator_maker(*args, **kwargs):

        # 我们动态的建立一个只接收一个函数的装饰器,
        # 但是他能接收来自maker的参数
        def decorator_wrapper(func):

            # 最后我们返回原始的装饰器,毕竟它只是'平常'的函数
            # 唯一的陷阱:装饰器必须有这个特殊的,否则将不会奏效.
            return decorator_to_enhance(func, *args, **kwargs)

        return decorator_wrapper
下面是如何用它们:

# 下面的函数是你建来当装饰器用的,然后把装饰器加到上面:-)
# 不要忘了这个 "decorator(func, *args, **kwargs)"
@decorator_with_args
def decorated_decorator(func, *args, **kwargs):
    def wrapper(function_arg1, function_arg2):
        print "Decorated with", args, kwargs
        return func(function_arg1, function_arg2)
    return wrapper

# 现在你用你自己的装饰装饰器来装饰你的函数(汗~~~)

@decorated_decorator(42, 404, 1024)
def decorated_function(function_arg1, function_arg2):
    print "Hello", function_arg1, function_arg2

decorated_function("Universe and", "everything")
#输出:
#Decorated with (42, 404, 1024) {}
#Hello Universe and everything

# Whoooot!
估计你看到这和你刚看完爱因斯坦相对论差不多,但是现在如果明白怎么用就好多了吧.

最好的练习:装饰器

装饰器是Python2.4里引进的,所以确保你的Python解析器的版本>=2.4
装饰器使函数调用变慢了.一定要记住.
装饰器不能被取消(有些人把装饰器做成可以移除的但是没有人会用)所以一旦一个函数被装饰了.所有的代码都会被装饰.
用装饰器装饰函数将会很难debug(在>=2.5版本将会有所改善;看下面)
functools模块在2.5被引进.它包含了一个functools.wraps()函数,可以复制装饰器函数的名字,模块和文档给它的包装器.

(事实上:functools.wraps()是一个装饰器!☺)

#为了debug,堆栈跟踪将会返回函数的 __name__
def foo():
    print "foo"

print foo.__name__
#输出: foo

# 如果加上装饰器,将变得有点复杂
def bar(func):
    def wrapper():
        print "bar"
        return func()
    return wrapper

@bar
def foo():
    print "foo"

print foo.__name__
#输出: wrapper

# "functools" 将有所帮助

import functools

def bar(func):
    # 我们所说的"wrapper",正在包装 "func",
    # 好戏开始了
    @functools.wraps(func)
    def wrapper():
        print "bar"
        return func()
    return wrapper

@bar
def foo():
    print "foo"

print foo.__name__
#输出: foo
怎么使用装饰器?

现在遇到了大问题:我们用装饰器干什么?

看起来很黄很暴力,但是如果有实际用途就更好了.好了这里有1000个用途.传统的用法就是用它来为外部的库的函数(你不能修改的)做扩展,或者debug(你不想修改它,因为它是暂时的).

你也可以用DRY的方法去扩展一些函数,像:

def benchmark(func):
    """
    A decorator that prints the time a function takes
    to execute.
    """
    import time
    def wrapper(*args, **kwargs):
        t = time.clock()
        res = func(*args, **kwargs)
        print func.__name__, time.clock()-t
        return res
    return wrapper


def logging(func):
    """
    A decorator that logs the activity of the script.
    (it actually just prints it, but it could be logging!)
    """
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        print func.__name__, args, kwargs
        return res
    return wrapper


def counter(func):
    """
    A decorator that counts and prints the number of times a function has been executed
    """
    def wrapper(*args, **kwargs):
        wrapper.count = wrapper.count + 1
        res = func(*args, **kwargs)
        print "{0} has been used: {1}x".format(func.__name__, wrapper.count)
        return res
    wrapper.count = 0
    return wrapper

@counter
@benchmark
@logging
def reverse_string(string):
    return str(reversed(string))

print reverse_string("Able was I ere I saw Elba")
print reverse_string("A man, a plan, a canoe, pasta, heros, rajahs, a coloratura, maps, snipe, percale, macaroni, a gag, a banana bag, a tan, a tag, a banana bag again (or a camel), a crepe, pins, Spam, a rut, a Rolo, cash, a jar, sore hats, a peon, a canal: Panama!")

#输出:
#reverse_string ('Able was I ere I saw Elba',) {}
#wrapper 0.0
#wrapper has been used: 1x
#ablE was I ere I saw elbA
#reverse_string ('A man, a plan, a canoe, pasta, heros, rajahs, a coloratura, maps, snipe, percale, macaroni, a gag, a banana bag, a tan, a tag, a banana bag again (or a camel), a crepe, pins, Spam, a rut, a Rolo, cash, a jar, sore hats, a peon, a canal: Panama!',) {}
#wrapper 0.0
#wrapper has been used: 2x
#!amanaP :lanac a ,noep a ,stah eros ,raj a ,hsac ,oloR a ,tur a ,mapS ,snip ,eperc a ,)lemac a ro( niaga gab ananab a ,gat a ,nat a ,gab ananab a ,gag a ,inoracam ,elacrep ,epins ,spam ,arutaroloc a ,shajar ,soreh ,atsap ,eonac a ,nalp a ,nam A
当然,装饰器的好处就是你可以用它们来做任何事而不用重写,DRY:

@counter
@benchmark
@logging
def get_random_futurama_quote():
    from urllib import urlopen
    result = urlopen("http://subfusion.net/cgi-bin/quote.pl?quote=futurama").read()
    try:
        value = result.split("<br><b><hr><br>")[1].split("<br><br><hr>")[0]
        return value.strip()
    except:
        return "No, I'm ... doesn't!"


print get_random_futurama_quote()
print get_random_futurama_quote()

#输出:
#get_random_futurama_quote () {}
#wrapper 0.02
#wrapper has been used: 1x
#The laws of science be a harsh mistress.
#get_random_futurama_quote () {}
#wrapper 0.01
#wrapper has been used: 2x
#Curse you, merciful Poseidon!
Python自身提供了几个装饰器,像property, staticmethod.

Django用装饰器管理缓存和试图的权限.
Twisted用来修改异步函数的调用.
好大的坑!
