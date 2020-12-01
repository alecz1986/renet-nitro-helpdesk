#
# -*- coding: utf-8 -*-

import os
import sys
import re
import sqlalchemy
import datetime
import Image
import lxml
from lxml import etree
from lxml.builder import E as EE
from StringIO import StringIO
from fullshopapi import Info_page
from fullshopapi import Category
from fullshopapi import News
from fullshopapi import Sale
from fullshopapi import Line
from rrduet.rr_template import E, field
from hta_base import template_base, form_base, check_action
from hta_page import menu_base
from hta_main import keywords
from hta_sys_product import resize_photo
from hta_config import htdocs_dir

class info(template_base):
    cls__kwds = set([ 'pages' ])
    cls__title = u"Информационные страницы"
    cls__xsllist = [
        ('', '__root__.xsl'),
        ('body', 'info.xsl'),
        ('form', '__simpleedit__.xsl'),
    ]
    cls__externals = [
        '/data/richedit.js',
    ]
    class callback_form(form_base):
        fields = [
            field('info_page_id', 0, int, ValueError),
            field('category_id',0, int, ValueError),
            field('weight',0, int, ValueError),
            field('name',''),
            field('uri',''),
            field('photo',None, complexity=True),
            field('anons',''),
            field('sarbc',''),
            field('author',''),
            field('text',''),
            field('action',''),
            ]
        labels = {'category_id':u'Выберите категорию',
                  'name':u'Название',
                  'uri':u'Часть url',
                  'weight':u'Вес',
                  'photo':u'Фото',
                  'anons':u'Анонс',
                  'sarbc':u'Раздел на SARBC',
                  'author':u'Авторство',
                  'text':u'Текст статьи',
                  }
        ftypes = {'category_id': 'select',
                'sarbc':'select',
                'photo':'file',
                'text':'textarea',
                'anons':'textarea',
                'author':'textarea',
                }

        def select_category_id(self, field):
            options = []
            for r in self.template_ref().dbconn.query(Category).all():
                options.append(E.option(E.value(str(r.category_id)), r.name))
            options.append(E.option(E.value(str(0)), u'все'))
            options.append(E.option(E.value(str(1)), u'статьи'))
            return E.options(*options)
        
        def select_sarbc(self, field):
            options = []
            options.append(E.option(E.value(str('')), u'не размещать'))
            options.append(E.option(E.value(str('health')), u'здоровье'))
            options.append(E.option(E.value(str('auto')), u'авто'))
            options.append(E.option(E.value(str('mama')), u'мама и малыш'))
            options.append(E.option(E.value(str('torg')), u'торговля'))
            options.append(E.option(E.value(str('realty')), u'недвижимость'))
            return E.options(*options)

    def E_form(self):
        return template_base.E_form(self, multipart='yes')
    def logic(self):
        form = self.form
        action = form['action']
        info_page_id = form['info_page_id']
        category_id = form['category_id']
        name = form['name']
        uri = form['uri']
