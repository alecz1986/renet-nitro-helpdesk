#
# -*- coding: UTF-8 -*-

import sys
import os
import re
import copy
import urllib
import urlparse
import signal
import time
import datetime
import weakref
from lxml import etree as et
from lxml.builder import E
from lxml.etree import XMLSyntaxError

"""
Структура WEB-формы определяются соввокупностью полей field в структуре
wform на этапе инициализации класса (метаклассовость). Один раз созданное
воплощение класса field можно многократно использовать в конструировании
интерфейса форм, т.к. после создания объект field не должен изменяться.
Удобней всего манипулировать списками значений.

При инициализации для класса field определяются ряд именованных аргументов.
Они могут быть заданы в любом удобном порядке, но рекомендуется придерживаться
общего стиля в рамках данного проекта. Нами предлагается следующий порядок:
    - default: значение по умолчанию;
    - filter_in: функция отфильтровки и-или преобразования в другой тип;
    - accept_in: если при фильтрации получено одно из ожидаемых исключений,
      прерывание работы не последует, а будет взято значение по умолчанию;
    - __удален__: обратный фильтр, используется, если нужно преобразовать,
      значение в текстовое представление для возврата в составе XML документа,
      в виде значения заголовков или иных параметрах HTTP ответа. Возвращаемое
      значение поставляет такое значение, как оно используется для работы с
      текстовыми "input" полями. Объект вида dict используется в зависимости от
      задействованного сценария. Это может быть создание связки
      "select"-"option", "checkbox", "radio" или создание xml элемента, или его
      ирархии. В качестве ключевых слов для приведения данных к требуемому виду
      могут использоваться те же ключевые слова, что используются для
      определения фазы формы. Ключевое слово указывается вторым элементом
      двуэлементного кортежа метода __getitem__. Использование двуэлементного
      кортежа для выбора преобразования по полю можно использовать только для
      метода __getitem__;
    - container: если значение None - принимаются исключительно одиночные
      значения. Наличие более двух воспринимаются ошибкой. Использование
      значения, отличного от None необходимо в случае множественности полей на
      уровне "input", "select" и "textarea" тэгов. Если множественное значение
      задается в одном тэге (например, запись значений через запятую), то
      будет логично задействовать преобразование "filter_in". Возможен и
      комплексный подход;

Экземпляр класса форм может и должен изменяться. Он несет в себе относительно
небольшую логику по получению данных из формы и предлагает интерфейс по
концентрации всех полученных данных от браузера в едином месте. На этот же
класс возложено определение пути поведения, в зависимости от имеющегося набора
полей.

Для веб-сервиса у именнованного поля существует принципиальная возможность
одновременно участвовать в словарях GET, POST, cookies и urlvals (составленного
на основе парсинга URI строки). Однако для безопасности приложения бывает
полезно определить, каким образом должно быть получено то или иное значение.

В итоге по получившемуся набору элементов можно судить, в какой фазе находится
та или иная форма. К примеру данные в форме администратора могут находиться в
виде просмотра, в виде предложения к редактированию, отправка отредактированных
данных с переходом в новое состояние или без перехода, и т.д. Обычно таких фаз
для одной формы не бывает слишком много. Иногда о фазе можно судить по тому,
как были получены эти данные. Но каждый раз проводить полное тестирование
данных формы на соответствие одной из текущих фаз запутывает разработчика.
Отсутствие стилистической проработанности также дает о себе знать.

С фазой формы заодно попытаемся связать допустимость получения данных из словаря
определенного рода. Т.е. если мы доверяем получение данных из словаря POST, и не
доверяем получение из GET (например, объем ожидаемых данных значителен и может
быть усечен в процессе передачи), то одной из фазовых составляющих будет
определена ошибка в методе получения данных. Вероятным видом реакции формы в
описаном случае может быть повторный вывод формы POST с просьбой проверить данные
на полноту именно для указанного поля. Альтернативным методом может быть
запрещение работы с данной формой с выводом описания ошибки. То же может касаться
данных из cookies и urlvars.

Указание на фазовую составляющую задается в виде строки, которая в дальнейшем
разбирается на несколько частей. Синтаксис определяет и порядок просмотра
словарей и возможность их сочетания друг с другом. В самой форме есть типовые
схемы, принадлежность к каждой из которых также может быть заложено в описании
поля. Эти данные дополняют, но не исчерпывают потребность в персонализированныъ
данных.

Данные формы в процессе работы существуют сразу в нескольких воплощениях:
    - webob.Request: самый низщий и грязный уровень;
    - первичные данные, прошедшие обработку в form;
    - данные замещения, после их адаптации для сохранения в базе данных;
    - данные для вывода (не всегда они беруться именно из формы).

Каждый из уровней важен для процесса отладки и в связи с этим они не
должны перемешиваться и затираться.
"""

