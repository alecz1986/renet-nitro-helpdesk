# -*- coding: utf-8 -*-

import os
import sys
import re
from rrduet.rr_template import field, E
import hta_config
from hta_base import check_action
from hta_page import form_base, template_base, menu_base
from fullshopapi import Category
from fullshopapi import Category_tree
from fullshopapi import Delivery
from fullshopapi import Product
from fullshopapi import Distributor
from fullshopapi import Price_delivery
from fullshopapi import Photo
from fullshopapi import Prod_more_category
from fullshopapi import Tehnical
from fullshopapi import CategoryRev
from fullshopapi import Category_more_link
from fullshopapi import Compl
from fullshopapi import Prod_kw
from fullshopapi import Comment_prod
import lxml.etree as et
import sqlalchemy
import sqlalchemy.orm
import csv
import cStringIO
import htu_main
from hta_config import htdocs_dir, prod_dir
from lxml.html import fragment_fromstring


class excel_semicolon(csv.excel):
    delimiter = ';'
csv.register_dialect('excel_semicolon', excel_semicolon)


class my(object):
    def __init__(self, cats, parents):
        self.node = None
        self.cats = cats
        self.parents = parents
    def get_tree(self,  cid, parent=0):
        plus='0'
        check = (lambda a: a if a is not None else '')
        if cid in self.parents and cid not in self.parents[cid] and self.parents[cid] != []:
            plus = '1'
            #E.text(fragment_fromstring(check(self.cats[cid][0]), create_parent=True))
        node = E.category(id=str(cid), name=self.cats[cid][0], new=self.cats[cid][1], desk=self.cats[cid][2], root=str(self.cats[cid][3]), plus=plus, opt=self.cats[cid][4], template=self.cats[cid][5])
        if self.node is None: 
            self.node = node 
        else:
            node2append = self.node.xpath('//category[@id=%s]' % parent)[0]
            node2append.append(node) 
        if cid in self.parents and cid not in self.parents[cid]:
            for c in self.parents[cid]:
                self.get_tree(c, cid)
def kw2strval(kw):
    nkw = {}
    for k in kw:
        nkw[k] = unicode(kw[k])
    return nkw

atlist = [
    'articul',
    'name',
    'overview',
    'discription',
    'delivery',
    'vat',
    'sale',
    'week',
    'order_desk',
    'bonus',
    'spec',
    'price',
    'price_old',
    'params',
    'category',
    'visible',
    'holiday',
    'metric',
    'kw',
    'complements'
]


class tree_parser:
    def __init__(self, dbconn):
        self.up_nodes = []
        self.nodes = []
        self.categorys = []
        self.dbconn = dbconn
    def get_tree_child(self, category_id, visible=1):
        result = [ category_id ]
        result.extend([ r[0] for r in self.dbconn.execute("select `child_id` from `category_rev` where `parent_id`=%d" % (
            category_id,
        )) ])
        return result
    def get_tree_parent(self, category_id, visible=1):
        dbconn = self.dbconn
        for r in list(dbconn.query(Category).filter(Category.category_id == CategoryRev.parent_id).filter(CategoryRev.child_id == category_id).filter(CategoryRev.visible == visible).order_by(CategoryRev.parent_lvl.desc())):
            self.up_nodes.append(r.category_id)
            self.categorys.append(r)
        return self.up_nodes

ppath = htu_main.photoid2path(prod_dir, 3)
ppath_web = htu_main.photoid2path('product', 3)
def resize_photo(width, height, config_x, config_y):
    if width<=config_x and height<=config_y:
        small_x = width
        small_y = height
    elif width > config_x and height<=config_y:
        k_x = float(width).__div__(config_x)
        small_x = width / k_x
        small_y = height / k_x
    elif height>config_y and width<=config_x:
        k_y = float(height).__div__(config_y)
        small_x = width / k_y
        small_y = height / k_y
    else:
        k_x = float(width).__div__(config_x)
        k_y = float(height).__div__(config_y)
        if k_x > k_y:
            k = k_x
        else:
            k = k_y
        small_x = width / k
        small_y = height / k
    small_x = int(small_x)
    small_y = int(small_y)
    return (small_x, small_y)


class product(menu_base):
    cls__title = u"Меню: Управление продуктами"
    cls__kwds = set([ 'product' ])
    def E_menus(self):
        sess = self.req.environ['rrduet.sess']
        distrib_id = sess['distrib_id']
        q = ''
        if  distrib_id:
            dbconn = self.dbconn
            try:
                q = '?parenet_category=0&category_id='+str(dbconn.query(Distributor.category_id).filter(Distributor.distrib_id == distrib_id).one()[0])
            except sqlalchemy.orm.exc.NoResultFound:
                sys.exc_clear()
        return E.menus(
            E.menu(E.url('/private/product/export'), E.text(u"Экспорт товаров")),
            E.menu(E.url('/private/product/export_photo'), E.text(u"Экспорт фото товаров")),
            E.menu(E.url('/private/product/download_change'), E.text(u"Импорт товаров")),
            E.menu(E.url('/private/product/import'), E.text(u"Просмотр и изменение продуктов")),
            E.menu(E.url('/private/product/zip'), E.text(u"Загрузка фотографий")),
            E.menu(E.url('/private/product/params'), E.text(u"Установка параметров изображения")),
            E.menu(E.url('/private/category'+q), E.text(u"Управление категориями")),
            E.menu(E.url('/private/product/comment'), E.text(u"Отзывы")),
        )
class comment(template_base):
    cls__kwds = set([ 'product' ])
    cls__title = u"Отзывы"
    cls__xsllist = [
        ('', '__root__.xsl'),
        ('body', 'comment_prod.xsl'),
        ('form', '__simpleedit__.xsl'),
    ]
    class callback_form(form_base):
        fields = [
            field('comment_id', 0, int, ValueError),
            field('product_id', 0, int, ValueError),
            field('name',''),
            field('comment',''),
            field('status',''),
            field('action',''),
        ]
        labels = {
            'product_id':u"Продукт",
            'name':u"Имя",
            'comment':u"Комментарий",
            'status':u"Видимость",
        }
        ftypes = {
            'comment':'textarea',
            'product_id':'readonly',
            'status':'select',
        }
        def select_status(self, field):
            options = []
            options.append(E.option(E.value(u'no'), u'нет'))
            options.append(E.option(E.value(u'yes'), u'есть'))
            return E.options(*options)
    def logic(self):
        dbconn = self.dbconn
        form = self.form
        
        action = form['action']
        comment_id = form['comment_id']
        product_id = form['product_id']
        name = form['name']
        comment = form['comment']
        status = form['status']
        form['action'] = 'check'
        if action == 'check':
            if comment_id ==0:
                if product_id and name and comment and status:
                    comment_prod = Comment_prod(product_id, name, comment, status)
                    dbconn.add(comment_prod)
                    try:
                        dbconn.commit()
                        self.results.append(u"Комментарий успешно сохранен")
                    except:
                        sys.exc_clear()
                        dbconn.rollback()
                        self.errors.append(u"Конфликт имен")
                else:
                    self.errors.append(u"Не все поля были заполнены.")
            else:
                try:
                    comment_prod = dbconn.query(Comment_prod).filter(Comment_prod.comment_id == comment_id).one()
                    comment_prod.name = name
                    comment_prod.product_id = product_id
                    comment_prod.comment = comment
                    comment_prod.status = status
                    try:
                        dbconn.commit()
                        self.results.append(u"Комментарий успешно сохранен")
                    except:
                        sys.exc_clear()
                        dbconn.rollback()
                        self.errors.append(u"Конфликт имен")

                except sqlalchemy.orm.exc.NoResultFound:
                    sys.exc_clear()
                    self.errors.append(u"Комментарий не найден")

        elif action == 'delete' and comment_id:
            try:
                comment_prod = dbconn.query(Comment_prod).filter(Comment_prod.comment_id == comment_id).one()
            except sqlalchemy.orm.exc.NoResultFound:
                sys.exc_clear()
                self.errors.append(u'Изменения не были сохранены')
                return
            dbconn.delete(comment_prod)
            dbconn.commit()
        elif comment_id:
            try:
                comment_prod = dbconn.query(Comment_prod).filter(Comment_prod.comment_id == comment_id).one()
                form['name'] = comment_prod.name
                form['comment'] = comment_prod.comment
                form['status'] = comment_prod.status
                form['product_id'] = comment_prod.product_id

            except sqlalchemy.orm.exc.NoResultFound:
                sys.exc_clear()
                self.errors.append(u'Изменения не были сохранены')
                return
            
    def E_data(self):
        dbconn = self.dbconn
        comments = [E.comment(comment_id = str(r.comment_id),
            status = r.status,
            prod_id = str(r.product_id),
            prod_name = p.name,
            name = r.name,
            comment = r.comment) for r, p in dbconn.query(Comment_prod, Product).filter(Comment_prod.product_id==Product.product_id).order_by('-status')]
        return E.data(*comments)


class category(template_base):
    cls__kwds = set([ 'product' ])
    cls__title = u"Категории"
    cls__xsllist = [
        ('', '__root__.xsl'),
        ('body', 'category.xsl'),
        ('form', '__simpleedit__.xsl'),
    ]

    class callback_form(form_base):
        fields = [
            field('category_id', 0, int, ValueError),
            field('parent_category', 0, int, ValueError),
            field('parent_cat', 0, int, ValueError),
            field('photo',None, complexity=True),
            field('name',''),
            field('discription',''),
            field('warning',''),
            field('visible',''),
            field('new','no'),
            field('desk','no'),
#            field('auto','no'),
            field('action',''),
            field('weight','0.00'),
#            field('opt','no'),
            field('sale','no'),
            field('kws',''),
            field('template',''),
            field('min_sum',None),
            field('syncache',False,lambda x: True),
        ]
        labels = {
            'name':u'Название',
            'discription':u'Описание',
            'warning':u'Предупреждение',
            'photo': u'Загрузите изображение',
            'visible':u'Видимость',
            'new':u'Новинка',
            'desk':u'Стол заказов',
#            'auto':u'Шаблон в 3 колонки',
            'sale':u'Акция',
            'parent_cat':u'Родительская категория',
            'weight':u'Вес',
#            'opt':u'Оптовая категория',
            'min_sum':u'Минимальная стоимость заказа',
            'syncache':u'Синхронизировать',
            'kws':u'Keyword',
            'template':u'Шаблон',
        }
        ftypes = {
            'photo': 'file',
            'discription': 'textarea',
            'kws': 'textarea',
            'visible': 'select',
            'new': 'select',
            'desk': 'select',
#            'auto': 'select',
            'sale':'select',
            'parent_cat': 'select',
#            'opt': 'select',
            'template': 'select',
            'syncache': 'checkbox',
        }
        def select_visible(self, field):
            options = []
            options.append(E.option(E.value(u'open'), u'открыта'))
            options.append(E.option(E.value(u'close'), u'закрыта'))
            return E.options(*options)
        def select_new(self, field):
            options = []
            options.append(E.option(E.value(u'yes'), u'да'))
            options.append(E.option(E.value(u'no'), u'нет'))
            return E.options(*options)
        def select_opt(self, field):
            options = []
            options.append(E.option(E.value(u'yes'), u'да'))
            options.append(E.option(E.value(u'no'), u'нет'))
            return E.options(*options)
        def select_desk(self, field):
            options = []
            options.append(E.option(E.value(u'yes'), u'да'))
            options.append(E.option(E.value(u'no'), u'нет'))
            return E.options(*options)
        def select_auto(self, field):
            options = []
            options.append(E.option(E.value(u'yes'), u'да'))
            options.append(E.option(E.value(u'no'), u'нет'))
            return E.options(*options)
        def select_sale(self, field):
            options = []
            options.append(E.option(E.value(u'yes'), u'да'))
            options.append(E.option(E.value(u'no'), u'нет'))
            return E.options(*options)
        def select_template(self, field):
            options = []
            options.append(E.option(E.value(u'category'), u'Категории со списком подкатегорий и продуктами в этих подкатегориях (как в интиме)'))
            options.append(E.option(E.value(u'food'), u'Категории с картинками и подкатегориями в них (продукты питания)'))
            options.append(E.option(E.value(u'auto'), u'Категории с картинками (как в автотоварах)'))
            options.append(E.option(E.value(u'category_opt'), u'Оптовая категория'))
            options.append(E.option(E.value(u'order_desk'), u'Список товаров как в столе заказов (как в "Сашими")'))
            options.append(E.option(E.value(u'start_desk'), u'Стол заказов (категории с картинками, левое меню - только стол заказов)'))
            return E.options(*options)
        def select_parent_cat(self, field):
            sess = self.req.environ['rrduet.sess']
            distrib_id = sess['distrib_id']
            options = []
            self.template_ref().dbconn.rollback()
            options.append(E.option(E.value(u'0'), u'корневая категория'))
            if distrib_id:
                try:
                    category_id = self.template_ref().dbconn.query(Distributor).filter(Distributor.distrib_id == distrib_id).one().category_id
                except sqlalchemy.orm.exc.NoResultFound:
                    sys.exc_clear()
                    return E.options()
                categorys = self.template_ref().dbconn.query(Category).filter(Category.category_id == CategoryRev.child_id).filter(CategoryRev.parent_id == category_id).order_by('-name')
            else:
                categorys = self.template_ref().dbconn.query(Category).order_by('-name')
            self.template_ref().dbconn.rollback()
            for op in categorys:
                options.append(E.option(E.value(str(op.category_id)), op.name))
            categorys = list(self.template_ref().dbconn.execute('select name, category_id from category where category_id not in (select parent_id from category_rev)'))
            for name, category_id in categorys:
                options.append(E.option(E.value(str(category_id)), name))
            return E.options(*options)
    def E_form(self):
        return template_base.E_form(self, multipart='yes')
    def rebuild_category(self):
        dbconn = self.dbconn