#        text = self.req.POST.get('richEdit0', '')
        text = form['text']
        weight = form['weight']
        photo = form['photo']
        anons = form['anons']
        sarbc = form['sarbc']
        author = form['author']
        dbconn = self.dbconn
        form['action'] = 'check'
        filename = None
        small_x = small_y = None
        if action == 'check':
            if info_page_id==0 and  name and uri:
                if photo is not None:
                    filename = photo.filename
                    f = photo.file
                    import Image
                    img = Image.open(f)
                    width, height = img.size
                    small_x, small_y = resize_photo(width, height, 100,100)
                    img = img.resize((small_x, small_y), Image.ANTIALIAS)
                    img.save(htdocs_dir+'/'+filename)
                info = Info_page(category_id, name, uri, datetime.datetime.now(), weight, filename, anons, sarbc, author, small_x, small_y)
                dbconn.add(info)
                try:
                    dbconn.commit()
                    f = open(htdocs_dir+'/pages/'+uri+'.html', 'w')
                    f.write(text.encode('utf-8'))
                    f.close()
                    self.results.append(u'Страница успешно сохранена')
                except:
                    self.results.append(u'Конфликт имен')
            elif info_page_id and name and uri:
                try:
                    info = dbconn.query(Info_page).filter(Info_page.info_page_id == info_page_id).one()
                except sqlalchemy.orm.exc.NoResultFound:
                    sys.exc_clear()
                    return
                try:
                    if photo is not None:
                        filename = photo.filename
                        f = photo.file
                        import Image
                        img = Image.open(f)
                        width, height = img.size
                        small_x, small_y = resize_photo(width, height, 100,100)
                        img = img.resize((small_x, small_y), Image.ANTIALIAS)
                        img.save(htdocs_dir+'/'+filename)
                    info.category_id = category_id
                    info.name = name
                    info.uri = uri
                    info.weight = weight
                    info.photo = filename
                    info.anons = anons
                    info.sarbc = sarbc
                    info.author = author
                    dbconn.commit()
                    f = open(htdocs_dir+'/pages/'+uri+'.html', 'w')
                    f.write(text.encode('utf-8'))
                    f.close()
                    self.results.append(u'Страница успешно сохранена')
                except:
                    self.results.append(u'Страница не найдена')

            name_old = uri+'.html'
            name_new = uri+'.html'+"2"
            path = htdocs_dir+'/pages/'
            filename_old = os.path.join(path, name_old)
            filename_new = os.path.join(path, name_new)
            css = ["/data/basic.css", "/data/highslide/highslide.css"]
            t ='/usr/local/bin/tidy -q -language ru -utf8 -asxml --wrap 78 --drop-empty-paras 1 --drop-proprietary-attributes 1 --hide-comments 1 --join-classes 1 --join-styles 1 --fix-uri 1 --logical-emphasis 1 --lower-literals 1 --merge-divs 1 --merge-spans 1 --output-xml 1 --quote-ampersand 1 --quote-marks 1 --quote-nbsp 1 --repeated-attributes keep-first --replace-color 1 --indent-spaces 0 --indent 0 --indent-attributes 0 --wrap-sections 0 --newline LF --show-body-only 0 '+filename_old+' 2> /dev/null >'+filename_new
            parser = etree.HTMLParser(encoding='utf-8')
            os.popen(t)
            f = open(filename_new, 'r')
            tree = etree.parse(f, parser)
            try:
                try:
                    head = tree.xpath("/html/head")[0]
                    for c in css:
                        head.append(EE.link(rel="stylesheet", type="text/css",href=c))
                except:
                    pass
#                result = etree.tostring(tree.getroot(), encoding="utf8", pretty_print=True, method="xml" )
                result = etree.tostring(tree, encoding="utf8", pretty_print=True)
                f.close()
                os.remove(filename_old)
                r = open(filename_old, 'w')
                r.write(result)
                r.close()
                os.remove(filename_new)
            except:
                os.remove(filename_new)
        elif action == 'delete':
            try:
                info = dbconn.query(Info_page).filter(Info_page.info_page_id == info_page_id).one()
            except sqlalchemy.orm.exc.NoResultFound:
                sys.exc_clear()
                self.errors.append(u'Страница не найдена')
                return
            dbconn.delete(info)
            dbconn.commit()
            try:
                os.remove(htdocs_dir+'/pages/'+info.uri+'.html')
            except OSError, err:
                pass
            self.results.append(u'Страница успешно удалена')
        if info_page_id:
            try:
                info = dbconn.query(Info_page).filter(Info_page.info_page_id == info_page_id).one()
            except sqlalchemy.orm.exc.NoResultFound:
                sys.exc_clear()
                return
            f = open(htdocs_dir+'/pages/'+uri+'.html', 'r')
            form['text'] = f.read().replace('\n', " ").replace("'", '"').decode('utf-8')
            f.close()
            form['name'] = info.name
            form['uri'] = info.uri
            form['weight'] = info.weight
            form['category_id'] = info.category_id
            form['anons'] = info.anons
            form['sarbc'] = info.sarbc
            form['author'] = info.author

    def E_data(self):
        dbconn = self.dbconn
        try: 
            uri = dbconn.query(Info_page.uri).filter(Info_page.info_page_id == self.form['info_page_id']).one()[0]
            f = open(htdocs_dir+'/pages/'+ uri+'.html', 'r')
            text = f.read().replace('\n', " ").replace("'", '"')
            f.close()
            if not text:
                text = 'Текст статьи'
        except sqlalchemy.orm.exc.NoResultFound:
            sys.exc_clear()
            text = 'Текст статьи'
        info = dbconn.query(Info_page)
        data = E.data( text=text.decode('utf-8'))
        data_tag = data.xpath('//data')[0]
        for p in info:
            data_tag.append(E.info(info_page_id=str(p.info_page_id), name=p.name, uri=p.uri, category_id=str(p.category_id), weight=str(p.weight)))
        return data