# XXX: остановило непонятность определения интерфейса для передачи формы в виде.
# Content-Type: application/x-www-form

__all__ = [
    'field',
    'form',
    'template',
    'et',
    'E',
]

nodefault = object()
rx_namecheck = re.compile("^[A-Za-z_][0-9A-Za-z_]*$")

class field(object):
    cls__kwds = ('default', 'filter_in', 'accept_in', 'container', 'autoincrement', 'phases', 'complexity', 'setup')
    _rx = rx_namecheck
    _nodefault = nodefault
    _noop1 = staticmethod(lambda x: x)
    class __metaclass__(type):
        def __new__(cls, cname, cbases, cvars):
            # Наследование не работает в отношении __slots__.
            # Поэтому тупо эмулируем наследование.
            tmp = type.__new__(cls, cname, cbases, cvars)
            if hasattr(tmp, 'cls__kwds'):
                cvars['__slots__'] = ('name',) + tmp.cls__kwds + ('single', 'optional', 'tagging')
            ret = type.__new__(cls, cname, cbases, cvars)
            return ret
    def __init__(self, *args, **kw):
        # Используем слоты
        object.__init__(self)
        cls = self.__class__
        # Имя поля не может быть задано в виде ключевого слова.
        try:
            name = args[0]
        except IndexError:
            sys.exc_clear()
            raise TypeError("in firstly define name of %s()" % (cls.__name__,))
        args = args[1:]
        if len(args) > len(cls.cls__kwds):
            raise TypeError("%s() takes at most %d arguments (%d given)" % (cls.__name__, len(cls.cls__kwds), len(args)))
        for k, v in zip(cls.cls__kwds, args):
            if k in kw:
                raise TypeError("%s() got multiple values for keyword argument '%s'" % (cls.__name__, k))
            kw[k] = v
        # Простенькие проверки для имени переменной
        assert type(name) is str, name
        assert cls._rx.match(name) is not None, name
        # Агрумент определяет значение по умолчанию.
        default = kw.pop('default', cls._nodefault)
        # Функция по фильтрации и трансформации в нужный тип значения данного
        # поля.
        filter_in = kw.pop('filter_in', cls._noop1)
        if type(filter_in) is not str and not hasattr(filter_in, '__call__'):
            raise ValueError("filter_in must be callable or method name")
        # Если функция filter_in произвела ожидаемое исключение, результирующим
        # значением должно стать значение по умолчанию.
        accept_in = kw.pop('accept_in', ())
        try:
            accept_in = tuple(accept_in)
        except TypeError:
            sys.exc_clear()
            accept_in = (accept_in,)
        # Контейнер может быть одиночным (None) или специальной структуры.
        # Принимаются встроенные типы, функции, привязанные методы, лямбды,
        # что возвращало бы контейнер после вызова с единственным аргументом:
        # списком переданных значений. Может быть интегрированна проверка
        # на количество значений.
        container = kw.pop('container', None)
        if container is not None and type(container) is not str and not hasattr(container, '__call__'):
            raise ValueError("container must be callable or method name")
        # Поле требуещее значение None или целого числа > 0
        autoincrement = kw.pop('autoincrement', False)
        assert type(autoincrement) is bool, autoincrement
        if autoincrement:
            assert default is cls._nodefault, default
            assert filter_in is cls._noop1, filter_in
            assert accept_in == (), accept_in
            default = None
            filter_in = self.filter_autoincrement
            accept_in = (ValueError,)
        # XXX: Описание
        phases = kw.pop('phases', 'D/default')
        tagging = []
        for tag in phases.split():
            toks = tag.split('/', 2)
            assert len(toks) == 2, toks
            receive, phase = toks
            assert receive in "MPGCD", toks
            assert cls._rx.match(phase) is not None, toks
            tagging.append((receive, phase))
        # Текстовое поле.
        complexity = kw.pop('complexity', False)
        assert type(complexity) is bool, complexity
        # Функция инициализации формы задействованная в последовательности
        # объявления полей..
        setup = kw.pop('setup', None)
        assert type(setup) is str or setup is None, setup
        # Если задан недопустимый аргумент...
        if kw:
            raise TypeError("%s() got an unexpected keyword arguments: '%s'." % (cls.__name__, "', '".join(kw.keys())))
        self.name = name
        self.default = default
        self.filter_in = filter_in
        self.accept_in = accept_in
        self.container = container
        self.autoincrement = autoincrement
        self.phases = phases
        self.optional = default is not cls._nodefault # Опциональное значение
        self.single = container is None # Одиночное значение
        self.tagging = tagging
        self.complexity = complexity
        self.setup = setup
    @staticmethod
    def filter_autoincrement(x):
        x = int(x)
        if x <= 0:
            x = None
        return x