#        dbconn.execute("lock tables `category` read,`category_rev` write")
        dbconn.rollback()
        cats = dbconn.query(Category).order_by('name').all()
        dbconn.execute('delete from category_temp')
        for i in cats:
            dbconn.execute('insert into category_temp(category_id) values (%s)' % i.category_id)
        dbconn.execute('update category, category_temp set weight = category_temp_id where category.category_id = category_temp.category_id')
        dbconn.execute('update category set weight=714 where category_id=321525')
        dbconn.execute('update category set weight=715 where category_id=321526')
        dbconn.execute('update category set weight=716 where category_id=321527')
        dbconn.execute('update category set weight=717 where category_id=321528')
        dbconn.execute('update category set weight=718 where category_id=321529')
        dbconn.execute("lock tables `category` read,`category_rev` write, `category_tree` write")
        dbconn.rollback()
        pars = {}
        visibles = {}
        parents = {}
        cats = {}
        roots = []
#        categorys = list(dbconn.query(Category).order_by(Category.weight, Category.name))
        categorys = list(dbconn.query(Category).order_by(Category.weight))
        for cat in categorys:
            category_id = cat.category_id
            parent_id = cat.parent_category
            visible = cat.visible
            name = cat.name.replace("'", "`").replace('"', "`")
            new = cat.new
            cat_id = cat.category_id
            desk = cat.desk
            opt = cat.opt
            template = cat.template
            pars.setdefault(parent_id, []).append(category_id)
            visibles[category_id] = 1
            if visible == 'open':
                if parent_id == 0:
                    roots.append(cat_id)
                parents.setdefault(parent_id, []).append(cat_id)
                parents.setdefault(cat_id, [])
                cats[cat_id] = [name, new, desk, parent_id, opt, template]
        for cat_link in list(dbconn.query(Category_more_link)):
            category_id = cat_link.category_id
            category_id_more = cat_link.category_id_more
            if category_id in cats and category_id in parents and category_id_more in cats:
                parents[category_id].append(category_id_more)
        root = E.category()
        for r in roots:
            m = my(cats,parents)
            m.get_tree(r)
            node = m.node
            root.append(node)
        dbconn.execute("delete from `category_tree`")
        for cat in categorys:
            _spec = """
                <xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xi="urn:xi" xmlns:css="urn:css">
                  <xsl:template match="category">
                    <xsl:copy>
                      <xsl:apply-templates select="@*"/>
                      <xsl:if test=".//@id = '%s'">
                        <xsl:attribute name="action"><xsl:value-of select=".//@id = '%s'"/></xsl:attribute>
                        <xsl:apply-templates select="node()" />
                      </xsl:if>
                    </xsl:copy>
                  </xsl:template>
                  <xsl:template match="@*">
                    <xsl:copy/>
                  </xsl:template>
                </xsl:stylesheet>
            """ % (str(cat.category_id), str(cat.category_id))
            xslt = cStringIO.StringIO(_spec)
            parser = et.parse(xslt)
            result = et.XSLT(parser)
            res = result(root)
            if 1:
                dbconn.execute("insert into `category_tree` set `category_id`=%d,`tree`='%s'" % (cat.category_id, et.tostring(res, encoding='utf-8')))
            else:
                print 'er'
        lvl = 0
        d_lvl = {}
        d_map = {}
        ids = [ 0 ]
        while pars:
            # Цикл по группе категорий с данным уровнем вложенности.
            nids = []
            its = []
            for parent_id in ids:
                childs = pars.pop(parent_id, ())
                nids.extend(childs)
                if not parent_id:
                    # Не нужна связь от несуществующего псевдо-парента.
                    continue
                d_map[parent_id] = [ parent_id ]
                d_lvl[parent_id] = lvl
                its.extend( (parent_id, child_id) for child_id in childs )
            for parent_id, child_id in its:
                d = pars.get(child_id)
                if d is not None:
                    its.extend( (parent_id, sub_id) for sub_id in d )
                d_map[parent_id].append(child_id)
            if not nids:
                break
            ids = nids
            del nids
            lvl += 1
        dbconn.execute("delete from `category_rev`")
        for parent_id in d_map:
            if not visibles.get(parent_id, True):
                continue
            childs = d_map[parent_id]
            if not childs:
                continue
            parent_lvl = d_lvl[parent_id]
            for child_id in childs:
                if not visibles.get(child_id, True):
                    continue
                dbconn.execute("insert into `category_rev` set `parent_id`=%d,`child_id`=%d,`parent_lvl`=%d,`visible`=%d" % (
                    parent_id,
                    child_id,
                    parent_lvl,
                    visibles[category_id],
                ))
        dbconn.execute("unlock tables")
    def logic(self):
        sess = self.req.environ['rrduet.sess']
        distrib_id = sess['distrib_id']
        form = self.form

        action = form['action']
        category_id = form['category_id']
        parent_category = form['parent_category']
        parent_cat = form['parent_cat']
        name = form['name']
        discription = form['discription']
        warning = form['warning']
        photo = form['photo']
        visible = form['visible']
        new = form['new']
        desk = form['desk']
        auto = 'no'
        #form['auto']
        sale = form['sale']
        weight = form['weight']
        opt = 'no'
        #form['opt']
        min_sum = form['min_sum']
        kws = form['kws']
        template = form['template']
        form['action'] = 'check'
        dbconn = self.dbconn
        if action == 'check':
            if photo is not None:
                filename = photo.filename
                f = photo.file
            else:
                filename = None
            if  category_id == 0 and  name:
                if not discription:
                    discription =' '
                category = Category(1, parent_cat, name, discription, photo=filename, warning=warning, visible=visible, new=new, desk = desk, auto = auto, weight = weight, opt=opt, min_sum=min_sum, sale=sale, kws=kws, template=template)
                if filename:
                    try:
                        os.remove(htdocs_dir+'/category/'+category.photo)
                    except:
                        pass
                    category.photo = filename
                    import Image
                    img = Image.open(f)
                    path = htdocs_dir+'/category/'+filename
                    if img.mode != "RGB":
                        img = img.convert("RGB")
                    img.save(path)
                dbconn.add(category)
                try:
                    dbconn.commit()
                except:
                    self.errors.append(u'Конфликт имен')
            elif category_id and  name:
                try: 
                    category = dbconn.query(Category).filter(Category.category_id == category_id).one()
                except sqlalchemy.orm.exc.NoResultFound:
                    sys.exc_clear()
                    self.errors.append(u'Изменения не были сохранены')
                    return
                self.admin_actions.append(('change category', 'ip=%s, cat_id= %s, username=%s, parent_cat=%s, name=%s, visible=%s, parent_category_old=%s' % (self.req.environ['REMOTE_ADDR'], str(category_id), sess['login'], str(parent_cat), name, visible , category.parent_category)) )
                category.name = name
                category.discription = discription
                category.warning = warning
                category.visible = visible
                category.new = new
                category.desk = desk
                category.weight = weight
                category.parent_category = parent_cat
                category.opt = opt
                category.auto = auto
                category.min_sum = min_sum
                category.sale = sale
                category.kws = kws
                category.template = template
                t = tree_parser(dbconn)
                dbconn.execute("update `category` set `visible`='%s' where `category_id` in (%s)" % (
                    visible,
                    (",".join(( str(r) for r in t.get_tree_child(category_id, int(visible == 'open')) ))),
                ))
                if filename:
                    category.photo = filename
                    import Image
                    img = Image.open(f)
                    path = htdocs_dir+'/category/'+filename
                    if img.mode != "RGB":
                        img = img.convert("RGB")
                    img.save(path)
                try:
                    dbconn.commit()
                except:
                    self.errors.append(u"Для переназначаемой родительской категории категория %s уже существует." % (name, ))
                    return
        elif action == 'delete':
            self.admin_actions.append(('delete category', 'ip=%s, cat_id= %s, username=%s, parent_cat=%s, name=%s, visible=%s' % (self.req.environ['REMOTE_ADDR'], str(category_id), sess['login'], str(parent_cat), name, visible )) )
            try:
                category = dbconn.query(Category).filter(Category.category_id == category_id).one()
            except sqlalchemy.orm.exc.NoResultFound:
                sys.exc_clear()
                self.errors.append(u'Изменения не были сохранены')
                return
            dbconn.delete(category)
            dbconn.commit()
        elif action == 'delete_prod':
            self.admin_actions.append(('delete prod', 'ip=%s, cat_id= %s, username=%s, parent_cat=%s, name=%s' % (self.req.environ['REMOTE_ADDR'], str(category_id), sess['login'], str(parent_cat), name )) )
            if distrib_id is None:
                self.resp.location = '/private/category/distrib?action=check&category_id=%s' % category_id 
                self.resp.status_int = 302
                self.resp.body = ''
            else:
                products = dbconn.query(Product, Prod_more_category).filter(sqlalchemy.and_(Product.product_id == Prod_more_category.product_id, Prod_more_category.category_id == CategoryRev.child_id, CategoryRev.parent_id == category_id))
                if distrib_id:
                    products = products.filter(Product.distrib_id == distrib_id)
                prod_ids = ','.join(str(p[0].product_id) for p in products)
                try:
                    photos = dbconn.execute('select photo_id from photo join product using(product_id) where product_id in (%s)' % prod_ids)
                except:
                    photos = []
                for ph in photos:
                    path = ppath.get(ph[0], ext=".png")
                    path_small = ppath.get(ph[0], ext="_small.png")
                    try:
                        os.remove('/usr/local/fshop/ht_admin/htdocs/'+path)
                    except:
                        sys.exc_clear()
                    try:
                        os.remove('/usr/local/fshop/ht_admin/htdocs/'+path_small)
                    except:
                        sys.exc_clear()
                dbconn.execute('delete from photo where product_id in (%s)' % prod_ids)
                dbconn.execute('delete from technical where product_id in (%s)' % prod_ids)
                dbconn.execute('delete from prod_more_category where product_id in (%s)' % prod_ids)
                dbconn.execute('delete from product where product_id in (%s)' % prod_ids)
        if category_id:
            try:
                category = dbconn.query(Category).filter(Category.category_id == category_id).one()
            except sqlalchemy.orm.exc.NoResultFound:
                sys.exc_clear()
                form['category_id'] = 0
                return
            form['warning'] = category.warning
            form['name'] = category.name
            form['discription'] = category.discription
            form['visible'] = category.visible
            form['new'] = category.new
            form['desk'] = category.desk
            form['parent_cat'] = category.parent_category
            form['weight'] =  category.weight
            form['opt'] = category.opt
            form['auto'] = category.auto
            form['min_sum'] = category.min_sum
            form['sale']  = category.sale
            form['kws'] = category.kws
            form['template'] = category.template
            self.errors.append(u'Внимание! Режим редактирования категории %s. Для добавления новой категории воспользуйтесь ссылкой "Добавить категорию".' % (category.name),)
        else:
            form['parent_cat'] = parent_cat
        if form['syncache']:
            self.rebuild_category()

    def E_data(self):
        dbconn = self.dbconn
        sess = self.req.environ['rrduet.sess']
        distrib_id = sess['distrib_id']
        if distrib_id and not self.form['parent_category']:
            try:
#                self.form['parent_category'] = dbconn.query(Distributor).filter(Distributor.distrib_id == distrib_id).one().category_id
                 self.form['category_id'] = dbconn.query(Distributor).filter(Distributor.distrib_id == distrib_id).one().category_id
            except sqlalchemy.orm.exc.NoResultFound:
                sys.exc_clear()
        if self.form['parent_category'] == 0 and self.form['category_id'] != 0:
            category = dbconn.query(Category).filter(Category.category_id == self.form['category_id']).order_by('name')
        else:
            category = dbconn.query(Category).filter(Category.parent_category == self.form['parent_category']).order_by('name')
        data = E.data(parent_category=str(self.form['parent_category']), parent_cat=str(self.form['parent_cat']))
        data_tag = data.xpath('//data')[0]
        for p in category:
            if p.warning is None:
                p.warning = ''
            data_tag.append(E.category(category_id=str(p.category_id), name=p.name, discription=p.discription, warning=p.warning, parent_category=str(p.parent_category)))
        return data

class category_link(template_base):
    cls__kwds = set([ 'product' ])
    cls__title = u"Ссылки к категории"
    cls__xsllist = [
        ('', '__root__.xsl'),
        ('body', 'category_link.xsl'),
        ('form', '__simpleedit__.xsl'),
    ]
    class callback_form(form_base):
        fields = [
            field('category_id', 0, int, ValueError),
            field('category_link_id', 0, int, ValueError),
            field('name',''),
            field('category_id_more',0, int, ValueError),
            field('action',''),
        ]
        labels = {
            'name':u'Название',
            'category_id_more':u'id категории',
        }
    def logic(self):
        form = self.form
        action = form['action']
        category_id = form['category_id']
        category_link_id = form['category_link_id']
        name = form['name']
        category_id_more = form['category_id_more']
        form['action'] = 'check'
        
        dbconn = self.dbconn
        if action=='check' and not (name and category_id_more):
            self.errors.append(u'Не все поля заполнены.')
            return
        if action == 'check':
            try:
                category_link = dbconn.query(Category_more_link).filter(Category_more_link.category_more_link_id == category_link_id).one()
                category_link.name = name
                category_link.category_id_more = category_id_more
                try:
                    dbconn.commit()
                except:
                    self.errors.append(u'Запись с таким url для данной категории уже существует')
            except sqlalchemy.orm.exc.NoResultFound:
                sys.exc_clear()
                if category_id:
                    category = Category_more_link(category_id, category_id_more, name)
                    dbconn.add(category)
                try:
                    dbconn.commit()
                except:
                    sys.exc_clear()
                    self.errors.append(u'Конфликт имен')
                    return
        elif action == 'delete':
            try:
                category_link = dbconn.query(Category_more_link).filter(Category_more_link.category_more_link_id == category_link_id).one()
                form['category_id'] = category_link.category_id
                dbconn.delete(category_link)
                dbconn.commit()
                self.results.append(u'Запись успешно удалена.')
            except sqlalchemy.orm.exc.NoResultFound:
                sys.exc_clear()
                self.errors.append(u'Изменения не были сохранены')
                return
        try:
            category_link = dbconn.query(Category_more_link).filter(Category_more_link.category_more_link_id == category_link_id).one()
        except sqlalchemy.orm.exc.NoResultFound:
            sys.exc_clear()
            return
        form['category_id'] = category_link.category_id
        form['name'] = category_link.name
        form['category_id_more'] = category_link.category_id_more

    def E_data(self):
        dbconn = self.dbconn
        dbconn.rollback()
        category_link = dbconn.query(Category_more_link).filter(Category_more_link.category_id == self.form['category_id']).all()
        data = E.data(category_id=str(self.form['category_id']))
        for p in category_link:
            data.append(E.category(name=p.name, link=str(p.category_id_more), id=str(p.category_more_link_id)))
        return data

class category_distrib(template_base):
    cls__title = u"Меню: Удаление продуктов"
    cls__kwds = set([ 'product' ])
    cls__xsllist = [
        ('', '__root__.xsl'),
        ('form', '__simpleedit__.xsl'),
    ]
    class callback_form(form_base):
        fields = [
            field('distrib_id',0, int, ValueError),
            field('category_id',0, int, ValueError),
            field('action',''),
            ]
        labels = {
                'distrib_id': u'Выберите поставку',
                }
        ftypes = {'distrib_id':'select'}

        def select_distrib_id(self, field):
            options = []
            distrib_id =  self.template_ref().distrib_id
            if distrib_id:
                try:
                    distrib_name =  self.template_ref().dbconn.query(Category.name).filter(sqlalchemy.and_(Distributor.distrib_id == distrib_id, Category.category_id == Distributor.category_id)).one()
                except sqlalchemy.orm.exc.NoResultFound:
                    sys.exc_clear()
                    return E.options()
                return  E.options(E.option(E.value(str(distrib_id)), distrib_name[0]))
            else:
                for r in self.template_ref().dbconn.query(Distributor.distrib_id, Category.name).filter(Distributor.category_id == Category.category_id):
                    options.append(E.option(E.value(str(r.distrib_id)), r.name))
                return E.options(*options)
    def logic(self):
        dbconn = self.dbconn
        sess = self.req.environ['rrduet.sess']
        self.distrib_id = sess['distrib_id']
        if self.distrib_id is not None:
            distrib_id = self.distrib_id
        else:
            distrib_id = self.form['distrib_id']
        category_id = self.form['category_id']
        action = self.form['action']
        if action == 'check' and distrib_id:
            products = dbconn.query(Product, Prod_more_category).filter(sqlalchemy.and_(Product.product_id == Prod_more_category.product_id, Product.distrib_id == distrib_id, Prod_more_category.category_id == category_id))
            for p in products:
                dbconn.delete(p[1])
                dbconn.execute('delete from prod_more_category where product_id=%s' % p[0].product_id)
                p[0].articul = p[0].articul + '_del'
                dbconn.commit()




class photo_params(template_base):
    cls__title = u"Меню: Установка параметров изображения"
    cls__kwds = set([ 'product' ])
    cls__xsllist = [
        ('', '__root__.xsl'),
        ('form', '__simpleedit__.xsl'),
    ]
    class callback_form(form_base):
        fields = [
            field('width',0, int, ValueError),
            field('height',0,int, ValueError),
            field('action',''),
            ]
        labels ={
                'width': u'Установите ширину изображения',
                'height': u'Установите высоту изображения',
                }

    def logic(self):
        config_x = self.form['width']
        config_y = self.form['height']
        action = self.form['action']
        self.form['action'] = 'check'
        dbconn = self.dbconn
        if action == 'check':
            if  config_x and config_y:
                ph = dbconn.query(Photo).all()
                for i in ph:
                    path_prod = os.path.dirname(ppath.get(i.photo_id))+'/'
                    path = path_prod+str(i.photo_id)+'.png'
                    try:
                        f = open(path)
                        import Image
                        img = Image.open(f)
                        width, height = img.size
                        small_x, small_y = resize_photo(width, height, config_x, config_y)
                        i.small_x = small_x
                        i.small_y = small_y
                        dbconn.commit()
    
                        file_name = str(i.photo_id)
                        img = img.resize((small_x, small_y), Image.ANTIALIAS)
                        img.save(path_prod+file_name+'_med.png')
                    except:
                        self.errors.append(u'Фото %s не было найдено' % path)
                self.results.append(u'Фотографии были успешно изменены.')
            else:
                self.errors.append(u'Необходимо задать параметры изображения.')


class photo(template_base):
    cls__title = u"Меню: Фото товара"
    cls__kwds = set([ 'product' ])
    cls__xsllist = [
        ('', '__root__.xsl'),
        ('body', 'photo.xsl'),
        ('form', '__simpleedit__.xsl'),
    ]
    class callback_form(form_base):
        fields = [
            field('product_id', 0, int, ValueError),
            field('photo',None, complexity=True),
            field('photo_id',0, int, ValueError),
            field('weight',0,int, ValueError),
            field('action',''),
            ]
        labels ={
                'photo': u'Выберите фото для загрузки',
                }
        ftypes = {
                'photo':'file',
                }
    def E_form(self):
        return template_base.E_form(self, multipart='yes')

    def logic(self):
        config_x = 100
        config_y = 100
        config_x_m = 200
        config_y_m = 200
        action = self.form['action']
        self.form['action'] = 'check'
        product_id = self.form['product_id']
        photo_id = self.form['photo_id']
        weight = self.form['weight']
        photo = self.form['photo']
        dbconn = self.dbconn
        if action == 'check':
            if photo_id and weight:
                try:
                    ph = dbconn.query(Photo).filter(Photo.photo_id == photo_id).one()
                except sqlalchemy.orm.exc.NoResultFound:
                    sys.exc_clear()
                    return
                ph.weight = int(ph.weight)+int(weight)
                dbconn.commit()
                self.form['weight'] = ''
                self.form['photo_id'] = ''
            if photo is not None:
                try:
                    name = unicode(photo.filename)
                except:
                    self.errors.append(u'Имя файла не должно содержать русских символов')
                    return
                f = photo.file
                import Image
                import os
                img = Image.open(f)
                width, height = img.size
                small_x, small_y = resize_photo(width, height, config_x, config_y)
                small_x_m, small_y_m = resize_photo(width, height, config_x_m, config_y_m)
                do = True
                try:
                    phs = dbconn.query(Photo).filter(Photo.product_id == product_id).filter(Photo.photo_name == name)
                    if len(list(phs)) > 0:
                        self.errors.append(u'Продукт уже содержит данное изображение')
                        do = True
                        return
                except:
                    sys.exc_clear()
                if do:
                    photo = Photo(product_id, small_x, small_y, width, height, 100, name, small_x_m, small_y_m)
                    dbconn.add(photo)
                    dbconn.commit()
                    file_name = str(photo.photo_id)
                    path_prod = os.path.dirname(ppath.get(photo.photo_id))+'/'
                    try:
                        os.makedirs(os.path.dirname(path_prod), 0755)
                    except OSError:
                        sys.exc_clear()
                    img.convert('RGB').save(path_prod+file_name+'.png')
#                    img.save(path_prod+file_name+'.png', 'rgb')
                    img_s = img.resize((small_x, small_y), Image.ANTIALIAS)
                    img_s.convert('RGB').save(path_prod+file_name+'_small.png')

                    img_m = img.resize((small_x_m, small_y_m), Image.ANTIALIAS)
                    img_m.convert('RGB').save(path_prod+file_name+'_med.png')
#                    img.save(path_prod+file_name+'_small.png')
        elif action == 'delete':
            try:
                ph = dbconn.query(Photo).filter(Photo.photo_id == photo_id).one()
            except sqlalchemy.orm.exc.NoResultFound:
                sys.exc_clear()
                return
            dbconn.delete(ph)
            dbconn.commit()
            import os
            path_prod = os.path.dirname(ppath.get(ph.photo_id))+'/'
            os.remove(path_prod+str(photo_id)+'.png')
            os.remove(path_prod+str(photo_id)+'_small.png')
            os.remove(path_prod+str(photo_id)+'_med.png')



    def E_data(self):
        product_id = self.form['product_id']
        dbconn = self.dbconn
        photo = dbconn.query(Photo).filter(Photo.product_id == product_id).order_by('weight')
        data = E.data()
        data_tag = data.xpath('//data')[0]
        for ph in photo:
            path_prod = os.path.dirname(ppath_web.get(ph.photo_id))
            data_tag.append(E.photo(x=str(ph.small_x), y=str(ph.small_y), id=str(ph.photo_id), weight=str(ph.weight), prod_id=str(product_id), path=path_prod))
        return data