class news(template_base):
    cls__kwds = set([ 'pages' ])
    cls__title = u"Новости"
    cls__xsllist = [
        ('', '__root__.xsl'),
        ('body', 'news.xsl'),
        ('form', '__simpleedit__.xsl'),
    ]
    cls__externals = [
        '/data/richedit.js',
    ]
    class callback_form(form_base):
        fields = [
            field('new_id', 0, int, ValueError),
            field('name',''),
            field('uri',''),
            field('overview',''),
            field('photo',None, complexity=True),
            field('action',''),
            ]
        labels = {'overview':u'Краткое содержание',
                  'photo': u'Загрузите фото для новости',
                  'name':u'Название',
                  'uri':u'Часть url',
                  }

        ftypes = {'photo':'file'}

    def E_form(self):
        return template_base.E_form(self, multipart='yes')

    def logic(self):
        action = self.form['action']
        new_id = self.form['new_id']
        overview = self.form['overview']
        photo = self.form['photo']
        name = self.form['name']
        uri = self.form['uri']
        text = self.req.POST.get('richEdit0', '')
        self.form['action'] = 'check'
        dbconn = self.dbconn
        if action == 'check':
            if new_id==0 and overview and name and uri:
                if photo is not None:
                    filename =photo.filename
                else:
                    filename=''
                new = News(name, uri, overview, filename, datetime.datetime.now())
                dbconn.add(new)
                try:
                    dbconn.commit()
                    if photo is not None:
                        f = photo.file
                        import Image
                        img = Image.open(f)
                        width, height = img.size
                        small_x, small_y = resize_photo(width, height, 200,200)
                        img = img.resize((small_x, small_y), Image.ANTIALIAS)
                        img.save(htdocs_dir+'/'+filename)
                    t = open(htdocs_dir+'/pages/'+uri+'.html', 'w')
                    t.write(text.encode('utf-8'))
                    t.close()
                    self.results.append(u'Страница успешно сохранена')
                except:
                    self.results.append(u'Конфликт имен')
            elif new_id and overview and name and uri:
                try:
                    new = dbconn.query(News).filter(News.new_id == new_id).one()
                except sqlalchemy.orm.exc.NoResultFound:
                    sys.exc_clear()
                    self.results.append(u'Страница не найдена')
                    return
                new.overview = overview
                new.name = name
                new.uid = uri
                if photo is not None:
                    new.photo = photo.filename
                    f = photo.file
                    import Image
                    img = Image.open(f)
                    width, height = img.size
                    small_x, small_y = resize_photo(width, height, 200,200)
                    img = img.resize((small_x, small_y), Image.ANTIALIAS)
                    img.save(htdocs_dir+'/'+photo.filename)
                dbconn.commit()
                t = open(htdocs_dir+'/pages/'+uri+'.html', 'w')
                t.write(text.encode('utf-8'))
                t.close()
                self.results.append(u'Страница успешно сохранена')
            name_old = uri+'.html'
            name_new = uri+'.html'+"2"
            path = htdocs_dir+'/pages/'
            filename_old = os.path.join(path, name_old)
            filename_new = os.path.join(path, name_new)
            css = ["/data/basic.css", "/data/highslide/highslide.css"]
            t ='/usr/local/bin/tidy -q -language ru -utf8 -asxml --wrap 78 --drop-empty-paras 1 --drop-proprietary-attributes 1 --hide-comments 1 --join-classes 1 --join-styles 1 --fix-uri 1 --logical-emphasis 1 --lower-literals 1 --merge-divs 1 --merge-spans 1 --output-xml 1 --quote-ampersand 1 --quote-marks 1 --quote-nbsp 1 --repeated-attributes keep-first --replace-color 1 --indent-spaces 0 --indent 0 --indent-attributes 0 --wrap-sections 0 --newline LF --show-body-only 0 '+filename_old+' 2> /dev/null >'+filename_new
            parser = etree.HTMLParser(encoding='utf-8')
            os.popen(t)
            f = open(filename_new, 'r')
            tree = etree.parse(f, parser)
            try:
                head = tree.xpath("/html/head")[0]
                for c in css:
                    head.append(EE.link(rel="stylesheet", type="text/css",href=c))
                result = etree.tostring(tree.getroot(), encoding="utf8",
                        pretty_print=True, method="html" )
                f.close()
                os.remove(filename_old)
                r = open(filename_old, 'w')
                r.write(result)
                r.close()
                os.remove(filename_new)
            except:
                os.remove(filename_new)
        elif action == 'delete':
            try:
                new = dbconn.query(News).filter(News.new_id == new_id).one()
            except sqlalchemy.orm.exc.NoResultFound:
                sys.exc_clear()
                self.results.append(u'Страница не найдена')
                return
            dbconn.delete(new)
            dbconn.commit()
            try:
                os.remove(htdocs_dir+'/pages/'+new.uid+'.html')
                os.remove(htdocs_dir+'/'+new.photo)
            except OSError, err:
                pass
            self.results.append(u'Страница успешно удалена')
        if self.results:
            self.form['new_id'] == 0
    def E_data(self):
        dbconn = self.dbconn
        try: 
            uri = dbconn.query(News.uid).filter(News.new_id == self.form['new_id']).one()[0]
            f = open(htdocs_dir+'/pages/'+ uri+'.html', 'r')
            text = f.read().replace('\n', " ").replace("'", '"')
            f.close()
        except sqlalchemy.orm.exc.NoResultFound:
            sys.exc_clear()
            text = 'Текст статьи'
        info = dbconn.query(News)
        data = E.data(E.rich(), text=text.decode('utf-8'), link=u'new')
        data_tag = data.xpath('//data')[0]
        for p in info:
            data_tag.append(E.new(new_id=str(p.new_id), name=p.name, uri=p.uid, text=p.overview, photo=p.photo))
        return data