class form(object):
    """
Получение переменных может вестись многими путями:
    - GET метод;
    - POST метод;
    - cookies;
    - urlvars;

Поскольку идея была заимствована из PHP упомяну еще две разновидности словарей:
    - переменные окружения;
    - встроенное пространство имен.

Их мы не будем использовать по причине того, что переменные не регистрируются
едином пространстве имен.

Здесь нужен единный непротиворечивый инструмент по работе с различными данными,
отправленными пользователем в сторону сервера. Из-за их непохожести следует
оговорить все ньюансы работы с ними.

Так, данные из словарей GET и POST по одному имени могут иметь несколько
значений, притом поддерживается перемешивание данных между словарями из-за
крайней похожести методов определения данных формы.

Данные из Cookie имеют только одно определенное значение по каждой переменной.
Кроме того переменная задается не столько для данной формы, сколько для всего
браузера в целом для заданого пути.

Другие отличия:
 - по Cookie могут прийти "неизвестные" для данной формы значения, которые
   обязаны быть проигнорированны;
 - в общем случае не может быть неизвестных GET или POST переменных, поскольку
   наличие лишнего аргумента подразумевает на внутреннюю нестыковку или на
   хакерскую атаку. Имена переменных, которые генерируются "на лету", создают
   трудности для статического определения. Мною было принято решение ставить
   структуру динамических полей в соответствие с одним из статических полей.
   В этом случае обработчик по заданому полю должен иметь возможность вызова
   после определения своего значения.
 - во избежание ошибок, поля, которые передаются через GET или POST запросы
   не должны различаться своим назначением. Но могут аккумулироваться, если
   ключ представляет из себя контейнер.
"""
    _nodefault = nodefault
    methods = ()
    class __metaclass__(type):
        _rx = rx_namecheck
        def __new__(cls, cname, cbases, cvars):
            ret = type.__new__(cls, cname, cbases, cvars)
            ret.meta_init(cvars)
            if 'fields' in cvars:
                ret.fields = list(ret.fields)
                ret.meta_fields_userlevel()
                ret.meta_fields()
            return ret
    @classmethod
    def meta_init(cls, cvars):
        pass
    @classmethod
    def meta_fields_userlevel(cls):
        pass
    @classmethod
    def meta_fields(cls):
        cls.fields = list(cls.fields)
        # Множество тэгов, фигурирующие в форме.
        tags_valid = set()
        # Соответствие имени группы к множеству тэгов по умолчанию.
        tags_dmap = {}
        for tagname, phases in getattr(cls, 'tags_default', { 'default': 'P/default G/default' }).items():
            tags = []
            # Разбиваем по границе пробелов.
            for tag in phases.split():
                if not tag:
                    # Отсекаем пробелы в начале и в хвосте.
                    continue
                toks = tag.split('/', 1)
                assert len(toks) == 2, toks
                receive, phase = toks
                assert receive in "MPGC", toks
                # Наименование фазы должно быть латиницей.
                assert cls._rx.match(phase) is not None, toks
                tags_valid.add(phase)
                tags.append((receive, phase))
            tags_dmap[tagname] = tags
        fields_seq = []
        fileds_map = {}
        for field in cls.fields:
            assert field.name not in fileds_map, field.name
            fileds_map[field.name] = field
            fields_seq.append(field)
            tagging = {}
            for receive, phase in field.tagging:
                if receive == 'D':
                    if phase not in tags_dmap:
                        raise ValueError("unknown group '%s' of default phases" % (phase,))
                    for receive, phase in tags_dmap[phase]:
                        tagging.setdefault(receive, set()).add(phase)
                else:
                    assert receive in "MPGC", receive
                    tags_valid.add(phase)
                    tagging.setdefault(receive, set()).add(phase)
            tagging = tagging.items()
            tagging.sort()
            field.tagging = tagging
        # Чтобы исключить наследование из базовых классов.
        cls.fileds_map = fileds_map
        cls.fields_seq = fields_seq
        cls.tags_dmap = tags_dmap
        cls.tags_valid = tags_valid
    def __init__(self, template, autorun=True):
        object.__init__(self)
        self.template_ref = weakref.ref(template)
        self.req = template.req
        self.resp = template.resp
        self.environ = template.environ
        self.fields_income = {}
        self.fields_update = {}
        self.tags = None
        for meth in self.methods:
            getattr(self, meth)()
        if autorun:
            self.run()
    def run(self):
        req = self.req
        for field in self.fields_seq:
            if field.setup is not None:
                getattr(self, field.setup)(field)
            ivals = []
            default = field.default
            filter_in = field.filter_in
            if filter_in.__class__ is str:
                filter_in = getattr(self, filter_in)
            accept_in = field.accept_in
            tags = set()
            already = []
            for receive, phases in field.tagging:
                if receive == 'M':
                    if req.method == 'POST':
                        receive = 'P'
                    else:
                        receive = 'G'
                if receive == 'P':
                    inp = req.POST
                elif receive == 'G':
                    inp = req.GET
                elif receive == 'C':
                    inp = req.cookies
                else:
                    raise TypeError("unknown type of dictionary (receive='%s')" % (receive,))
                tags.update(phases)
                if receive in already:
                    continue
                already.append(receive)
                ivalf = inp.getall(field.name)
                for ival in ivalf:
                    # Если нестроковое значение (сложный объект) игнорируем в
                    # зависимости от определения настроек поля.
                    if (type(ival) not in (str, unicode))^field.complexity:
                        continue
                    try:
                        ival = filter_in(ival)
                    except accept_in:
                        sys.exc_clear()
                        ival = default
                    if ival is field._nodefault:
                        continue
                    ivals.append(ival)
            if field.single:
                if len(ivals) == 1:
                    value = ivals[0]
                else:
                    value = default
            else:
                container = field.container
                if container.__class__ is str:
                    container = getattr(self, container)
                value = container(ivals)
            self.fields_income[field.name] = value
    def rollback(self):
        self.fields_update.clear()
    def get(self, item, default=None):
        cls = self.__class__
        if item in self.fields_update:
            ret = self.fields_update.get(item, cls._nodefault)
        else:
            ret = self.fields_income.get(item, cls._nodefault)
        if ret is cls._nodefault:
            return default
        return ret
    def __getitem__(self, item):
        cls = self.__class__
        if item in self.fields_update:
            ret = self.fields_update.get(item, cls._nodefault)
        else:
            ret = self.fields_income.get(item, cls._nodefault)
        if ret is cls._nodefault:
            raise KeyError(item)
        return ret
    def __setitem__(self, item, value):
        self.fields_update[item] = value
    def __delitem__(self, item):
        self.fileds_update[item] = self.__class__._nodefault
    def keys(self):
        return [ field.name for field in self.fields_seq ]
    def __contains__(self, item):
        cls = self.__class__
        if item in self.fields_update:
            ret = self.fields_update.get(item, cls._nodefault)
        else:
            ret = self.fields_income.get(item, cls._nodefault)
        return ret is not cls._nodefault
    def items(self):
        cls = self.__class__
        result = []
        for field in self.fields_seq:
            item = field.name
            if item in self.fields_update:
                ret = self.fields_update.get(item, cls._nodefault)
            else:
                ret = self.fields_income.get(item, cls._nodefault)
            if ret is cls._nodefault:
                ret = None
            result.append((item, ret))
        return result
    def load_from_orm(self, d, ignore=True):
        for field in self.fields_seq:
            try:
                self[field.name] = getattr(d, field.name)
            except AttributeError:
                if ignore:
                    sys.exc_clear()
                else:
                    raise
    def load_from_orm_autoincrement(self, d, ignore=True):
        for field in self.fields_seq:
            if not field.autoincrement:
                continue
            try:
                self[field.name] = getattr(d, field.name)
            except AttributeError:
                if ignore:
                    sys.exc_clear()
                else:
                    raise
    def store_to_orm(self, d):
        for field in self.fields_seq:
            try:
                getattr(d, field.name)
                setattr(d, field.name, self[field.name])
            except AttributeError:
                sys.exc_clear()
    def store_to_orm_autoincrement(self, d):
        for field in self.fields_seq:
            if not field.autoincrement:
                continue
            try:
                getattr(d, field.name)
                setattr(d, field.name, self[field.name])
            except AttributeError:
                sys.exc_clear()
    def load_from_dict(self, d, ignore=True):
        for field in self.fields_seq:
            try:
                self[field.name] = d[field.name]
            except KeyError:
                if ignore:
                    sys.exc_clear()
                else:
                    raise
    labels = {}
    def get_label(self, field):
        return self.labels.get(field.name)
    ftypes = {}
    def get_ftype(self, field):
        return self.ftypes.get(field.name, 'text')
    def selectable(self, field):
        return getattr(self, 'select_' + field.name)(field)
    def xmldata(self, xmlnode='form', **kw):
        cls = self.__class__
        if type(xmlnode) is str:
            xmlnode = getattr(E, xmlnode)(**kw)
        result = []
        for field in self.fields_seq:
            item = field.name
            if item in self.fields_update:
                ret = self.fields_update.get(item, cls._nodefault)
            else:
                ret = self.fields_income.get(item, cls._nodefault)
            xmlnode.append(self.xmlfield(field, ret))
        return xmlnode
    def xmlfield(self, field, val):
        name = field.name
        label = self.get_label(field)
        if label is None:
            # Для поля не определено текстовое значение.
            # Делаем её hidden.
            ftype = 'hidden'
        else:
            ftype = self.get_ftype(field)
        tags = [ E.name(name), E.ftype(ftype) ]
        if label is not None:
            tags.append(E.label(label))
        if ftype == 'select':
            tags.append(self.selectable(field))
        if field.single:
            tags.append(E.value(self.xmlencode(field, val)))
        else:
            tags.extend(( E.value(self.xmlencode(field, r)) for r in val ))
        return getattr(E, field.name)(*tags)
    def xmlencode(self, field, value):
        return unicode(value)