class product_import(template_base):
    cls__title = u"Просмотр и изменение продуктов"
    cls__kwds = set([ 'product' ])
    cls__xsllist = [
        ('', '__root__.xsl'),
        ('body', 'import.xsl'),
        ('form', '__simpleedit__.xsl'),
    ]
    cls__externals = [
        '/css/main.css',
        '/extjs/resources/css/ext-all.css',
        '/extjs/resources/css/dd.css',
        '/extjs/adapter/ext/ext-base.js',
        '/extjs/ext-all-debug.js',
        #'/extjs/ext-all.js',
        '/js/private/show_category.js',
        '/js/private/import_product.js',
    ]
    
    class callback_form(form_base):
        fields = [
            field('product_id', 0, int, ValueError),
            field('choised_id', 0, int, ValueError),
            field('action',''),
            ]
        labels = {'choised_id': u'Выберите категорию'}
        ftypes = {'choised_id':'select'}
        def select_choised_id(self, field):
            options = []
            distrib_id =  self.template_ref().distrib_id
            if distrib_id:
                try:
                    category_id = self.template_ref().dbconn.query(Distributor).filter(Distributor.distrib_id == distrib_id).one().category_id
                except sqlalchemy.orm.exc.NoResultFound:
                    sys.exc_clear()
                    return E.options()
                categorys = self.template_ref().dbconn.query(Category).filter(Category.category_id == CategoryRev.child_id).filter(CategoryRev.parent_id == category_id).order_by('-name')
            else:
                categorys = self.template_ref().dbconn.query(Category).order_by('-name')
            self.template_ref().dbconn.rollback()
            for op in categorys:
                options.append(E.option(E.value(str(op.category_id)), op.name))
            return E.options(*options)
    def logic(self):
        sess = self.req.environ['rrduet.sess']
        self.distrib_id = sess['distrib_id']
        action = self.form['action']
        product_id = self.form['product_id']
        choised_id = self.form['choised_id']
        sess.update({'choised_id':choised_id})
        sess.save()
        dbconn = self.dbconn
        if action == 'delete':
            dbconn.query(Product).filter(Product.product_id == product_id).delete()
            dbconn.query(Tehnical).filter(Tehnical.product_id == product_id).delete()
            dbconn.query(Prod_more_category).filter(Prod_more_category.product_id == product_id).delete()
            dbconn.commit()


class manage_delivery_ajax(template_base):
    cls__kwds = set([ 'product' ])
    cls__application = 'ajax'
    def ajax(self):
        self.resp.content_type = 'application/xml'
        dbconn = self.dbconn
        self.xmlroot = self.data(dbconn)
    def data(self, dbconn):
        #выборка доступных категорий по category_id
        form = self.form
        ajax = [ E.delivery(
            E.delivery_id(str(r.price_delivery_id)),
            E.name(r.name),
#            E.discription(r.discription),
            delivery_id=str(r.price_delivery_id)) for r in dbconn.query(Price_delivery) ]
        return E.ajax(*ajax)
class manage_category_ajax(template_base):
    cls__kwds = set([ 'product' ])
    cls__application = 'ajax'
    def ajax(self):
        self.resp.content_type = 'application/xml'
        dbconn = self.dbconn
        self.xmlroot = self.data(dbconn)
    def data(self, dbconn):
        #выборка доступных категорий по category_id
        form = self.form
        ajax = [ E.category(
            E.category_id(str(r.category_id)),
            E.name(r.name),
#            E.discription(r.discription),
            category_id=str(r.category_id)) for r in dbconn.query(Category) ]
        return E.ajax(*ajax)

class product_import_ajax(template_base):
    cls__kwds = set([ 'product' ])
    cls__application = 'ajax'
    class callback_form(form_base):
        fields = [
            field('start', 0, lambda x: max(0, int(x)), ValueError),
            field('limit', 1, lambda x: min(30, max(1, int(x))), ValueError),
            field('query', ''),
            field('prod_id', 0, int, ValueError),
            field('name',''),
            field('sort',''),
            field('dir',''),
            field('articul',''),
            field('distrib', ''),
            field('discription',''),
            field('overview',''),
            field('price','0.00'),
            field('old_price','0.00'),
            field('vat','all'),
            field('sale_on','no'),
            field('bonus', 0, int, ValueError),
            field('price_delivery_id', ''),
            field('order_desk', 0, int, ValueError),
            field('prod_week', 'no'),
            field('spec', 'no'),
            field('popular', '0'),
            field('visible', 'open'),
            field('holiday', 'no'),
            field('metric', u''),
            field('action', ''),
        ]
    def ajax(self):
        self.resp.content_type = 'application/xml'
        form = self.form
        action = form['action']
        dbconn = self.dbconn
        if action == '':
            self.xmlroot = self.data(dbconn)
        elif action == 'config':
            self.xmlroot = self.config(dbconn)

    def data(self, dbconn):
        form = self.form
        sess = self.req.environ['rrduet.sess']
        distrib_id = sess['distrib_id']
        choised_id = sess['choised_id']
        delivery = dbconn.query(Price_delivery)
        where = [
            Product.distrib_id == Distributor.distrib_id,
            Price_delivery.price_delivery_id == Product.price_delivery_id
        ]
        query = dbconn.query(Product, Distributor.discription, Price_delivery.name).filter(Product.distrib_id == Distributor.distrib_id).filter(Price_delivery.price_delivery_id == Product.price_delivery_id)
        distrib = dbconn.query(Distributor)
        if distrib_id:
            query = query.filter(Product.distrib_id == distrib_id)
            distrib = distrib.filter(Distributor.distrib_id == distrib_id)
        if choised_id:
            t = tree_parser(dbconn)
            query = query.filter(Product.product_id == Prod_more_category.product_id).filter(Prod_more_category.category_id.in_(t.get_tree_child(choised_id)))
            distrib = distrib.filter(Distributor.category_id.in_(t.get_tree_parent(choised_id)))
        sort = form['sort']
        dir_ = form['dir']
        search = form['query']
        if search:
            query = query.filter(sqlalchemy.or_(
                Product.articul.contains(search),
                Product.name.contains(search),
            ))
        if sort and  dir_:
            if sort == 'distrib':
                sort = 'distrib_id'
            query = query.order_by('product_'+sort+' '+dir_)
        count = query.count()
        limit = form['limit']
        if limit:
            query = query.limit(limit)
            start = form['start']
            if start:
                query = query.offset(start)
        #выборка доступных категорий по category_id
        ajax = []
        for r in delivery:
            ajax.append(E.deliv(name=r.name, delivery_id=str(r.price_delivery_id)))
        for r in distrib:
            ajax.append(E.distr(name=r.discription, distrib_id=str(r.distrib_id)))
        for r in query:
            ajax.append(E.product(
            E.name(r[0].name),
            E.articul(r[0].articul),
            E.distrib(r[1]),
            E.discription(r[0].discription),
            E.overview(r[0].overview),
            E.price(str(r[0].price)),
            E.old_price(str(r[0].old_price)),
            E.vat(r[0].vat),
            E.sale_on(r[0].sale_on),
            E.bonus(str(r[0].bonus)),
            E.delivery(r[2]),
            E.order_desk(str(r[0].order_desk)),
            E.prod_week(str(r[0].prod_week)),
            E.spec(str(r[0].spec)),
            E.visible(r[0].visible),
            E.holiday(r[0].holiday),
            E.metric(r[0].metric),
            E.popular(str(r[0].popular)),
            prod_id=str(r[0].product_id)))
        ajax.append(E.totalCount(str(count)))
        return E.ajax(*ajax)


    def config(self, dbconn):
        sess = self.req.environ['rrduet.sess']
        distr_id = sess['distrib_id']
        form = self.form
        action = form['action']
        name = form['name']
        articul = form['articul']
        distrib_id = form['distrib']
        discription = form['discription']
        overview = form['overview']
        price = form['price']
        old_price = form['old_price']
        vat = form['vat']
        sale_on = form['sale_on']
        bonus = form['bonus']
        product_id = form['prod_id']
        order_desk = form['order_desk']
        delivery = form['price_delivery_id']
        prod_week = form['prod_week']
        popular = form['popular']
        visible = form['visible']
        holiday = form['holiday']
        metric = form['metric']
        spec = form ['spec']
        try:
            popular = int(popular)
        except:
            popular = 0
        if popular>500 or popular<0:
            popular = 0
        if distrib_id:
            distrib = dbconn.query(Distributor.distrib_id).filter(Distributor.discription == distrib_id)
            if distrib.count():
                form['distrib_id'] = distrib[0].distrib_id
            else:
                form['distrib_id'] = int(distrib_id)
        if delivery:
            deliv = dbconn.query(Price_delivery.price_delivery_id).filter(Price_delivery.name == delivery)
            if deliv.count():
                form['price_delivery_id'] = deliv[0].price_delivery_id
            else:
                form['price_delivery_id'] = int(delivery)
        if product_id == 0:
            self.admin_actions.append(('product add', 'ip=%s, articul= %s, oper=%s' % (self.req.environ['REMOTE_ADDR'], articul, sess['login']) ) )
            prod = Product(articul, distrib_id, name, discription, overview, price, old_price, delivery, vat, sale_on, prod_week, spec, bonus, order_desk, popular,"open", "no", metric)
            dbconn.add(prod)
            try:
                dbconn.commit()
            except:
                return E.ajax()
        else:
            try:
                prod = dbconn.query(Product).filter(Product.product_id == product_id).one()
            except sqlalchemy.orm.exc.NoResultFound:
                sys.exc_clear()
                return E.ajax()
            form.store_to_orm(prod)
            try:
                dbconn.commit()
                self.admin_actions.append(('product del', 'ip=%s, product_id= %s, oper=%s' % (self.req.environ['REMOTE_ADDR'],str(product_id), sess['login']) ) )
            except:
                return E.ajax()
        return E.ajax()

class product_download(template_base):
    cls__kwds = set([ 'product' ])
    cls__title = u"Импорт товаров из csv"
    cls__xsllist = [
        ('', '__root__.xsl'),
        ('body', 'import_csv.xsl'),
        ('form', '__simpleedit__.xsl'),
    ]
    cls__externals = [
        '/css/main.css',
        '/extjs/resources/css/ext-all.css',
        '/extjs/resources/css/dd.css',
        '/extjs/adapter/ext/ext-base.js',
        '/extjs/ext-all-debug.js',
        #'/extjs/ext-all.js',
        '/js/private/show_delivery.js',
        '/js/private/show_category.js',
    ]

    class callback_form(form_base):
        fields = [
            field('file_csv', None, complexity=True),
            field('codding', ''),
            field('distrib', ''),
            field('separate', ''),
        ]
        labels = {
            'file_csv': u'Выберите csv файл',
            'codding': u'Выберите кодировку',
            'distrib': u'Выберите поставку',
            'separate': u'Выберите разделитель',
        }
        ftypes = {
            'file_csv': 'file',
            'codding': 'select',
            'distrib': 'select',
            'separate': 'select',
        }
        def select_codding(self, field):
            return E.options(E.option(E.value('cp1251'), u'cp1251'),
                            E.option(E.value('utf8'), u'utf8'), 
                            E.option(E.value('koi8-r'), u'koi8-r'),
                            E.option(E.value('ibm866'), u'ibm866'), 
                            )
        def select_separate(self, field):
            return E.options(E.option(E.value(';'), u';'),
                            E.option(E.value(','), u','), 
                            E.option(E.value('tab'), u'табуляция'), 
                            )

        def select_distrib(self, field):
            options = []
            distrib_id =  self.template_ref().distrib_id
            if distrib_id:
                try:
                    distrib_name =  self.template_ref().dbconn.query(Category.name).filter(sqlalchemy.and_(Distributor.distrib_id == distrib_id, Category.category_id == Distributor.category_id)).one()
                except sqlalchemy.orm.exc.NoResultFound:
                    sys.exc_clear()
                    return E.options()
                return  E.options(E.option(E.value(str(distrib_id)), distrib_name[0]))
            else:
                for r in self.template_ref().dbconn.query(Distributor.distrib_id, Category.name).filter(Distributor.category_id == Category.category_id):
                    options.append(E.option(E.value(str(r.distrib_id)), r.name))
                return E.options(*options)
    def E_form(self):
        return template_base.E_form(self, multipart='yes')
    
    def logic(self):
        import tempfile
        import csv
        
        sess = self.req.environ['rrduet.sess']
        self.distrib_id = sess['distrib_id']
        form = self.form
        dbconn = self.dbconn 
        separate = form ['separate']
        if separate == 'tab':
            dialect ='excel-tab'
        else:
            dialect = 'excel'
        codding = form['codding']
        distrib_id = form['distrib']
        if form['file_csv'] is None:
            return
        else:
            f = form['file_csv'].file
            content = f.read() 