class sale(template_base):
    cls__kwds = set([ 'pages' ])
    cls__title = u"Акции"
    cls__xsllist = [
        ('', '__root__.xsl'),
        ('body', 'news.xsl'),
        ('form', '__simpleedit__.xsl'),
    ]
    cls__externals = [
        '/data/richedit.js',
    ]
    class callback_form(form_base):
        fields = [
            field('new_id', 0, int, ValueError),
            field('name',''),
            field('uri',''),
            field('overview',''),
            field('action',''),
            ]
        labels = {'overview':u'Краткое содержание',
                  'name':u'Название',
                  'uri':u'Часть url',
                  }


    def logic(self):
        action = self.form['action']
        new_id = self.form['new_id']
        overview = self.form['overview']
        name = self.form['name']
        uri = self.form['uri']
        text = self.req.POST.get('richEdit0', '')
        self.form['action'] = 'check'
        dbconn = self.dbconn
        if action == 'check':
            if new_id==0 and overview and name and uri:
                new = Sale(name, uri, overview, datetime.datetime.now())
                dbconn.add(new)
                try:
                    dbconn.commit()
                    t = open(htdocs_dir+'/pages/'+uri+'.html', 'w')
                    t.write(text.encode('utf-8'))
                    t.close()
                    self.results.append(u'Страница успешно сохранена')
                except:
                    self.results.append(u'Конфликт имен')
            elif new_id and overview and name and uri:
                try:
                    new = dbconn.query(Sale).filter(Sale.sale_id == new_id).one()
                except sqlalchemy.orm.exc.NoResultFound:
                    self.results.append(u'Страница не найдена')
                    sys.exc_clear()
                    return
                new.overview = overview
                new.name = name
                new.uid = uri
                dbconn.commit()
                t = open(htdocs_dir+'/pages/'+uri+'.html', 'w')
                t.write(text.encode('utf-8'))
                t.close()
                self.results.append(u'Страница успешно сохранена')
            name_old = uri+'.html'
            name_new = uri+'.html'+"2"
            path = htdocs_dir+'/pages/'
            filename_old = os.path.join(path, name_old)
            filename_new = os.path.join(path, name_new)
            css = ["/data/basic.css", "/data/highslide/highslide.css"]
            t ='/usr/local/bin/tidy -q -language ru -utf8 -asxml --wrap 78 --drop-empty-paras 1 --drop-proprietary-attributes 1 --hide-comments 1 --join-classes 1 --join-styles 1 --fix-uri 1 --logical-emphasis 1 --lower-literals 1 --merge-divs 1 --merge-spans 1 --output-xml 1 --quote-ampersand 1 --quote-marks 1 --quote-nbsp 1 --repeated-attributes keep-first --replace-color 1 --indent-spaces 0 --indent 0 --indent-attributes 0 --wrap-sections 0 --newline LF --show-body-only 0 '+filename_old+' 2> /dev/null >'+filename_new
            parser = etree.HTMLParser(encoding='utf-8')
            os.popen(t)
            f = open(filename_new, 'r')
            tree = etree.parse(f, parser)
            try:
                head = tree.xpath("/html/head")[0]
                for c in css:
                    head.append(EE.link(rel="stylesheet", type="text/css",href=c))
                result = etree.tostring(tree.getroot(), encoding="utf8",
                        pretty_print=True, method="html" )
                f.close()
                os.remove(filename_old)
                r = open(filename_old, 'w')
                r.write(result)
                r.close()
                os.remove(filename_new)
            except:
                os.remove(filename_new)
        elif action == 'delete':
            try:
                new = dbconn.query(Sale).filter(Sale.sale_id == new_id).one()
            except sqlalchemy.orm.exc.NoResultFound:
                self.results.append(u'Страница не найдена')
                sys.exc_clear()
                return
            dbconn.delete(new)
            dbconn.commit()
            try:
                os.remove(htdocs_dir+'/pages/'+new.uid+'.html')
            except OSError, err:
                pass
            self.results.append(u'Страница успешно удалена')
        if self.results:
            self.form['new_id'] == 0
    def E_data(self):
        dbconn = self.dbconn
        try: 
            uri = dbconn.query(Sale.uid).filter(Sale.sale_id == self.form['new_id']).one()[0]
            f = open(htdocs_dir+'/pages/'+ uri+'.html', 'r')
            text = f.read().replace('\n', " ").replace("'", '"')
            f.close()
        except sqlalchemy.orm.exc.NoResultFound:
            sys.exc_clear()
            text = 'Текст статьи'
        info = dbconn.query(Sale)
        data = E.data(E.rich(), text=text.decode('utf-8'), link=u'sale')
        data_tag = data.xpath('//data')[0]
        for p in info:
            data_tag.append(E.new(new_id=str(p.sale_id), name=p.name, uri=p.uid, text=p.overview))
        return data
