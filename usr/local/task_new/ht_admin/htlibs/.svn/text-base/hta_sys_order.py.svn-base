#
# -*- coding: utf-8 -*-

import sys
import re
import sqlalchemy
import sqlalchemy.orm
from sqlalchemy import func
from sqlalchemy import desc
from rrduet.rr_template import field, E
import datetime

import hta_config
from hta_base import check_action,form_order
from hta_page import form_base, template_base, menu_base
from fullshopapi import Category
from fullshopapi import Delivery
from fullshopapi import Product
from fullshopapi import Payment
from fullshopapi import Distributor
from fullshopapi import Price_delivery
from fullshopapi import Order 
from fullshopapi import Prod_order 
from fullshopapi import History 
from fullshopapi import Status_order 
from fullshopapi import Comment 
from fullshopapi import Distrib_oper 

class order_old(template_base):
    cls__title = u"Заказы"
    cls__kwds = set([ 'order' ])
    cls__xsllist = [
        ('', '__root__.xsl'),
    ]
    cls__externals = [
        '/css/main.css',
        '/extjs/resources/css/ext-all.css',
        '/extjs/resources/css/dd.css',
        '/extjs/adapter/ext/ext-base.js',
        '/extjs/ext-all-debug.js',
        #'/extjs/ext-all.js',
        '/js/private/order.js',
    ]
    class callback_form(form_base):
        fields = [
            field('order_id', 0, int, ValueError),
            field('action',''),
            ]
    def logic(self):
        action = self.form['action']
        order_id = self.form['order_id']
        dbconn = self.dbconn
        if action == 'delete':
            try:
                order = dbconn.query(Order).filter(Order.order_id == order_id).one()
            except sqlalchemy.orm.exc.NoResultFound:
                sys.exc_clear()
                return
            dbconn.delete(order)
            prod_orders = dbconn.query(Prod_order).filter(Prod_order.order_id == order_id).all()
            for k in prod_orders:
                dbconn.delete(k)
            dbconn.commit()
            return 
class page_order(template_base):
    cls__title = u"Заказы"
    cls__kwds = set([ 'order' ])
    cls__xsllist = [
        ('', '__root__.xsl'),
        ('form', '__simpleedit__.xsl'),
        ('body', 'order_new.xsl'),
    ]
    cls__externals = [
        '/css/main.css',
        '/js/jquery-1.2.6.js',
        '/js/private/order_new.js',
    ]
    class callback_form(form_base):
        
        fields = [
            field('date_b', ''),
            field('date_e', ''),
            field('date_distr', ''),
            field('order_id', 0, int, ValueError),
            field('status', 0, int, ValueError),
            field('limit', 20, int, ValueError),
            field('offset', 0,  int, ValueError),
            ]
        labels = {
                'order_id':u'Номер заказа',
                'status':u'Выберите статус заказа',
                'date_b':u'Выберите начало периода',
                'date_e':u'Выберите конец периода',
                'date_distr':u'Выберите дату доставки',
                
                }
        ftypes = {'status':'select', 'date_b':'date', 'date_e':'date', 'date_distr':'date'}
        def select_status(self, field):
            options = [E.option(E.value('0'), '----------')]
            for r in self.template_ref().dbconn.query(Status_order).all():
                options.append(E.option(E.value(str(r.status_order_id)), r.name))
            return E.options(*options)
    def orders(self):
        import cStringIO
        from lxml import etree
        self.form['order_id'] = 0
        f = open('/usr/local/fshop/ht_admin/templates/order_new.xsl')
        _spec = f.read()
        f.close()
        xslt = cStringIO.StringIO(_spec)
        parser = etree.parse(xslt)
        result = etree.XSLT(parser)
        return result(E.R(self.E_data()))

    def E_data(self):
        form = self.form
        limit=form['limit']
        offset=form['offset']
        date_b = form['date_b']
        date_e = form['date_e']
        date_distr = form['date_distr']
        sess = self.req.environ['rrduet.sess']
        oper_id = sess['oper_id']