#            content = content.read()
            (fd, fname) = tempfile.mkstemp(prefix='import', suffix='.csv', dir=htdocs_dir+'/csv/')
            temp = open(fname, 'w')
            temp.write(content)
            temp.close()
            self.resp.location = '/private/product/test?csv=%s&codding=%s&separate=%s&distrib_id=%s' % (fname, codding, separate, distrib_id)
            self.resp.status_int = 302
            self.resp.body = ''
            form['file_csv'] = None
            return 

class product_test(template_base):
    cls__kwds = set([ 'product' ])
    cls__title = u"Импорт товаров из csv"
    cls__xsllist = [
        ('', '__root__.xsl'),
        ('body', 'test.xsl'),
    ]
    class callback_form(form_base):
        fields = [
            field('csv', ''),
            field('codding', ''),
            field('distrib_id', ''),
            field('separate', ''),
            field('action', ''),
        ]
    def E_data(self):
        import csv
        dbconn = self.dbconn
        form = self.form
        fname = form ['csv']
        codding = form ['codding']
        separate = form ['separate']
        distrib_id = form['distrib_id']
        action = form['action']
        f = open(fname, 'r')
        if separate == 'tab':
            dialect = 'excel-tab'
        else:
            dialect = 'excel'
        if dialect == 'excel-tab':
            reader = csv.reader(f, dialect=dialect)
        else:
            try:
                reader = csv.reader(f, dialect=dialect, delimiter=str(separate))
            except:
                reader = csv.reader(f, dialect=dialect, delimiter=';')
        test = list(reader)
        test_map = ['articul', 'name', 'overview', 'discription', 'delivery', 'vat', 'sale', 'week', 'order_desk', 'bonus', 'spec', 'price', 'price_old', 'params', 'category']
        key_map = test[0]
        if len(key_map) < 2:
            key_map = key_map[0].split(',')
        for k in range(len(key_map)):
            key_map[k] = key_map[k].strip()
        check = True
        for i in test_map:
            if i not in key_map:
                check = False
        if len(key_map)<15 or not check:
            self.errors.append(u'Не верный формат строки заголовков таблицы. Составьте строку заголовков согласно инструкции.')
            return E.data()
        data = E.data(fname=fname, codding=codding,separate=separate, distrib_id=distrib_id)
        data_tag = data.xpath('//data')[0]
        if test[1]:
            if len(test[1])<2:
                self.errors.append(u'Неверно указан разделитель')
                return E.data()
        for i in range(1, len(test)):
            p = {}
            for k in key_map:
                index = key_map.index(k)
                try:
                    p[k] = test[i][index].decode(codding)
                except:
                    self.errors.append(u'Неверно указана кодировка.')
                    return E.data()
            params = p['params'].split(',')
            category = p['category'].split(',')
            data_tag.append(E.product(articul=p['articul'],
                    name = p['name'], 
                    discription = p['discription'],
                    overview = p['overview'],
                    price = p['price'],
                    price_old = p['price_old'],
                    delivery = p['delivery'],
                    vat = p['vat'],
                    sale = p['sale'],
                    week = p['week'],
                    spec = p['spec'],
                    bonus = p['bonus'],
                    order_desk = p['order_desk'],
                    params = p['params'],
                    category = p['category'],
                    )) 
            if action:
                product = Product(p['articul'],
                    distrib_id,
                    p['name'], 
                    p['discription'],
                    p['overview'],
                    p['price'],
                    p['price_old'],
                    p['delivery'],
                    p['vat'],
                    p['sale'],
                    p['week'],
                    p['spec'],
                    p['bonus'],
                    p['order_desk'],
                    0,
                    "open") 
                dbconn.add(product)
                do = False
                try:
                    dbconn.commit()
                    do = True
                except sqlalchemy.exc.SQLAlchemyError:
                    dbconn.rollback()
                    self.errors.append(u'Продукт %s с артикулом %s не добавлен. Конфликт имен. Проверьте артикул или номер поставки'% (p['name'],p['articul'
                    ]))
                if do:
                    if params != ['']:
                        params_new = []
                        for pp in params:
                            if ':' in pp or not len(params_new):
                                params_new.append(pp)
                            else:
                                params_new[-1] = ",".join((params_new[-1], pp))
                        for pp in params_new:
                            try:
                                name, value = pp.split(':')
                                techical = Tehnical(product.product_id, name, value)
                                dbconn.add(techical)
                            except:
                                self.errors.append(u'Товар с артикулом %s. Ошибка в формате технический характеристик (не указана ",").'% (p['articul']))
                    if category != ['']:
                        for c in category:
                            cat = Prod_more_category(c, product.product_id, 0)
                            dbconn.add(cat)
                    else:
                        try:
                            c = dbconn.query(Distributor.category_id).filter(Distributor.distrib_id == distrib_id).one()[0]
                        except sqlalchemy.orm.exc.NoResultFound:
                            sys.exc_clear()
                            return data
                        cat = Prod_more_category(c, product.product_id, 0)
                        dbconn.add(cat)
                    try:
                        dbconn.commit()
                    except sqlalchemy.exc.SQLAlchemyError:
                        dbconn.rollback() 
                        self.errors.append(u'Ошибка при загрузке техническийх характеристик и категории для товара с артикулом %s'% (p['articul']))
        if action:
            self.results.append(u'Загрузка данных закончена. Добавлено %s из %s продуктов' % (str(len(test)-len(self.errors)-1),str(len(test)-1)))
        return data

class product_change_download(template_base):
    cls__kwds = set([ 'product' ])
    cls__title = u"Изменение товаров из csv"
    cls__xsllist = [
        ('', '__root__.xsl'),
        ('body', 'import_csv.xsl'),
        ('form', '__simpleedit__.xsl'),
    ]
    cls__externals = [
        '/css/main.css',
        '/extjs/resources/css/ext-all.css',
        '/extjs/resources/css/dd.css',
        '/extjs/adapter/ext/ext-base.js',
        '/extjs/ext-all-debug.js',
        #'/extjs/ext-all.js',
        '/js/private/show_delivery.js',
        '/js/private/show_category.js',
    ]

    class callback_form(form_base):
        fields = [
            field('file_csv', None, complexity=True),
            field('codding', ''),
            field('distrib', ''),
            field('separate', ''),
        ]
        labels = {
            'file_csv': u'Выберите csv файл',
            'codding': u'Выберите кодировку',
            'distrib': u'Выберите поставку',
            'separate': u'Выберите разделитель',
        }
        ftypes = {
            'file_csv': 'file',
            'codding': 'select',
            'distrib': 'select',
            'separate': 'select',
        }
        def select_codding(self, field):
            return E.options(E.option(E.value('cp1251'), u'cp1251'),
                            E.option(E.value('utf8'), u'utf8'), 
                            E.option(E.value('koi8-r'), u'koi8-r'),
                            E.option(E.value('ibm866'), u'ibm866'), 
                            )
        def select_separate(self, field):
            return E.options(E.option(E.value(';'), u';'),
                            E.option(E.value(','), u','), 
                            E.option(E.value('tab'), u'табуляция'), 
                            )

        def select_distrib(self, field):
            options = []
            distrib_id =  self.template_ref().distrib_id
            if distrib_id:
                try:
                    distrib_name =  self.template_ref().dbconn.query(Category.name).filter(sqlalchemy.and_(Distributor.distrib_id == distrib_id, Category.category_id == Distributor.category_id)).one()
                except sqlalchemy.orm.exc.NoResultFound:
                    sys.exc_clear()
                    return E.options()
                return  E.options(E.option(E.value(str(distrib_id)), distrib_name[0]))
            else:
                for r in self.template_ref().dbconn.query(Distributor.distrib_id, Category.name).filter(Distributor.category_id == Category.category_id):
                    options.append(E.option(E.value(str(r.distrib_id)), r.name))
                return E.options(*options)
    def E_form(self):
        return template_base.E_form(self, multipart='yes')
    
    def logic(self):
        import tempfile
        import csv
        
        sess = self.req.environ['rrduet.sess']
        self.distrib_id = sess['distrib_id']
        form = self.form
        dbconn = self.dbconn 
        separate = form ['separate']
        if separate == 'tab':
            dialect ='excel-tab'
        else:
            dialect = 'excel'
        codding = form['codding']
        distrib_id = form['distrib']
        if form['file_csv'] is None:
            return
        else:
            f = form['file_csv'].file
            content = f.read() 
#            content = content.read()
            tempfd, fname = tempfile.mkstemp(prefix='change', suffix='.csv', dir=htdocs_dir+'/csv/')
            temp = os.fdopen(tempfd, "w")
            temp.write(content)
            temp.close()
            del temp
            self.resp.location = '/private/product/test_change?csv=%s&codding=%s&separate=%s&distrib_id=%s' % (fname, codding, separate, distrib_id)
            self.resp.status_int = 302
            self.resp.body = ''
            form['file_csv'] = None
            return 

class product_change_test(template_base):
    cls__kwds = set([ 'product' ])
    cls__title = u"Изменение товаров из csv"
    cls__xsllist = [
        ('', '__root__.xsl'),
        ('body', 'test.xsl'),
    ]
    class callback_form(form_base):
        fields = [
            field('csv', ''),
            field('codding', ''),
            field('distrib_id', 0, lambda x: max(0, int(x)), (ValueError,)),
            field('separate', ''),
            field('action', ''),
        ]
    def E_data(self):
        import csv
        dbconn = self.dbconn
        form = self.form
        fname = form ['csv']
        codding = form ['codding']
        separate = form ['separate']
        distrib_id = form['distrib_id']
        if not distrib_id:
            return E.data()
        cats_distrib = [r[0] for r in list(dbconn.query(CategoryRev.child_id).filter(CategoryRev.parent_id==Distributor.category_id).filter(Distributor.distrib_id==distrib_id))]
        dbconn.execute("update product, distributor set product.visible='close' where product.distrib_id=distributor.distrib_id and distributor.zip_visible='yes' and distributor.distrib_id=%d" % (
            distrib_id,
        ))
        action = form['action']
        f = open(fname, 'r')
        if separate == 'tab':
            dialect = 'excel-tab'
        else:
            dialect = 'excel'
        reader = None
        if dialect == 'excel-tab':
            reader = csv.reader(f, dialect=dialect, lineterminator='\r\n')
        else:
            try:
                reader = csv.reader(f, dialect=dialect, delimiter=str(separate), lineterminator='\r\n')
            except:
                reader = csv.reader(f, dialect=dialect, delimiter=';', lineterminator='\r\n')
        if reader is None:
            self.errors.append(u"Не удалось открыть файл. Попробуйте еще раз или свяжитесь с разработчиком.")
            return E.data()
        it = iter(reader)
        fline = reader.next()
        keys = [
            'articul',
            'name',
            'overview',
            'discription',
            'delivery',
            'vat',
            'sale',
            'week',
            'order_desk',
            'bonus',
            'spec',
            'price',
            'price_old',
            'params',
            'category',
            'visible',
            'holiday',
            'metric',
            'kw',
            'complements',
            'profit',
            'procent'
        ]
        keyslen = len(keys)
        for i, k in enumerate(fline):
            fline[i] = k.strip()
        if len(fline) == 1:
            fline = fline[0].split(',')
        elif not fline:
            self.errors.append(u"Неверный формат строки заголовка")
            return E.data()
        check = True
        if (set(keys)&set(fline)) != set(keys) or (set(keys)|set(fline)) != set(keys):
            self.errors.append(u"Неверный формат строки заголовков таблицы. Составьте строку заголовков согласно инструкции. Обратите внимание на новое поле 'metric'")