class template(object):
    class __metaclass__(type):
        """
Корневой шаблонизатор компилируем только раз на стадии инициализации класса,
что будет сказываться на скорости проработки всей страницы.
"""
        def __new__(cls, cname, cbases, cvars):
            xslpaste = cvars.pop('cls__xslpaste', None)
            ret = type.__new__(cls, cname, cbases, cvars)
            if not hasattr(ret, 'cls__xslacl') or not hasattr(ret, 'cls__xslparser'):
                ret.cls__xslacl = et.XSLTAccessControl(read_network=False)
                ret.cls__xslparser = et.XMLParser(
                        dtd_validation=False,
                        resolve_entities=True,
                        load_dtd=True,
                        ns_clean=False)
            if xslpaste is not None:
                xml = et.XML(xslpaste, parser=ret.cls__xslparser)
                ret.cls__xslpaste = et.XSLT(xml, access_control=ret.cls__xslacl)
            if not hasattr(ret, 'cls__xslpaths'):
                ret.cls__xslpaths = {}
            ret.cls__xslnames = {}
            if ret.debug:
                if ret.cls__template_path is not None:
                    ret.cls__xsllist.extend(ret.cls__xsllist_default)
                    for name, filename in ret.cls__xsllist:
                        ret.xslload_path(name, filename)
            return ret
    cls__application = 'application'
    cls__charset_default = 'utf-8'

    cls__template_path = None
    cls__xsllist_default = []
    cls__xsllist = [
        ('', '__root__.xsl'),
    ]
    cls__product = E.product(E.fullname("not defined"), E.license("n/a"))
    cls__title = "[EMPTY]"
    cls__externals = ()
    cls__namespaces = {
        'xi': 'urn:xi',
        'css': 'urn:css',
    }
    cls__pathprefix = '/'
    # Шаблон предназначен:
    # - для обозначения CSS параметров в отдельных атрибутах: css:attribute-name="value";
    # - этот документ является преобразователем для основного документа, причем может
    #   использоваться неоднократно, формируя разные уровни вложенности.
    cls__xslpaste = """
<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:css="urn:css"
  xmlns:xi="urn:xi"
  exclude-result-prefixes="css xi">
  <xsl:output
    method="xml"
    doctype-public="-//W3C//DTD XHTML 1.0 Strict//EN"
    doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"/>
  <xsl:template match="*|comment()">
    <xsl:element name="{name()}">
      <xsl:for-each select="@*[not(namespace-uri() = 'urn:css' or namespace-uri() = 'urn:xi' or name() = 'style')]">
        <xsl:attribute name="{name()}">
          <xsl:value-of select="."/>
        </xsl:attribute>
      </xsl:for-each>
      <xsl:choose>
        <xsl:when test="@*[namespace-uri() = 'urn:css']">
          <xsl:attribute name="style">
            <xsl:for-each select="@*[namespace-uri() = 'urn:css']">
              <xsl:value-of select="local-name()"/>
              <xsl:text>:</xsl:text>
              <xsl:value-of select="translate(., ';', '')"/>
              <xsl:text>;</xsl:text>
              <xsl:if test="position() != last()">
                <xsl:text> </xsl:text>
              </xsl:if>
            </xsl:for-each>
            <xsl:if test="@style">
              <xsl:text> </xsl:text>
              <xsl:value-of select="@style"/>
            </xsl:if>
          </xsl:attribute>
        </xsl:when>
        <xsl:otherwise>
          <xsl:if test="@style">
            <xsl:copy select="."/>
          </xsl:if>
        </xsl:otherwise>
      </xsl:choose>
      <xsl:value-of select="@xi:text"/>
      <xsl:apply-templates/>
    </xsl:element>
  </xsl:template>
  <xsl:template match="comment()">
    <xsl:copy/>
  </xsl:template>
  <xsl:template match="xi:bind">
    <xsl:apply-templates/>
  </xsl:template>
</xsl:stylesheet>
"""
    methods = [
        'rr_form',
    ]
    urlencode = staticmethod(urllib.urlencode)
    urlparse = staticmethod(urlparse.urlparse)
    debug = True
    def __init__(self, resp, apps=None):
        object.__init__(self)
        cls = self.__class__
        if apps is None:
            apps = cls.cls__application
        self.title = cls.cls__title
        self.resp = resp
        self.req = resp.request
        self.environ = self.req.environ
        self.apps = apps
        self.rr_initialize()

        for meth in self.methods:
            getattr(self, meth)()

        self.rr_checkperm()
        self.rr_startup()
        try:
            if not hasattr(self, 'xmlresult') or not self.xmlresult():
                app = getattr(self, self.apps)
                app()
                self.rr_output()
        except:
            exc_info = sys.exc_info()
            self.rr_cleanup(exc_info)
        else:
            self.rr_cleanup()
    def __call__(self, environ, start_response):
        return self.resp(environ, start_response)
    def rr_initialize(self):
        self.xmlentities = {}
        self.xmlnodemap = {}
        self.xmlbinds = {}
        self.xmlroot = E.R()
        self.externals = list(self.cls__externals)
        self.errors = []
        self.results = []

        path_info = self.req.path_info
        paths = self.req.path_info.split('/')
        paths[-1] = ''
        path_menu = '/'.join(paths)
        paths.pop()
        paths[-1] = ''
        path_up = '/'.join(paths)
        if not path_up or not path_up.startswith(self.cls__pathprefix):
            path_up = self.cls__pathprefix
        self.path_info = path_info
        self.path_menu = path_menu
        self.path_up = path_up
    def rr_checkperm(self):
        pass
    def rr_form(self):
        self.form = self.callback_form(self)
    def rr_startup(self):
        pass
    def rr_cleanup(self, exc_info=None):
        pass
    def rr_output(self):
        cs = self.resp.charset
        if cs is None:
            self.resp.charset = cs = 'utf-8'
        self.resp.body = et.tostring(self.xmlroot, encoding=cs, pretty_print=self.debug)
    @classmethod
    def E_product(self):
        return self.cls__product
    def E_page(self):
        paths = self.req.path_info.split('/')
        paths[-1] = ''
        path_menu = '/'.join(paths)
        paths.pop()
        paths[-1] = ''
        path_up = '/'.join(paths)
        if not path_up or not path_up.startswith(self.cls__pathprefix):
            path_up = self.cls__pathprefix
        self.path_menu = path_menu
        self.path_up = path_up
        return E.page(
            E.title(self.title),
            E.path_info(self.req.path_info),
            E.path_menu(path_menu),
            E.path_up(path_up),
        )
    def E_external(self):
        if self.apps != 'access_denied':
            return E.external(*[ getattr(E, r.rsplit('.', 1)[-1])(r) for r in self.externals ])
        return E.external()
    def E_user(self):
        return E.user()
    def E_form(self, *args, **kw):
        return self.form.xmldata(*args, **kw)
    def E_data(self):
        return E.data()
    def E_tables(self):
        return E.tables()
    def E_ivars(self):
        return E.ivars()
    def E_menus(self):
        return E.menus()
    def E_results(self):
        return E.results(*[ E.result(r) for r in self.results ])
    def E_errors(self):
        return E.errors(*[ E.error(r) for r in self.errors ])
    def xmlresult(self):
        return
    def application(self):
        xml = E.R(
            self.E_page(),
            self.E_external(),
            self.E_user(),
            self.E_product(),
            self.E_form(),
            self.E_data(),
            self.E_tables(),
            self.E_ivars(),
            self.E_menus(),
            # Должны выполнятся позже всех.
            self.E_results(),
            self.E_errors(),
        )
        self.xsllist_execute(xml)
    def xsllist_execute(self, xml):
        self.cls__xsllist.extend(self.cls__xsllist_default)
        for name, filename in self.cls__xsllist:
            self.xsl_exec(name, filename, xml)
        self.xsl_fillbind()
    @classmethod
    def xslload_path(cls, name, path):
        xslt = cls.cls__xslnames.get(name)
        if xslt is None:
            # XXX: тут поставить начало проверки времени создания
            try:
                try:
                    realpath = os.path.realpath(os.path.join(cls.cls__template_path, path))
                    xslt = cls.cls__xslpaths.get(realpath)
                    if xslt is None:
                        # Зачитываем файл, если не нашли в кеше.
                        fout = open(realpath)
                        xml = et.parse(fout, parser=cls.cls__xslparser)
                        xslt = et.XSLT(xml, access_control=cls.cls__xslacl)
                        cls.cls__xslpaths[realpath] = xslt
                        del xml, fout
                    cls.cls__xslnames[name] = xslt
                except:
                    raise
            finally:
                # XXX: тут поставить завершение проверки времени создания
                pass
        return xslt
    def xsl_exec(self, name, path, dataroot):
        cls = self.__class__
        xslt = self.xslload_path(name, path)
        docroot = xslt(dataroot, **self.xmlentities)
        xmlroot = docroot.getroot()
        if xmlroot is None:
            return
        self.xmlbinds[name] = ret = xmlroot.getroottree()
        # Запоминаем точки загрузки узлов. Карта накапливается в процессе
        # обработки нескольких документов.
        nodemap = self.xmlnodemap
        for node in docroot.xpath('//xi:bind', namespaces=cls.cls__namespaces):
            nodemap.setdefault(node.get('name', ''), []).append(node)
        return ret
    def xsl_fillbind(self, nodemap=None, binds=None):
        if nodemap is None:
            nodemap = self.xmlnodemap
        if binds is None:
            binds = self.xmlbinds
        for name, value in self.xmlbinds.items():
            if issubclass(value.__class__, basestring):
                for node in nodemap.get(name, ()):
                    node.text = value
            else:
                # FIXME: Скомпирировать выражение при помощи XPath класса
                rootx = value.xpath('/*')
                for node in nodemap.get(name, ()):
                    node.extend(rootx)
        try:
            self.xmlroot = self.cls__xslpaste(self.xmlbinds[''])
        except et.XSLTApplyError, e:
            raise ValueError(e, et.tostring(self.xmlbinds[''], pretty_print=1))