#        if date_distr == '' and oper_id==1:
#            date_distr = datetime.datetime.now().strftime('%Y-%m-%d')
        date_now = datetime.datetime.now().strftime('%Y-%m-%d')
        status = form['status']
        order_id = form['order_id']
        where = []
        if date_b !='':
            where.append('porder.datetime>="%s"' % date_b)
        if date_e != '':
            where.append('porder.datetime<="%s"' % date_e)
        if date_distr != '':
            where.append('porder.datetime_distr>="%s 0:0:0" and porder.datetime_distr<="%s 23:59:59"' % (date_distr, date_distr))
        if order_id:
            where = ['porder.order_id=%s' % order_id]
        if where:
            where_clause = 'where '+' and '.join(where)
        if where:
            where_clause = 'where '+' and '.join(where)
        else:
            where_clause = ''
        if status:
            st_where = 'where st_id=%s' % (status,)
        else:
            st_where = ''
        dbconn = self.dbconn
        t = """
            select sql_calc_found_rows * from( select  * from (
                select porder.order_id as ord_id,
                    status_order.name as status,
                    status_order.status_order_id as st_id,
                    porder.datetime as dt,
                    datetime_distr, 
                    concat(username, ' ', sername, ' ', patronymic) as fio,
                    email,
                    address,
                    phones,
                    amount,
                    porder.note,
                    payment.name as pmt,
                    delivery.name as delivery,
                    porder.sale as sale
                from porder join history_prod using(order_id) join status_order using(status_order_id) join delivery using(delivery_id) join payment on payment.payment_id=porder.payment_id
                %s
                order by porder.order_id, history_prod.datetime desc)
            as k  group by ord_id order by ord_id desc) as p %s limit %s offset %s; 
        """ % (where_clause, st_where, limit, offset,)
        order_status = dbconn.execute(t)
        count = list(dbconn.execute("select found_rows()"))[0][0]
        next = prev = ''
        if count>offset+limit:
            next = str(offset+limit) 
        if offset > 0:
            prev = str(offset-limit)
        orders= []
        for ord_id , sts, st_id, dt, dt_distr, fio, email, address, phones, amount, note, pmt, delivery, sale in order_status: 
            prods = dbconn.query(Prod_order).filter(Prod_order.order_id==ord_id)
            sale_str = u"нет"
            for pr in prods:
                if pr.sale:
                    sale_str = u"есть"
            css = 'green'
            if date_now == dt_distr.strftime('%Y-%m-%d'):
                css = 'red'
            orders.append(E.order(
                E.ord_id(str(ord_id)),
                E.status(sts),
                E.stid(str(st_id)),
                E.dt(dt.strftime('%Y-%m-%d')),
                E.dt_distr(dt_distr.strftime('%Y-%m-%d %H:%M'), css=css),
                E.fio(fio),
                E.email(email),
                E.address(address),
                E.phones(phones),
                E.amount('%10.2f' % (amount*(1-sale/100))),
                E.note(note),
                E.pmt(pmt),
                E.delivery(delivery),
                E.sale(sale_str),
                E.prods(*(E.prod(name=p.product_name, count=str(p.count), amount=str(p.amount), close=p.close) for p in prods)),
                #dbconn.query(Prod_order).filter(Prod_order.order_id==ord_id))),
                E.comments(*(E.comment(c.comment, name=d.firstname) for c,d in dbconn.query(Comment, Distrib_oper).filter(Comment.order_id==ord_id).filter(Comment.oper_id==Distrib_oper.oper_id).order_by(Comment.comment_order_id))),
                E.history(*(E.st(dt=h.datetime.strftime('%Y-%m-%d %H:%M:%S'), name=s.name, oper=op.firstname) for h,s, op in dbconn.query(History, Status_order, Distrib_oper).filter(
                    History.order_id==ord_id).filter(Status_order.status_order_id==History.status_order_id).filter(Distrib_oper.oper_id==History.oper_id).order_by(desc(History.datetime)) )),
            ))
        return E.data(*orders, offset=str(offset), next=next, prev=prev,date_b=date_b, date_e=str(date_e), status=str(status)) 