#            print keys, fline
            return E.data()
        data = E.data(fname=fname, codding=codding, separate=separate, distrib_id=str(distrib_id))
        count_old = count_new = 0
        lines = []
        for i, line in enumerate(it):
            if len(line) != keyslen:
                self.errors.append(u"Неверное количество полей в строке %d" % (i,))
                return E.data()
            kw = {}
            for k, v in zip(fline, line):
                if k == 'visible':
                    if v == 'close':
                        kw[k] = v
                    else:
                        kw[k] = 'open'
                elif k == 'holiday':
                    if v == 'yes':
                        kw[k] = v
                    else:
                        kw[k] = 'no'
                elif k == 'delivery':
                    if v in ('1', '7'):
                        kw[k] = v
                    else:
                        kw[k] = '1'
                elif k in ('price', 'price_old', 'profit', 'procent'):
                    v = v.replace(' ','').replace('/', '.').replace(',', '.')
                    if v  == '':
                        v = 0.0
                    try:
                        kw[k] = float(v)
                    except ValueError:
                        self.errors.append(u"Старая цена должна быть задана числовым значением (строка %d, столбец '%s' (%d)), art %s." % (
                            i, chr(ord('A') + fline.index(k)), fline.index(k) , str(kw['articul'])))
                        return E.data()
                else:
                    try:
                        kw[k] = v.decode(codding).strip()
                    except UnicodeDecodeError:
                        self.errors.append(u"Неверно указана кодировка (строка %d, столбец '%s' (%d))." % ( i, chr(ord('A') + fline.index(k)), fline.index(k) ))
                        return E.data()
            lines.append(kw)
            data.append(E.product(**kw2strval(kw)))
        if action != 'commit':
            return data
        sess = self.req.environ['rrduet.sess']
        self.admin_actions.append(('download changes', 'ip=%s, distrib= %s, oper=%s, css=%s' % (self.req.environ['REMOTE_ADDR'], str(distrib_id), sess['login'], fname) ) )
        for lineno, kw in enumerate(lines):
            have_error = False
            params = kw.pop('params')
            category = kw.pop('category')
            kws = kw.pop('kw')
            complements = kw.pop('complements')
            try:
                dbconn.rollback()
                product = dbconn.query(Product).filter(Product.distrib_id == distrib_id).filter(Product.articul == kw['articul']).one()
            except sqlalchemy.orm.exc.NoResultFound:
                sys.exc_clear()
                product = Product(distrib_id=distrib_id, popular=0, **kw)
                dbconn.add(product)
                try:
                    dbconn.commit()
                    count_new += 1
                except sqlalchemy.exc.SQLAlchemyError:
                    dbconn.rollback()
                    have_error = True
            else:
                product.name = kw['name']
                product.discription = kw['discription']
                product.overview = kw['overview']
                product.price = kw['price']
                product.old_price = kw['price_old']
                product.price_delivery_id = kw['delivery']
                product.vat = kw['vat']
                product.sale_on = kw['sale']
                product.prod_week = kw['week']
                product.spec = kw['spec']
                product.bonus = kw['bonus']
                product.order_desk = kw['order_desk']
                product.visible = kw['visible'] 
                product.holiday = kw['holiday']
                product.metric = kw['metric']
                product.procent = kw['procent']
                product.profit = kw['profit']
                try:
                    dbconn.commit()
                    count_old += 1
                except sqlalchemy.exc.SQLAlchemyError:
                    dbconn.rollback()
                    self.errors.append(u"Продукт '%s' с артикулом '%s' не изменен. Конфликт имен. Проверьте артикул или номер поставки (строка номер %d)" % (
                        kw['name'],
                        kw['articul'],
                        lineno,
                    ))
                    have_error = True
            if not have_error:
                if params:
                    for param in params.split('|'):
                        toks = param.split(':')
                        if len(toks) != 2:
                            self.errors.append(u"Неверный формат параметра в графе params для продукта с артикулом '%s'. В значении параметра знаки ':' и '|' недопустимы (строка %d)." % (
                                kw['articul'],
                                lineno,
                            ))
                            continue
                        name, value = map(lambda x: x.strip(), toks)
                        try:
                            technical = dbconn.query(Tehnical).filter(Tehnical.product_id == product.product_id).filter(Tehnical.name == name).one()
                            technical.value = value
                        except sqlalchemy.orm.exc.NoResultFound:
                            sys.exc_clear()
                            technical = Tehnical(product.product_id, name, value)
                            dbconn.add(technical)
                        try:
                            dbconn.commit()
                        except sqlalchemy.exc.SQLAlchemyError:
                            have_error = True
                            dbconn.rollback()
                if 1 and kws:
                    kws_old = [r[0] for r in list(dbconn.query(Prod_kw.kw).filter(Prod_kw.product_id == product.product_id))]
                    kws = kws.split(' ')
                    for kw_ in kws:
                        if kw_:
                            kw_ = kw_.strip()
                            if kw_ not in kws_old:
                                dbconn.add(Prod_kw(product.product_id, kw_))
                            try:
                                dbconn.commit()
                            except  sqlalchemy.exc.SQLAlchemyError:
                                dbconn.rollback()
                if 1 and complements:
                    compls_old = [r[0] for r in list(dbconn.query(Compl.product_id).filter(Compl.prod_id == product.product_id))]
                    complements = complements.split(',')
                    for complement in complements:
                        complement = complement.strip()
                        if complement not in compls_old:
                            dbconn.add(Compl(product.product_id, complement))
                        try:
                            dbconn.commit()
                        except sqlalchemy.exc.SQLAlchemyError:
                            dbconn.rollback()

                if category:
                    cats_old = [r[0] for r in list(dbconn.query(Prod_more_category.category_id).filter(Prod_more_category.product_id == product.product_id))]
                    try:
                        category_ids = [ int(c.strip()) for c in category.split(',') ]
                    except ValueError:
                        sys.exc_clear()
                        self.errors.append(u"Для категории должны быть заданы числовые идентификаторы, разделеные запятой (дано '%s' для строки %d)" % (
                            category,
                            lineno,
                        ))
                        continue
                    for category_id in category_ids:
                        if  category_id not in cats_old and category_id in cats_distrib:
                            cat = Prod_more_category(category_id, product.product_id, 50)
                            dbconn.add(cat)
                        try:
                            dbconn.commit()
                        except sqlalchemy.exc.SQLAlchemyError:
                            dbconn.rollback()
                else:
                    try:
                        category_id = dbconn.query(Distributor.category_id).filter(Distributor.distrib_id == distrib_id).one()[0]
                    except sqlalchemy.orm.exc.NoResultFound:
                        sys.exc_clear()
                    else:
                        cat = Prod_more_category(category_id, product.product_id, 0)
                        dbconn.add(cat)
                        try:
                            dbconn.commit()
                        except sqlalchemy.exc.SQLAlchemyError:
                            dbconn.rollback()
        self.results.append(u'Загрузка данных закончена. Изменено %s. Добавлено %s. Всего %s' % (str(count_old), str(count_new), str(len(lines))))
        return data


class product_zip(template_base):
    cls__kwds = set([ 'product' ])
    cls__title = u"Загрузка фотографий из архива"
    cls__xsllist = [
        ('', '__root__.xsl'),
        ('body', 'import_zip.xsl'),
        ('form', '__simpleedit__.xsl'),
    ]

    class callback_form(form_base):
        fields = [
            field('zip', None, complexity=True),
            field('distrib', ''),
            field('separate', ','),
            field('codding', ','),
        ]
        labels = {
            'zip': u'Выберите архив',
            'distrib': u'Выберите поставку',
            'separate': u'Выберите разделитель',
            'codding': u'Выберите кодировку',
        }
        ftypes = {
            'zip': 'file',
            'distrib': 'select',
            'separate': 'select',
            'codding': 'select',
        }
        
        def select_codding(self, field):
            return E.options(E.option(E.value('cp1251'), u'cp1251'),
                            E.option(E.value('utf8'), u'utf8'), 
                            E.option(E.value('koi8-r'), u'koi8-r'),
                            E.option(E.value('ibm866'), u'ibm866'), 
                            )
        def select_distrib(self, field):
            options = []
            distrib_id =  self.template_ref().distrib_id
            if distrib_id:
                try:
                    distrib_name =  self.template_ref().dbconn.query(Category.name).filter(sqlalchemy.and_(Distributor.distrib_id == distrib_id, Category.category_id == Distributor.category_id)).one()
                except sqlalchemy.orm.exc.NoResultFound:
                    sys.exc_clear()
                    return E.options()
                return  E.options(E.option(E.value(str(distrib_id)), distrib_name[0]))
            else:
                for r in self.template_ref().dbconn.query(Distributor.distrib_id, Category.name).filter(Distributor.category_id == Category.category_id):
                    options.append(E.option(E.value(str(r.distrib_id)), r.name))
                return E.options(*options)
        def select_separate(self, field):
            return E.options(E.option(E.value(';'), u';'),
                            E.option(E.value(','), u','), 
                            E.option(E.value('tab'), u'табуляция'), 
                            )

    def E_form(self):
        return template_base.E_form(self, multipart='yes')
    
    def logic(self):
        import zipfile
        import csv
        import Image
        import cStringIO
        map_ = {'tab':'excel-tab', ',':'excel', ';':'excel'}
        form = self.form
        dbconn = self.dbconn
        separate = form['separate']
        codding = form['codding']
        self.distrib_id = distrib_id = form['distrib']
        if form['zip'] is None:
            return
        f = form['zip'].file
        try:
            zip_photo = zipfile.ZipFile(f, 'r')
        except:
            self.errors.append(u'Архив должен иметь формат zip.')
            return
        csv_file = None
        for info in zip_photo.infolist():
            try:
                if info.filename.split('.')[-1:] == ['csv']:
                   csv_file = info.filename
            except:
                self.errors.append(u'Содержание архива не отвечает требованиям загрузки.')
        if not csv_file:
            self.errors.append(u'Архив должен содержать csv файл с указанием артикула товара и фотографии')
            return
        f =  zip_photo.read(csv_file)
        if separate == 'tab':
            reader = csv.reader(cStringIO.StringIO(f), dialect=map_[separate])
        elif separate == ';':
            reader = csv.reader(cStringIO.StringIO(f), dialect=map_[separate], delimiter=';')
        else:
            reader = csv.reader(cStringIO.StringIO(f), dialect=map_[separate], delimiter=',')
        test = list(reader)
        test_map = ['articul', 'name']
        key_map = test[0]
        check = True
        config_x = config_y = 100
        config_x_m = config_y_m = 200
        for k in range(len(key_map)):
            key_map[k] = key_map[k].strip().replace("*", "")
        for i in test_map:
            if i not in key_map:
                check = False
        if len(key_map)<2 or not check:
            self.errors.append(u'Не верный формат строки заголовков таблицы. Составьте строку заголовков согласно инструкции.')
            return 
        count = 0
        all_count = 0