class spec(template_base):
    cls__kwds = set([ 'pages' ])
    cls__title = u"Спецпредложения"
    cls__xsllist = [
        ('', '__root__.xsl'),
        ('body', 'spec.xsl'),
        ('form', '__simpleedit__.xsl'),
    ]
    class callback_form(form_base):
        fields = [
            field('uri',''),
            field('num',''),
            field('image',None, complexity=True),
            field('action',''),
            ]
        labels = {'uri':u'Ссылка',
                  'image': u'Загрузите фото',
                  }

        ftypes = {'image':'file'}

    def E_form(self):
        return template_base.E_form(self, multipart='yes')

    def logic(self):
        form = self.form
        action = form['action']
        image = form['image']
        uri = form['uri']
        form['action'] = 'check'
        num = form['num']
        path = htdocs_dir+'/data/'+ 'spec.xml'
        res = etree.fromstring(open(path, 'r').read())
        trackList = res.xpath('//trackList')[0]
        playlist = res.xpath('//playlist')[0]
        if action == 'check':
            if uri and image is not None and not num:
                filename = image.filename
                if re.match(r"^[a-zA-Z]+[0-9a-zA-Z]*(?:\.[0-9a-zA-Z]+)?$", filename) is None:
                    self.errors.append(u'Название файла должно содеражать латинские буквы и цифры.')
                    return
                f = image.file
                img = Image.open(f)
                img.save(htdocs_dir+'/data/'+filename)
                trackList.append(E.track(E.location('http://peshca.ru/data/'+filename), E.info(uri), num=filename))
                self.results.append(u'Запись успешно добавлена')
            elif num:
                if image is not None:
                    filename = image.filename
                    if re.match(r"^[a-z]+[0-9a-z]*(?:\.[0-9a-z]+)?$", filename) is None:
                        self.errors.append(u'Название файла должно содеражать латинские буквы и цифры.')
                        return
                    f = image.file
                    img = Image.open(f)
                    img.save(htdocs_dir+'/data/'+filename)
                else:
                    filename = ''
                playlist.append(E.action(act='1', info=uri, location=filename, num=num))
        elif action == 'delete':
            playlist.append(E.action(num=num)) 
            self.results.append(u'Запись успешно удалена')
        xslt = StringIO(_spec)
        parser = etree.parse(xslt)
        result = etree.XSLT(parser)
        res = result(res)
        tmp = htdocs_dir+'/data/'+ '_tmp.xml'
        fn = open(tmp, 'w')
        fn.write(etree.tostring(res))
        fn.close()
        os.rename(tmp, path)
        return
    def E_data(self):
        path = htdocs_dir+'/data/'+ 'spec.xml'
        res = etree.fromstring(open(path, 'r').read())
        return res 