class page_order_print(template_base):
    cls__title = u"Заказы"
    cls__kwds = set([ 'order' ])
    cls__xsllist = [
        ('', 'order_new_print.xsl'),
    ]
    cls__externals = [
        '/css/main.css',
    ]
    class callback_form(form_base):
        
        fields = [
            field('order_id', 0, int, ValueError),
            ]
    def orders(self):
        import cStringIO
        from lxml import etree
        self.form['order_id'] = 0
        f = open('/usr/local/fshop/ht_admin/templates/order_new.xsl')
        _spec = f.read()
        f.close()
        xslt = cStringIO.StringIO(_spec)
        parser = etree.parse(xslt)
        result = etree.XSLT(parser)
        return result(E.R(self.E_data()))

    def E_data(self):
        form = self.form
        order_id = form['order_id']
        where = []
        if order_id:
            where = 'porder.order_id=%s' % order_id
        if where:
            where_clause = 'where '+where
        dbconn = self.dbconn
        t = """
            select sql_calc_found_rows * from( select  * from (
                select porder.order_id as ord_id,
                    status_order.name as status,
                    status_order.status_order_id as st_id,
                    porder.datetime as dt,
                    datetime_distr, 
                    concat(username, ' ', sername, ' ', patronymic) as fio,
                    email,
                    address,
                    phones,
                    amount,
                    porder.note,
                    payment.name as pmt,
                    delivery.name as delivery,
                    porder.sale as sale
                from porder join history_prod using(order_id) join status_order using(status_order_id) join delivery using(delivery_id) join payment on payment.payment_id=porder.payment_id
                %s
                order by porder.order_id, history_prod.datetime desc)
            as k  group by ord_id order by ord_id desc) as p; 
        """ % (where_clause,)
        order_status = dbconn.execute(t)
        orders = []
        for ord_id , sts, st_id, dt, dt_distr, fio, email, address, phones, amount, note, pmt, delivery, sale in order_status: 
            prods = dbconn.query(Prod_order).filter(Prod_order.order_id==ord_id)
            sale_str = u"нет"
            for pr in prods:
                if pr.sale:
                    sale_str = u"есть"
            css = 'green'
            orders.append(E.order(
                E.ord_id(str(ord_id)),
                E.status(sts),
                E.stid(str(st_id)),
                E.dt(dt.strftime('%Y-%m-%d')),
                E.dt_distr(dt_distr.strftime('%Y-%m-%d %H:%M'), css=css),
                E.fio(fio),
                E.email(email),
                E.address(address),
                E.phones(phones),
                E.amount('%10.2f' % (amount*(1-sale/100))),
                E.note(note),
                E.pmt(pmt),
                E.delivery(delivery),
                E.sale(sale_str),
                E.prods(*(E.prod(name=p.product_name, count=str(p.count), amount=str(p.amount), close=p.close) for p in prods)),
                #dbconn.query(Prod_order).filter(Prod_order.order_id==ord_id))),
                E.comments(*(E.comment(c.comment, name=d.firstname) for c,d in dbconn.query(Comment, Distrib_oper).filter(Comment.order_id==ord_id).filter(Comment.oper_id==Distrib_oper.oper_id).order_by(Comment.comment_order_id))),
                E.history(*(E.st(dt=h.datetime.strftime('%Y-%m-%d %H:%M:%S'), name=s.name, oper=op.firstname) for h,s, op in dbconn.query(History, Status_order, Distrib_oper).filter(
                    History.order_id==ord_id).filter(Status_order.status_order_id==History.status_order_id).filter(Distrib_oper.oper_id==History.oper_id).order_by(desc(History.datetime)) )),
            ))
        return E.data(*orders) 
class order_new(page_order):
    cls__externals = [
        '/css/main.css',
        '/js/jquery-1.2.6.js',
        '/js/private/order_new2.js',
    ]

class order_sale(page_order):
    cls__kwds = set([ 'order' ])
    cls__application = 'ajax'
    class callback_form(form_order):
        fields = [
            field('sale',''),
        ]
    def ajax(self):
        self.resp.content_type = 'text/html'
        form = self.form
        order_id = form['order_id']
        form['sale'] = 0
        sale = float(form['sale'])
        dbconn = self.dbconn
        self.xmlroot = self.orders()
        try:
            order = dbconn.query(Order).filter(Order.order_id==order_id).one()
        except sqlalchemy.orm.exc.NoResultFound:
            sys.exc_clear()
            return self.xmlroot
        order.sale=sale
        try:
            dbconn.commit()
        except:
            return self.xmlroot
        self.xmlroot = self.orders()
        return self.xmlroot