#        for i in zip_photo.filelist:
#            print i.filename
        for i in range(1, len(test)):
            p = {}
            for k in key_map:
                index = key_map.index(k)
                p[k] = test[i][index]
            names = p['name'].split(",")
            max_weight = len(names)
            for i_weight, name in enumerate(names):
                weight = (max_weight-i_weight)*100
                name = name.strip()
                try:
                    photo_name = name.decode(codding)
                except:
                    sys.exc_clear()
                    self.errors.append(u'Неверно указана кодировка')
                    return
                all_count += 1
                try:
                    img = zip_photo.read(name)
                    img = Image.open(cStringIO.StringIO(img))
                    width, height = img.size
                    small_x, small_y = resize_photo(width, height, config_x, config_y)
                    small_x_m, small_y_m = resize_photo(width, height, config_x_m, config_y_m)
                    try:
                        product_id = dbconn.query(Product).filter(sqlalchemy.and_(Product.articul == p['articul'].decode(codding), Product.distrib_id == distrib_id)).one().product_id
                        do = True
                        try:
                            photo = dbconn.query(Photo).filter(Photo.product_id == product_id).filter(Photo.photo_name == photo_name)
                            if len(list(photo)) != 0:
                                do =  False
                        except sqlalchemy.orm.exc.NoResultFound:
                            sys.exc_clear()
                        if do:
                            photo = Photo(product_id, small_x, small_y, width, height, weight, photo_name, small_x_m, small_y_m)
                            dbconn.add(photo)
                            dbconn.commit()
                            count += 1
                            file_name = str(photo.photo_id)
                            path_prod = os.path.dirname(ppath.get(photo.photo_id))+'/'
                            try:
                                os.makedirs(os.path.dirname(path_prod), 0755)
                            except OSError:
                                sys.exc_clear()
                            img.save(path_prod+file_name+'.png')
                            img_s = img.resize((small_x, small_y), Image.ANTIALIAS)
                            img_s.save(path_prod+file_name+'_small.png')

                            img_m = img.resize((small_x_m, small_y_m), Image.ANTIALIAS)
                            img_m.save(path_prod+file_name+'_med.png')

                            self.results.append(u"Фото для товара с артикулом %s загружено" % p['articul'].decode(codding))
                    except sqlalchemy.orm.exc.NoResultFound:
                        sys.exc_clear()
                        self.errors.append(u'Не найден продукт для данной поставки с артикулом %s' % p['articul'].decode(codding))
                except:
                    try:
                        self.errors.append(u'В архиве отсутсвет фото %s'% name.decode(codding))
                    except:
                        try:
                            self.errors.append(u'В архиве отсутсвет фото для продукта с артикулом %s'% p['articul'].decode(codding))
                            print p['articul'].decode(codding)
                        except:
                            self.errors.append(u'Неверно указана кодировка')
        self.results.append(u'Загрузка фотографий завершена. Загружено %s из %s' % (str(count), str(all_count)))


class product_params(template_base):
    cls__kwds = set([ 'product' ])
    cls__title = u"Характеристики товара"
    cls__xsllist = [
        ('', '__root__.xsl'),
        ('body', 'product_params.xsl'),
        ('form', '__simpleedit__.xsl'),
    ]
    class callback_form(form_base):
        fields = [
            field('product_id', 0, int, ValueError),
            field('params', 0, int, ValueError),
            field('name',''),
            field('value',''),
            field('action',''),
            ]
        labels = {'name':u'Значение параметра',
                  'value':u''
                  }

    def logic(self):
        action = self.form['action']
        product_id = self.form['product_id']
        name = self.form['name']
        value = self.form['value']
        self.form['action'] = 'check'
        dbconn = self.dbconn
        if action == 'check':
            if name and value:
                tehnical = Tehnical(product_id, name, value)
                dbconn.add(tehnical)
                dbconn.commit()
            else:
                self.errors.append(u'не все поля были заполнены')
        elif self.form['params']:
            try:
                tehnical = dbconn.query(Tehnical).filter(Tehnical.technical_id == self.form['params']).one()
            except sqlalchemy.orm.exc.NoResultFound:
                sys.exc_clear()
                return
            dbconn.delete(tehnical)
            dbconn.commit()
        return


    def E_data(self):
        dbconn = self.dbconn
        tehnical = dbconn.query(Tehnical).filter(Tehnical.product_id == self.form['product_id'])
        data = E.data()
        data_tag = data.xpath('//data')[0]
        for t in tehnical:
            data_tag.append(E.tehnical(name=t.name, value=str(t.value), id=str(t.technical_id), prod=str(self.form['product_id'])))
        return data

class product_category(template_base):
    cls__kwds = set([ 'product' ])
    cls__title = u"Отображение товара"
    cls__xsllist = [
        ('', '__root__.xsl'),
        ('body', 'product_category.xsl'),
        ('form', '__simpleedit__.xsl'),
    ]
    cls__externals = [
        '/css/main.css',
        '/extjs/resources/css/ext-all.css',
        '/extjs/resources/css/dd.css',
        '/extjs/adapter/ext/ext-base.js',
        '/extjs/ext-all-debug.js',
        #'/extjs/ext-all.js',
        '/js/private/show_category.js',
    ]
    class callback_form(form_base):
        fields = [
            field('product_id', 0, int, ValueError),
            field('category_id',0, int, ValueError),
            field('params', 0, int, ValueError),
            field('action',''),
            ]
        labels = {'category_id':u'Выберите категорию',
                  }
        ftypes = {'category_id': 'select'}

        def select_category_id(self, field):
            options = []
            for r in self.template_ref().dbconn.query(Category).all():
                options.append(E.option(E.value(str(r.category_id)), r.name))
            return E.options(*options)

    def logic(self):
        action = self.form['action']
        product_id = self.form['product_id']
        category_id = self.form['category_id']
        self.form['action'] = 'check'
        dbconn = self.dbconn
        if action == 'check':
            weight = 0
            if category_id:
                prod_more_category = Prod_more_category(category_id, product_id, weight)
                dbconn.add(prod_more_category)
                dbconn.commit()
            else:
                self.errors.append(u'не все поля были заполнены')
        elif self.form['params']:
            try:
                prod_more_category = dbconn.query(Prod_more_category).filter(Prod_more_category.prod_more_category_id == self.form['params']).one()
            except sqlalchemy.orm.exc.NoResultFound:
                sys.exc_clear()
                return
            dbconn.delete(prod_more_category)
            dbconn.commit()
        return


    def E_data(self):
        dbconn = self.dbconn
        category = dbconn.query(Category.name, Prod_more_category.prod_more_category_id).filter(sqlalchemy.and_(Prod_more_category.product_id == self.form['product_id'], Prod_more_category.category_id == Category.category_id))
        data = E.data()
        data_tag = data.xpath('//data')[0]
        for name, prod_more_category_id in category:
            data_tag.append(E.category(name=name, id=str(prod_more_category_id), prod=str(self.form['product_id'])))
        return data

class product_kw(template_base):
    cls__kwds = set([ 'product' ])
    cls__title = u"Ключевые слова"
    cls__xsllist = [
        ('', '__root__.xsl'),
        ('body', 'product_kw.xsl'),
        ('form', '__simpleedit__.xsl'),
    ]
    class callback_form(form_base):
        fields = [
            field('product_id', 0, int, ValueError),
            field('prod_kw_id', 0, int, ValueError),
            field('kw',''),
            field('action',''),
            ]
        labels = {'kw':u'Ключевое слово',
                  }

    def logic(self):
        action = self.form['action']
        product_id = self.form['product_id']
        prod_kw_id = self.form['prod_kw_id']
        kw = self.form['kw']
        self.form['action'] = 'check'
        dbconn = self.dbconn
        if action == 'check':
            if prod_kw_id:
                try:
                    kw_db = dbconn.query(Prod_kw).filter(Prod_kw.prod_kw_id == prod_kw_id).one()
                    kw_db.kw = kw
                    try:
                        dbconn.commit()
                        self.results.append(u"Заспись успешно изменена.")
                    except:
                        self.errors.append(u"Конфликт имен.")
                except sqlalchemy.orm.exc.NoResultFound:
                    sys.exc_clear()
            elif kw:
                try:
                    kw_db = dbconn.query(Prod_kw).filter(Prod_kw.product_id == product_id).filter(Prod_kw.kw == kw).one()
                    self.errors.append(u"Конфликт имен.")
                except sqlalchemy.orm.exc.NoResultFound:
                    sys.exc_clear()
                    new_kw = Prod_kw(product_id, kw)
                    dbconn.add(new_kw)
                    try:
                        dbconn.commit()
                        self.results.append(u"Заспись успешно добавлена.")
                    except:
                        self.errors.append(u"Конфликт имен.")
        elif action == 'del' and prod_kw_id:
            try:
                kw_db = dbconn.query(Prod_kw).filter(Prod_kw.prod_kw_id == prod_kw_id).one()
                self.form['action']=''
                self.form['product_id'] = kw_db.product_id
                self.form['prod_kw_id'] = 0
                dbconn.delete(kw_db)
                dbconn.commit()
                self.results.append(u"Ключевое слово удалено.")
            except sqlalchemy.orm.exc.NoResultFound:
                sys.exc_clear()
        elif prod_kw_id:
            try:
                kw_db = dbconn.query(Prod_kw).filter(Prod_kw.prod_kw_id == prod_kw_id).one()
                self.form['kw'] = kw_db.kw
                self.form['product_id'] = kw_db.product_id
            except sqlalchemy.orm.exc.NoResultFound:
                sys.exc_clear()
                self.errots.append(u"Ключевое слово не найдено.")
        return


    def E_data(self):
        dbconn = self.dbconn
        kws = dbconn.query(Prod_kw).filter(Prod_kw.product_id == self.form['product_id'])
        data = E.data(product_id=str(self.form['product_id']))
        data_tag = data.xpath('//data')[0]
        for kw in kws:
            data_tag.append(E.kw(kw=kw.kw, prod_kw_id=str(kw.prod_kw_id), product_id=str(kw.product_id)))
        return data

class product_more(template_base):
    cls__kwds = set([ 'product' ])
    cls__title = u"Дополнительные товары"
    cls__xsllist = [
        ('', '__root__.xsl'),
        ('body', 'product_compl.xsl'),
        ('form', '__simpleedit__.xsl'),
    ]
    class callback_form(form_base):
        fields = [
            field('prod_id', 0, int, ValueError),
            field('compl_id', 0, int, ValueError),
            field('articul',''),
            field('action',''),
            ]
        labels = {'articul':u'Артикул товара',
                  }

    def logic(self):
        action = self.form['action']
        prod_id = self.form['prod_id']
        compl_id = self.form['compl_id']
        articul = self.form['articul']
        self.form['action'] = 'check'
        dbconn = self.dbconn
        if action == 'check':
            if compl_id:
                try:
                    compl = dbconn.query(Compl).filter(Compl.compl_id == compl_id).one()
                    compl.product_id = articul
                    try:
                        dbconn.commit()
                        self.results.append(u"Заспись успешно изменена.")
                    except:
                        dbconn.rollback()
                        self.errors.append(u"Конфликт имен.")
                except sqlalchemy.orm.exc.NoResultFound:
                    sys.exc_clear()
            elif articul:
                try:
                    compl = dbconn.query(Compl).filter(Compl.prod_id == prod_id).filter(Compl.product_id == articul).one()
                    self.errors.append(u"Конфликт имен.")
                except sqlalchemy.orm.exc.NoResultFound:
                    sys.exc_clear()
                    new_compl = Compl(prod_id, articul)
                    dbconn.add(new_compl)
                    try:
                        dbconn.commit()
                        self.results.append(u"Заспись успешно добавлена.")
                    except:
                        dbconn.rollback()
                        self.errors.append(u"Конфликт имен.")
        elif action == 'del' and compl_id:
            try:
                compl = dbconn.query(Compl).filter(Compl.compl_id == compl_id).one()
                self.form['action']=''
                self.form['prod_id'] = compl.prod_id
                self.form['compl_id'] = 0
                dbconn.delete(compl)
                dbconn.commit()
                self.results.append(u"Запись удалена.")
            except sqlalchemy.orm.exc.NoResultFound:
                sys.exc_clear()
        elif compl_id:
            try:
                compl = dbconn.query(Compl).filter(Compl.compl_id == compl_id).one()
                self.form['articul'] = compl.product_id
                self.form['prod_id'] = compl.prod_id
            except sqlalchemy.orm.exc.NoResultFound:
                sys.exc_clear()
                self.errots.append(u"Запись не найдена.")
        return


    def E_data(self):
        dbconn = self.dbconn
        compls = dbconn.query(Compl, Product.name).filter(Compl.prod_id == self.form['prod_id']).filter(Product.product_id == Compl.product_id)
        data = E.data(prod_id=str(self.form['prod_id']))
        data_tag = data.xpath('//data')[0]
        for (compl, name) in compls:
            data_tag.append(E.compl(art=name, compl_id=str(compl.compl_id), product_id=str(compl.prod_id)))
        return data