class line(template_base):
    cls__kwds = set([ 'pages' ])
    cls__title = u"Бегущая строка"
    cls__xsllist = [
        ('', '__root__.xsl'),
        ('body', 'line.xsl'),
        ('form', '__simpleedit__.xsl'),
    ]
    class callback_form(form_base):
        fields = [
            field('line_id', 0, int, ValueError),
            field('name',''),
            field('link',''),
            field('color',''),
            field('action',''),
            ]
        labels = {'name':u'Текст',
                'link':u'Ссылка',
                'color':u'Цвет',
                  }



    def logic(self):
        form = self.form
        action = form['action']
        name = form['name']
        link = form['link']
        color = form['color']
        line_id = form['line_id']
        form['action'] = 'check'
        dbconn = self.dbconn
        if line_id:
            try:
                line = dbconn.query(Line).filter(Line.line_id == line_id).one()
            except:
                sys.exc_clear()
                return
        if action == 'check':
            if line_id and name and color and link:
                line.name = name
                line.link = link
                line.color = color
            elif line_id == 0 and name and color and link:
                line = Line(name, link, color)
                dbconn.add(line)
        elif action == 'delete':
            dbconn.delete(line)
            form['line_id'] = 0
            form['name'] = ''
            form['link'] = ''
            form['color'] = ''
        if action:
            try:
                dbconn.commit()
                self.results.append(u'Запись успешно удалена.')
            except:
                self.errors.append(u'Конфликт имен.')
        if line_id:
            form['name'] = line.name
            form['link'] = line.link
            form['color'] = line.color
        return
    def E_data(self):
        dbconn = self.dbconn
        return E.data(E.lines(* (E.line(name=l.name, link = l.link, color=l.color, line_id=str(l.line_id)) for l in list(dbconn.query(Line)))))


_spec = '''
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xi="urn:xi" xmlns:css="urn:css">
  <xsl:template match="/">
    <playlist  version="1">
        <trackList>
            <xsl:for-each select='/playlist/trackList/track'>
                  <xsl:choose>
                    <xsl:when test="./@num = /playlist/action/@num">
                      <xsl:if test="/playlist/action/@act">
                        <xsl:element name='track'>
                           <xsl:attribute name='num'><xsl:value-of select="./@num"/></xsl:attribute>
                           <xsl:choose>
                               <xsl:when test="/playlist/action/@info != ''">
                                   <info><xsl:value-of select="/playlist/action/@info"/></info>
                               </xsl:when>
                               <xsl:otherwise>
                                   <info><xsl:value-of select="./info/text()"/></info>
                               </xsl:otherwise>
                            </xsl:choose>
                            <xsl:choose>
                               <xsl:when test="/playlist/action/@location != ''">
                                   <location><xsl:value-of select="/playlist/action/@location"/></location>
                               </xsl:when>
                               <xsl:otherwise>
                                   <location><xsl:value-of select="./location/text()"/></location>
                               </xsl:otherwise>
                           </xsl:choose>
                        </xsl:element>
                      </xsl:if>
                    </xsl:when>
                    <xsl:otherwise>
                      <xsl:element name='track'>
                       <xsl:attribute name='num'><xsl:value-of select="./@num"/></xsl:attribute>
                       <info><xsl:value-of select="./info/text()"/></info>
                       <location><xsl:value-of select="./location/text()"/></location>
                      </xsl:element>
                    </xsl:otherwise>
                  </xsl:choose>
            </xsl:for-each>
        </trackList>
    </playlist>
  </xsl:template>
</xsl:stylesheet>'''