class order_date_distr(page_order):
    cls__kwds = set([ 'order' ])
    cls__application = 'ajax'
    class callback_form(form_order):
        fields = [
            field('date_distr_new',''),
            ]
    def ajax(self):
        self.resp.content_type = 'text/html'
        form = self.form
        order_id = form['order_id']
        date_distr = form['date_distr_new']
        dbconn = self.dbconn
        self.xmlroot = self.orders()
        sess = self.req.environ['rrduet.sess']
        oper_id = sess['oper_id']
        try:
            order = dbconn.query(Order).filter(Order.order_id==order_id).one()
            old = order.datetime_distr.strftime('%Y-%m:%d %H:%M:%S')
        except sqlalchemy.orm.exc.NoResultFound:
            sys.exc_clear()
            return self.xmlroot
        order.datetime_distr=date_distr
        try:
            comment = u"смена даты доставки с %s на %s" % (old, date_distr)
            comment = Comment(order_id, oper_id, comment)
            dbconn.add(comment)
            dbconn.commit()
        except:
            dbconn.rollback()
            sys.exc_clear()
        self.xmlroot = self.orders()
        return self.xmlroot



class order_ajax(template_base):
    cls__kwds = set([ 'order' ])
    cls__application = 'ajax'
    class callback_form(form_base):
        fields = [
            field('order_id', 0,int, ValueError),
            field('username',''),
            field('sername',''),
            field('patronymic', ''),
            field('email',''),
            field('address',''),
            field('phones',''),
            field('sale_type',''),
            field('note',''),
            field('delivery_id',''),
            field('payment_id', ''),
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
        orders = dbconn.execute('select * from (select porder.order_id,porder.username, porder.sername, porder.patronymic, porder.email, porder.address, porder.phones, porder.sale_type, porder.note, porder.delivery_id, porder.payment_id, porder.amount, history_prod.datetime, status_order.name as name, status_order.status_order_id  from porder  join history_prod using (order_id) join status_order using (status_order_id) order by status_order.name desc, order_id) as t group by name, datetime;')
        delivery = dbconn.query(Delivery).all()
        payment = dbconn.query(Payment).all()
        ajax = []
        for d in delivery:
            ajax.append(E.delivery(
                delivery_id = str(d.delivery_id),
                name = d.name,
                    ))
        for p in payment:
            ajax.append(E.payment(
                payment_id = str(p.payment_id),
                name = p.name,
                    ))
        for r in orders:
            ajax.append(E.order(
                order_id = str(r[0]),
                name = r[1],
                sename = r[2],
                patronymic = r[3],
                email = r[4],
                address = r[5],
                phones = r[6],
                sale_type = str(r[7]),
                note = r[8],
                delivery_id = str(r[9]),
                payment_id = str(r[10]),
                amount = str(r[11]),
                date = r[12].strftime('%Y-%m-%d'),
                status = r[13]
                ))
        return E.ajax(*ajax)


    def config(self, dbconn):
        form = self.form
        action = form['action']
        order_id = form['order_id']
        name = form['username']
        sename = form['sername']
        patronymic = form['patronymic']
        email = form['email']
        address = form['address']
        phones = form['phones']
        sale_type = form['sale_type']
        note = form['note']
        delivery_id = form['delivery_id']
        payment_id = form['payment_id']
        amount = form['amount']
        order_id = order_id
        if order_id == 0:
            order = Order('', '','', '','','','all','', 0,0, 0)
            dbconn.add(order)
            dbconn.commit()
            form['order_id'] = order.order_id
            form.store_to_orm(order)
            try:
                dbconn.commit()
                history = History(order.order_id, datetime.datetime.now(), '1')
                dbconn.add(history)
                dbconn.commit()
            except:
                dbconn.delete(order)
                dbconn.commit()
        else:
            try:
                order = dbconn.query(Order).filter(Order.order_id == order_id).one()
            except sqlalchemy.orm.exc.NoResultFound:
                sys.exc_clear()
                return
            form.store_to_orm(order)
            dbconn.commit()
            try:
                dbconn.commit()
            except:
                dbconn.delete(order)
                dbconn.commit()
        orders = dbconn.query(Order, History.datetime).filter(sqlalchemy.and_(History.order_id == Order.order_id, History.status_order_id == 1)).all()
        delivery = dbconn.query(Delivery).all()
        payment = dbconn.query(Payment).all()
        ajax = []
        for d in delivery:
            ajax.append(E.delivery(
                delivery_id = str(d.delivery_id),
                name = d.name,
                    ))
        for p in payment:
            ajax.append(E.payment(
                payment_id = str(p.payment_id),
                name = p.name,
                    ))
        for r in orders:
            ajax.append(E.order(
                order_id = str(r[0].order_id),
                name = r[0].username,
                sename = r[0].sername,
                patronymic = r[0].patronymic,
                email = r[0].email,
                address = r[0].address,
                phones = r[0].phones,
                sale_type = str(r[0].sale_type),
                note = r[0].note,
                delivery_id = str(r[0].delivery_id),
                payment_id = str(r[0].payment_id),
                amount = str(r[0].amount),
                date = r[1].strftime('%Y-%m-%d')
                ))
        return E.ajax(*ajax)

class order_detail(template_base):
    cls__kwds = set([ 'order' ])
    cls__title = u"Информация о заказе"
    cls__xsllist = [
        ('', '__root__.xsl'),
        ('body', 'order_detail.xsl'),
    ]
    cls__externals = [
        '/css/main.css',
        '/extjs/resources/css/ext-all.css',
        '/extjs/resources/css/dd.css',
        '/extjs/adapter/ext/ext-base.js',
        '/extjs/ext-all-debug.js',
        #'/extjs/ext-all.js',
        '/js/private/order_detail.js',
    ]
    class callback_form(form_base):
        fields = [
            field('order_id', 0, int, ValueError),
            field('prod_order_id', 0, int, ValueError),
            field('action',''),
            ]
    def logic(self):
        action = self.form['action']
        order_id = self.form['order_id']
        prod_order_id = self.form['prod_order_id']
        self.form['action'] = ''
        self.form['prod_order_id'] = 0
#        self.title = 'Заказ № %s' % order_id
        dbconn = self.dbconn
        if action == 'delete':
            try:
                order = dbconn.query(Prod_order).filter(Prod_order.prod_order_id == prod_order_id).one()
            except sqlalchemy.orm.exc.NoResultFound:
                sys.exc_clear()
                return
            order.close="yes"
            dbconn.commit()
            amount = dbconn.query(func.sum(Prod_order.amount*Prod_order.count-Prod_order.sale)).filter(Prod_order.order_id == order_id).filter(Prod_order.close=="no")[0][0]
            profit = dbconn.query(func.sum(Prod_order.amount*Prod_order.procent*Prod_order.count/100+Prod_order.profit*Prod_order.count-Prod_order.sale)).filter(Prod_order.order_id == order_id).filter(Prod_order.close=="no")[0][0]
            try:
                order = dbconn.query(Order).filter(Order.order_id == order_id).one()
            except sqlalchemy.orm.exc.NoResultFound:
                sys.exc_clear()
                return
            order.amount = amount
            order.profit = profit
            dbconn.commit()
            return
        elif action == 'add':
            try:
                order = dbconn.query(Prod_order).filter(Prod_order.prod_order_id == prod_order_id).one()
            except sqlalchemy.orm.exc.NoResultFound:
                sys.exc_clear()
                return
            order.close="no"
            dbconn.commit()
            amount = dbconn.query(func.sum(Prod_order.amount*Prod_order.count-Prod_order.sale)).filter(Prod_order.order_id == order_id).filter(Prod_order.close=="no")[0][0]
            profit = dbconn.query(func.sum(Prod_order.amount*Prod_order.procent*Prod_order.count/100+Prod_order.profit*Prod_order.count-Prod_order.sale)).filter(Prod_order.order_id == order_id).filter(Prod_order.close=="no")[0][0]
            try:
                order = dbconn.query(Order).filter(Order.order_id == order_id).one()
            except sqlalchemy.orm.exc.NoResultFound:
                sys.exc_clear()
                return
            order.amount = amount
            order.profit = profit
            dbconn.commit()
            return
    def E_data(self):
        return E.data(order_id=str(self.form['order_id']))

class order_detail_ajax(template_base):
    cls__kwds = set([ 'order' ])
    cls__application = 'ajax'
    class callback_form(form_base):
        fields = [
            field('prod_order_id', 0,int, ValueError),
            field('order_id', 0,int, ValueError),
            field('product_id', 0,int, ValueError),
            field('count', 0),
            field('bonus', 0),
            field('sale', 0),
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
        order_id = form['order_id']
        orders = dbconn.query(Prod_order).filter(Prod_order.order_id == order_id).all()
        products = dbconn.execute('select p.product_id, p.name, c.name from product as p join distributor as d using (distrib_id) join category as c using (category_id)')
        ajax = []
        for p in products:
            ajax.append(E.product(
                product_id = str(p[0]),
                name = p[1]+' '+p[2],
                    ))
        for r in orders:
            ajax.append(E.order(
                prod_order_id = str(r.prod_order_id),
                order_id = str(r.order_id),
                product_id = str(r.product_id),
                product_name = r.product_name,
                count = str(r.count),
                amount = str(r.amount),
                bonus = str(r.bonus),
                close=r.close,
                sale=str(r.sale),
                ))
        return E.ajax(*ajax)


    def config(self, dbconn):
        form = self.form
        action = form['action']
        order_id = form['order_id']
        prod_order_id = form['prod_order_id']
        product_id = form['product_id']
        count = form['count']
        sale = form['sale']
        bonus = 0
        if prod_order_id == 0:
            try:
                prod = dbconn.query(Product).filter(Product.product_id == product_id).one()
                amount = prod.price
                distr = prod.distrib_id
                product_name = prod.name+' (art. '+prod.articul+')'
            except sqlalchemy.orm.exc.NoResultFound:
                sys.exc_clear()
                return
            prod_order = Prod_order(order_id, product_id, amount, count, product_name, bonus,"no", distr, sale)
            dbconn.add(prod_order)
            try:
                dbconn.commit()
            except:
                dbconn.delete(prod_order)
                dbconn.commit()
            amount = dbconn.query(func.sum(Prod_order.amount*Prod_order.count-Prod_order.sale)).filter(Prod_order.order_id == order_id).filter(Prod_order.close=="no")[0][0]
            try:
                order = dbconn.query(Order).filter(Order.order_id == order_id).one()
            except sqlalchemy.orm.exc.NoResultFound:
                sys.exc_clear()
                return
            order.amount = amount
            dbconn.commit()
        else:
            try:
                prod_order = dbconn.query(Prod_order).filter(Prod_order.prod_order_id == prod_order_id).one()
            except sqlalchemy.orm.exc.NoResultFound:
                sys.exc_clear()
                return
            try:
                prod = dbconn.query(Product).filter(Product.product_id == product_id).one()
                product_name = prod.name
            except sqlalchemy.orm.exc.NoResultFound:
                sys.exc_clear()
                return
            prod_order.count = count
            prod_order.bonus = bonus
            prod_order.order_id = order_id
            prod_order.prod_order_id = prod_order_id
            prod_order.product_name = product_name
            prod_order.sale = sale
            try:
                dbconn.commit()
                amount = dbconn.query(func.sum(Prod_order.amount*Prod_order.count-Prod_order.sale)).filter(Prod_order.order_id == order_id).filter(Prod_order.close=="no")[0][0]
                profit = dbconn.query(func.sum(Prod_order.amount*Prod_order.procent*Prod_order.count/100+Prod_order.profit*Prod_order.count-Prod_order.sale)).filter(Prod_order.order_id == order_id).filter(Prod_order.close=="no")[0][0]
                try:
                    order = dbconn.query(Order).filter(Order.order_id == order_id).one()
                except sqlalchemy.orm.exc.NoResultFound:
                    sys.exc_clear()
                    return
                order.amount = amount
                order.profit = profit
                dbconn.commit()
            except:
                pass
        orders = dbconn.query(Prod_order).filter(Prod_order.order_id == order_id).all()
        products = dbconn.execute('select p.product_id, p.name, c.name from product as p join distributor as d using (distrib_id) join category as c using (category_id)')
        ajax = []
        for p in products:
            ajax.append(E.product(
                product_id = str(p[0]),
                name = p[1]+' '+p[2],
                    ))
        for r in orders:
            ajax.append(E.order(
                prod_order_id = str(r.prod_order_id),
                order_id = str(r.order_id),
                product_id = str(r.product_id),
                product_name = r.product_name,
                count = str(r.count),
                amount = str(r.amount),
                bonus = str(r.bonus),
                close=r.close,
                sale=str(r.sale),
                ))
        return E.ajax(*ajax)

class order_status_old(template_base):
    cls__kwds = set([ 'order' ])
    cls__title = u"Статус заказа"
    cls__xsllist = [
        ('', '__root__.xsl'),
        ('body', 'order_status.xsl'),
        ('form', '__simpleedit__.xsl'),
    ]
    class callback_form(form_base):
        fields = [
            field('order_id', 0, int, ValueError),
            field('status',''),
            field('action',''),
            ]
        labels = {'status':u'Выберите статус заказа'}
        ftypes = {'status':'select'}
        def select_status(self, field):
            options = []
            for r in self.template_ref().dbconn.query(Status_order).all():
                options.append(E.option(E.value(str(r.status_order_id)), r.name))
            return E.options(*options)

    def logic(self):
        action = self.form['action']
        order_id = self.form['order_id']
        status = self.form['status']
        self.form['action'] = 'check'
        dbconn = self.dbconn
        sess = self.req.environ['rrduet.sess']
        oper_id = sess['oper_id']
        if action == 'check':
            if order_id and status:
                history = History(order_id, datetime.datetime.now(), status, oper_id)
                dbconn.add(history)
                dbconn.commit()
            else:
                self.errors.append(u'выберите статус заказа')


    def E_data(self):
        dbconn = self.dbconn
        history = dbconn.query(History.datetime, Status_order.name).filter(sqlalchemy.and_(History.order_id == self.form['order_id'], History.status_order_id == Status_order.status_order_id)).order_by(desc(History.datetime))
        data = E.data()
        data_tag = data.xpath('//data')[0]
        for date, status in history:
            data_tag.append(E.status(date=date.strftime('%Y-%m-%d %H:%M:%S'), status=status))
        return data

class order_status(page_order):
    cls__kwds = set([ 'order' ])
    cls__application = 'ajax'
    class callback_form(form_order):
        fields = [
            field('status_new',  0,int, ValueError),
            ]
    def ajax(self):
        self.resp.content_type = 'text/html'
        form = self.form
        order_id = form['order_id']
        status = form['status_new']
        dbconn = self.dbconn
        self.xmlroot = self.orders()
        sess = self.req.environ['rrduet.sess']
        oper_id = sess['oper_id']
        try:
            order = dbconn.query(Order).filter(Order.order_id==order_id).one()
            old = order.datetime_distr.strftime('%Y-%m:%d %H:%M:%S')
        except sqlalchemy.orm.exc.NoResultFound:
            sys.exc_clear()
            return self.xmlroot
        history = History(order_id, datetime.datetime.now(), status, oper_id)
        dbconn.add(history)
        try:
            dbconn.commit()
        except:
            sys.exc_clear()
            dbconn.rollback()
        self.xmlroot = self.orders()
        return self.xmlroot

class order_comment_old(template_base):
    cls__kwds = set([ 'order' ])
    cls__title = u"Комментарии к заказу"
    cls__xsllist = [
        ('', '__root__.xsl'),
        ('body', 'order_comment.xsl'),
        ('form', '__simpleedit__.xsl'),
    ]
    class callback_form(form_base):
        fields = [
            field('order_id', 0, int, ValueError),
            field('comment',''),
            field('action',''),
            ]
        labels = {'comment':u'Комментарий'}
        ftypes = {'comment': 'textarea'}
    def logic(self):
        action = self.form['action']
        order_id = self.form['order_id']
        comment = self.form['comment']
        self.form['action'] = 'check'
        dbconn = self.dbconn
        if action == 'check':
            if order_id and comment:
                sess = self.req.environ['rrduet.sess']
                oper_id = sess['oper_id']
                comment = Comment(order_id, oper_id, comment)
                dbconn.add(comment)
                dbconn.commit()
            else:
                self.errors.append(u'Добавьте комментарий')


    def E_data(self):
        dbconn = self.dbconn
        comment = dbconn.query(Comment.comment, Distrib_oper).filter(sqlalchemy.and_(Comment.order_id == self.form['order_id'], Comment.oper_id==Distrib_oper.oper_id))
        data = E.data()
        data_tag = data.xpath('//data')[0]
        for c, d in comment:
            data_tag.append(E.order(oper="%s %s" % (d.lastname, d.firstname), comment=c))
        return data
class order_comment(page_order):
    cls__kwds = set([ 'order' ])
    cls__application = 'ajax'
    class callback_form(form_order):
        fields = [
            field('comment',''),
        ]
    def ajax(self):
        self.resp.content_type = 'text/html'
        form = self.form
        order_id = form['order_id']
        comment = form['comment']
        dbconn = self.dbconn
        self.xmlroot = self.orders()
        sess = self.req.environ['rrduet.sess']
        oper_id = sess['oper_id']
        try:
            order = dbconn.query(Order).filter(Order.order_id==order_id).one()
        except sqlalchemy.orm.exc.NoResultFound:
            sys.exc_clear()
            return self.xmlroot
        comment = Comment(order_id, oper_id, comment)
        dbconn.add(comment)
        try:
            dbconn.commit()
        except:
            sys.exc_clear()
            dbconn.rollback()
        self.xmlroot = self.orders()
        return self.xmlroot