class export(template_base):
    cls__kwds = set([ 'product' ])
    cls__title = u"Экспорт товара"
    cls__xsllist = [
        ('', '__root__.xsl'),
        ('form', '__simpleedit__.xsl'),
    ]
    class callback_form(form_base):
        fields = [
            field('distrib_id', 0, int, ValueError),
            field('charset','koi8-r'),
            field('dialect', 'excel'),
            field('action',''),
            ]
        labels = {
                'distrib_id':u'Выберите дистрибьюцию',
                'charset':u'Кодировка',
                'dialect':u'Разделитель',
                  }
        ftypes = {'distrib_id': 'select',
                    'dialect': 'select',
                    'charset': 'select',
                }
        
        def select_distrib_id(self, field):
            options = []
            distrib_id =  self.template_ref().distrib_id
            if distrib_id:
                try:
                    distrib_name =  self.template_ref().dbconn.query(Category.name).filter(sqlalchemy.and_(Distributor.distrib_id == distrib_id, Category.category_id == Distributor.category_id)).one()
                except sqlalchemy.orm.exc.NoResultFound:
                    sys.exc_clear()
                    return E.options()
                return  E.options(E.option(E.value(str(distrib_id)), distrib_name[0]))
            else:
                for r in self.template_ref().dbconn.query(Distributor.distrib_id, Category.name).filter(Distributor.category_id == Category.category_id):
                    options.append(E.option(E.value(str(r.distrib_id)), r.name))
                return E.options(*options)
        def select_dialect(self, field):
            return E.options(E.option(E.value('excel'), u';'),
                            E.option(E.value('excel_semicolon'), u','), 
                            E.option(E.value('excel-tab'), u'табуляция'), 
                            )
        def select_charset(self, field):
            return E.options(E.option(E.value('cp1251'), u'cp1251'),
                            E.option(E.value('utf8'), u'utf8'), 
                            E.option(E.value('koi8-r'), u'koi8-r'),
                            E.option(E.value('ibm866'), u'ibm866'), 
                            )
    def logic(self):
        sess = self.req.environ['rrduet.sess']
        self.distrib_id = sess['distrib_id']
        action = self.form['action']
        distrib_id = self.form['distrib_id']
        if self.distrib_id:
            distrib_id = self.distrib_id
        charset = self.form['charset']
        dialect = self.form['dialect']
        self.form['action'] = 'check'
        dbconn = self.dbconn
        if action == 'check':
            if  distrib_id:
                rows = []
                for r in list(dbconn.query(Product).filter(Product.distrib_id == distrib_id)):
                    product_id = r.product_id
                    lst = []
                    for at in atlist:
                        if at == 'delivery':
                            val = r.price_delivery_id
                        elif at == 'params':
                            val = u'| '.join(( (u"%s: %s" % (r.name, r.value)) for r in dbconn.query(Tehnical).filter(Tehnical.product_id == product_id) ))
                        elif at == 'category':
                            val = u','.join(( unicode(r.category_id) for r in dbconn.query(Prod_more_category).filter(Prod_more_category.product_id == product_id) ))
                            if val == '':
                                val = r.distrib_id
                        elif at == 'price_old':
                            val = str(r.old_price).replace('.00', '')
                        elif at == 'price':
                            val = str(r.price).replace('.00', '')
                        elif at == 'sale':
                            val = r.sale_on
                        elif at == 'week':
                            val = r.prod_week
                        elif at == 'overview':
                            val = val.replace("\n", " ")
                        elif at == 'description':
                            val = val.replace("\n", " ")
                        elif at == 'kw':
                            val = u' '.join(( r.kw for r in dbconn.query(Prod_kw).filter(Prod_kw.product_id == product_id) ))
                        elif at == 'complements':
                            val = u','.join(( unicode(r.product_id) for r in dbconn.query(Compl).filter(Compl.prod_id == product_id) ))
                        else:
                            val = getattr(r, at)
                        lst.append(unicode(val).encode(charset, 'ignore'))
                    rows.append(lst)
                s = cStringIO.StringIO()
                w = csv.writer(s, dialect)
                w.writerow(atlist)
                for p in rows:
                    w.writerow(p)
                self.resp.content_type = 'text/x-csv'
                self.resp.body = s.getvalue()
                self.resp.headers['Content-Disposition'] = 'attachment; filename="export_distrib%s.csv"'% str(distrib_id)
                return True
            else:
                self.errors.append(u'Укажите дистрибьюцию')
        return None 
class export_photo(template_base):
    cls__kwds = set([ 'product' ])
    cls__title = u"Экспорт фото товара"
    cls__xsllist = [
        ('', '__root__.xsl'),
        ('form', '__simpleedit__.xsl'),
    ]
    class callback_form(form_base):
        fields = [
            field('distrib_id', 0, int, ValueError),
            field('charset','koi8-r'),
            field('dialect', 'excel'),
            field('action',''),
            ]
        labels = {
                'distrib_id':u'Выберите дистрибьюцию',
                'charset':u'Кодировка',
                'dialect':u'Разделитель',
                  }
        ftypes = {'distrib_id': 'select',
                    'dialect': 'select',
                    'charset': 'select',
                }
        
        def select_distrib_id(self, field):
            options = []
            distrib_id =  self.template_ref().distrib_id
            if distrib_id:
                try:
                    distrib_name =  self.template_ref().dbconn.query(Category.name).filter(sqlalchemy.and_(Distributor.distrib_id == distrib_id, Category.category_id == Distributor.category_id)).one()
                except sqlalchemy.orm.exc.NoResultFound:
                    sys.exc_clear()
                    return E.options()
                return  E.options(E.option(E.value(str(distrib_id)), distrib_name[0]))
            else:
                for r in self.template_ref().dbconn.query(Distributor.distrib_id, Category.name).filter(Distributor.category_id == Category.category_id):
                    options.append(E.option(E.value(str(r.distrib_id)), r.name))
                return E.options(*options)
        def select_dialect(self, field):
            return E.options(E.option(E.value('excel'), u';'),
                            E.option(E.value('excel_semicolon'), u','), 
                            E.option(E.value('excel-tab'), u'табуляция'), 
                            )
        def select_charset(self, field):
            return E.options(E.option(E.value('cp1251'), u'cp1251'),
                            E.option(E.value('utf8'), u'utf8'), 
                            E.option(E.value('koi8-r'), u'koi8-r'),
                            E.option(E.value('ibm866'), u'ibm866'), 
                            )
    def logic(self):
        sess = self.req.environ['rrduet.sess']
        self.distrib_id = sess['distrib_id']
        action = self.form['action']
        distrib_id = self.form['distrib_id']
        if self.distrib_id:
            distrib_id = self.distrib_id
        charset = self.form['charset']
        dialect = self.form['dialect']
        self.form['action'] = 'check'
        dbconn = self.dbconn
        if action == 'check':
            if  distrib_id:
                rows = []
                for art, ph_name in list(dbconn.query(Product.articul, Photo.photo_name).filter(Product.distrib_id == distrib_id).filter(Product.product_id == Photo.product_id)):
                    rows.append([unicode(str(art)).encode(charset, 'ignore'), unicode(ph_name).encode(charset, 'ignore')])
                s = cStringIO.StringIO()
                w = csv.writer(s, dialect)
                w.writerow(['articul', 'name'])
                for p in rows:
                    w.writerow(p)
                self.resp.content_type = 'text/x-csv'
                self.resp.body = s.getvalue()
                self.resp.headers['Content-Disposition'] = 'attachment; filename="export_distrib%s.csv"'% str(distrib_id)
                return True
            else:
                self.errors.append(u'Укажите дистрибьюцию')
        return None 

class export_pricelist(template_base):
    cls__kwds = set([ 'product' ])
    cls__title = u"Прайслист"
    cls__xsllist = [
        ('', '__root__.xsl'),
        ('form', '__simpleedit__.xsl'),
    ]
    class callback_form(form_base):
        fields = [
            field('distrib_id', 0, int, ValueError),
            field('charset','koi8-r'),
            field('dialect', 'excel'),
            field('action',''),
            ]
        labels = {
                'distrib_id':u'Раздел',
                'charset':u'Кодировка',
                'dialect':u'Разделитель',
                  }
        ftypes = {'distrib_id': 'select',
                    'dialect': 'select',
                    'charset': 'select',
                }
        
        def select_distrib_id(self, field):
            options = []
            distrib_id =  self.template_ref().distrib_id
            #options.append(E.option(E.value(u'0'), u'все разделы'))
            if distrib_id:
                try:
                    distrib_name =  self.template_ref().dbconn.query(Category.name).filter(sqlalchemy.and_(Distributor.distrib_id == distrib_id, Category.category_id == Distributor.category_id)).one()
                except sqlalchemy.orm.exc.NoResultFound:
                    sys.exc_clear()
                    return E.options()
                return  E.options(E.option(E.value(str(distrib_id)), distrib_name[0]))
            else:
                for r in self.template_ref().dbconn.query(Distributor.distrib_id, Category.name).filter(Distributor.category_id == Category.category_id):
                    options.append(E.option(E.value(str(r.distrib_id)), r.name))
                return E.options(*options)
        def select_dialect(self, field):
            return E.options(E.option(E.value('excel'), u';'),
                            E.option(E.value('excel_semicolon'), u','), 
                            E.option(E.value('excel-tab'), u'табуляция'), 
                            )
        def select_charset(self, field):
            return E.options(E.option(E.value('cp1251'), u'cp1251'),
                            E.option(E.value('utf8'), u'utf8'), 
                            E.option(E.value('koi8-r'), u'koi8-r'),
                            E.option(E.value('ibm866'), u'ibm866'), 
                            )
    def logic(self):
        sess = self.req.environ['rrduet.sess']
        self.distrib_id = sess['distrib_id']
        action = self.form['action']
        distrib_id = self.form['distrib_id']
        if self.distrib_id:
            distrib_id = self.distrib_id
        charset = self.form['charset']
        dialect = self.form['dialect']
        self.form['action'] = 'check'
        dbconn = self.dbconn
        if action == 'check':
            products = dbconn.query(Product, Category.name)
            if  distrib_id:
                products = products.filter(Product.distrib_id == distrib_id)
            products = products.filter(Distributor.distrib_id == Product.distrib_id).filter(Category.category_id == Distributor.category_id)
            rows = [[u"Артикул".encode(charset, 'ignore'), u"Название".encode(charset, 'ignore'), u"Цена".encode(charset, 'ignore') ]]
            distr_id = 0 
            for r in products:
                if distr_id != r[0].distrib_id:
                    distr_id = r[0].distrib_id
                    rows.append([unicode(r[1]).encode(charset, 'ignore')])
                articul = unicode(r[0].articul).encode(charset, 'ignore')
                name = unicode(r[0].name).encode(charset, 'ignore')
                price = unicode(str(r[0].price)).encode(charset, 'ignore')
                rows.append([articul, name, price])
                s = cStringIO.StringIO()
                w = csv.writer(s, dialect)
            for p in rows:
                w.writerow(p)
            self.resp.content_type = 'text/x-csv'
            self.resp.body = s.getvalue()
            self.resp.headers['Content-Disposition'] = 'attachment; filename="export_pricelist%s.csv"'% str(distrib_id)
            return True
        else:
            self.errors.append(u'Укажите раздел')
        return None 



