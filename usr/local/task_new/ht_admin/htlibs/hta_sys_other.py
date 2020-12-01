#
# -*- coding: utf-8 -*-

import sys
import re
from rrduet.rr_template import field, E
import hta_config
from hta_base import check_action
from hta_page import form_base, template_base
from fullshopapi import Payment
from fullshopapi import Delivery
from fullshopapi import Price_delivery
from fullshopapi import Status_order
from fullshopapi import Banners
import sqlalchemy
import sqlalchemy.orm
import Image
from hta_config import htdocs_dir

class delivery_page(template_base):
    cls__kwds = set([ 'other' ])
    cls__title = u"Типы доставок"
    cls__xsllist = [
        ('', '__root__.xsl'),
        ('body', 'delivery.xsl'),
        ('form', '__simpleedit__.xsl'),
    ]
    class callback_form(form_base):
        fields = [
            field('delivery_id', 0, int, ValueError),
            field('payment_id', 0, int, ValueError),
            field('name',''),
            field('note',''),
            field('action',''),
            ]
        labels = {'payment_id':u'Оплата',
                'name':u'Имя',
                'note':u'Примечание',
                }
        ftypes = {'payment_id':'select'}
        def select_payment_id(self, field):
            options = []
            for r in self.template_ref().dbconn.query(Payment):
                options.append(E.option(E.value(str(r.payment_id)), r.name))
            return E.options(*options)

    def logic(self):
        action = self.form['action']
        payment_id = self.form['payment_id']
        delivery_id = self.form['delivery_id']
        name = self.form['name']
        note = self.form['note']
        self.form['action'] = 'check'
        dbconn = self.dbconn
        if action == 'check':
            if delivery_id == 0 and  note and name and payment_id:
                delivery = Delivery(payment_id, name, note)
                dbconn.add(delivery)
                try:
                    dbconn.commit()
                except:
                    self.errors.append(u'Конфликт имен')
            elif delivery_id and  note and name and payment_id:
                try:
                    delivery = dbconn.query(Delivery).filter(Delivery.delivery_id == delivery_id).one()
                except sqlalchemy.orm.exc.NoResultFound:
                    sys.exc_clear()
                    return
                try:
                    delivery.name = name
                    delivery.payment_id = payment_id
                    delivery.note = note
                    dbconn.commit()
                except:
                    self.errors.append(u'Изменения не были сохранены')
        elif action == 'delete':
            try:
                delivery = dbconn.query(Delivery).filter(Delivery.delivery_id == delivery_id).one()
            except sqlalchemy.orm.exc.NoResultFound:
                self.form['delivery_id'] = 0
                self.form['action'] = 'check'
                sys.exc_clear()
                return
            try:
                dbconn.delete(delivery)
                dbconn.commit()
            except:
                self.errors.append(u'Изменения не были сохранены')
            self.form['delivery_id'] = 0
            self.form['action'] = 'check'
        if self.results:
            self.form['delivery_id'] = 0
            self.form['note'] = ''
            self.form['payment_id'] = 0
            self.form['name'] = ''


    def E_data(self):
        dbconn = self.dbconn
        delivery = dbconn.query(Delivery, Payment.name).filter(Delivery.payment_id == Payment.payment_id)
        data = E.data()
        data_tag = data.xpath('//data')[0]
        for p in delivery:
            data_tag.append(E.delivery(payment_id=str(p[0].payment_id), delivery_id=str(p[0].delivery_id), name=p[0].name, note=p[0].note, payment_name = p[1]))
        return data

class price_delivery_page(template_base):
    cls__kwds = set([ 'other' ])
    cls__title = u"Стоимость доставок"
    cls__xsllist = [
        ('', '__root__.xsl'),
        ('body', 'price_delivery.xsl'),
        ('form', '__simpleedit__.xsl'),
    ]
    class callback_form(form_base):
        fields = [
            field('delivery_id', 0, int, ValueError),
            field('name',''),
            field('price',0),
            field('action',''),
            ]
        labels = {
                'name':u'Имя',
                'price':u'Стоимость',
                }

    def logic(self):
        action = self.form['action']
        name = self.form['name']
        price = self.form['price']
        delivery_id = self.form['delivery_id']
        self.form['action'] = 'check'
        dbconn = self.dbconn
        if action == 'check':
            if delivery_id == 0 and  price and name:
                delivery = Price_delivery(name, price)
                dbconn.add(delivery)
                try:
                    dbconn.commit()
                except:
                    self.errors.append(u'Конфликт имен')
            elif delivery_id and  price and name:
                try:
                    delivery = dbconn.query(Price_delivery).filter(Price_delivery.price_delivery_id == delivery_id).one()
                except sqlalchemy.orm.exc.NoResultFound:
                    sys.exc_clear()
                    return
                try:
                    delivery.name = name
                    delivery.price = price
                    dbconn.commit()
                except:
                    self.errors.append(u'Изменения не были сохранены')
        elif action == 'delete':
            try:
                delivery = dbconn.query(Price_delivery).filter(Price_delivery.price_delivery_id == delivery_id).one()
            except sqlalchemy.orm.exc.NoResultFound:
                sys.exc_clear()
                self.form['delivery_id'] = 0
                self.form['action'] = 'check'
                return
            try:
                dbconn.delete(delivery)
                dbconn.commit()
            except:
                self.errors.append(u'Изменения не были сохранены')
            self.form['delivery_id'] = 0
            self.form['action'] = 'check'
        if self.results:
            self.form['delivery_id'] = 0
            self.form['price'] = 0
            self.form['name'] = ''


    def E_data(self):
        dbconn = self.dbconn
        delivery = dbconn.query(Price_delivery)
        data = E.data()
        data_tag = data.xpath('//data')[0]
        for p in delivery:
            data_tag.append(E.delivery(delivery_id=str(p.price_delivery_id), name=p.name, price=str(p.price)))
        return data

class payment_page(template_base):
    cls__kwds = set([ 'other' ])
    cls__title = u"Типы оплаты"
    cls__xsllist = [
        ('', '__root__.xsl'),
        ('body', 'payment.xsl'),
        ('form', '__simpleedit__.xsl'),
    ]
    cls__externals = [
        '/data/richedit.js',
    ]
    class callback_form(form_base):
        fields = [
            field('payment_id', 0, int, ValueError),
            field('sale_type','all'),
            field('name',''),
            field('discription',''),
            field('action',''),
            ]
        labels = {'sale_type':u'Покупатель',
                'name':u'Имя',
                'discription':u'Описание'}
        ftypes = {'sale_type':'select'}
        def select_sale_type(self, field):
            return E.options(E.option(E.value('org_vat'), u'Платедьщик НДС'),
                            E.option(E.value('org'), u'Неплательщик НДС'), 
                            E.option(E.value('pp'), u'Физическое лицо'), 
                            )

    def logic(self):
        action = self.form['action']
        payment_id = self.form['payment_id']
        name = self.form['name']
        sale_type = self.form['sale_type']
        discription = self.form['discription']
        self.form['action'] = 'check'
        text = self.req.POST.get('richEdit0', '')
        dbconn = self.dbconn
        if action == 'check':
            if payment_id == 0 and sale_type and discription and name:
                payment = Payment(name, discription, sale_type, text)
                dbconn.add(payment)
                try:
                    dbconn.commit()
                except:
                    self.errors.append(u'Конфликт имен')
            elif sale_type and discription and name and payment_id:
                try:
                    payment = dbconn.query(Payment).filter(Payment.payment_id == payment_id).one()
                except sqlalchemy.orm.exc.NoResultFound:
                    sys.exc_clear()
                    return
                try:
                    payment.name = name
                    payment.sale_type = sale_type
                    payment.discription = discription
                    payment.text_email = text
                    dbconn.commit()
                except:
                    self.errors.append(u'Изменения не были сохранены')
        elif action == 'delete':
            try:
                payment = dbconn.query(Payment).filter(Payment.payment_id == payment_id).one()
            except sqlalchemy.orm.exc.NoResultFound:
                sys.exc_clear()
                self.form['payment_id'] = 0
                self.form['action'] = 'check'
                return
            try:
                dbconn.delete(payment)
                dbconn.commit()
            except:
                self.errors.append(u'Изменения не были сохранены')
            self.form['payment_id'] = 0
            self.form['action'] = 'check'
        if self.results:
            self.form['payment_id'] = 0
            self.form['name'] = ''
            self.form['discription'] = ''


    def E_data(self):
        dbconn = self.dbconn
        payment = dbconn.query(Payment)
        try: 
            p = dbconn.query(Payment).filter(Payment.payment_id == self.form['payment_id']).one()
            text = p.text_email.replace('\n', " ").replace("'", '"')
        except sqlalchemy.orm.exc.NoResultFound:
            sys.exc_clear()
            text = u'Реквизиты'
        data = E.data(E.rich(), text=text)
        data_tag = data.xpath('//data')[0]
        for p in payment:
            data_tag.append(E.payment(payment_id=str(p.payment_id), name=p.name, sale_type=p.sale_type, discription=p.discription))
        return data
class status_page(template_base):
    cls__kwds = set([ 'other' ])
    cls__title = u"Статусы заказов"
    cls__xsllist = [
        ('', '__root__.xsl'),
        ('body', 'status.xsl'),
        ('form', '__simpleedit__.xsl'),
    ]
    class callback_form(form_base):
        fields = [
            field('status_id', 0, int, ValueError),
            field('name',''),
            field('action',''),
            ]
        labels = {
                'name':u'Имя',
                }

    def logic(self):
        action = self.form['action']
        status_id = self.form['status_id']
        name = self.form['name']
        self.form['action'] = 'check'
        dbconn = self.dbconn
        if action == 'check':
            if  status_id == 0 and name:
                status = Status_order(name)
                dbconn.add(status)
                try:
                    dbconn.commit()
                except:
                    self.errors.append(u'Конфликт имен')
            elif name and status_id:
                try: 
                    status = dbconn.query(Status_order).filter(Status_order.status_order_id == status_id).one()
                except sqlalchemy.orm.exc.NoResultFound:
                    sys.exc_clear()
                    return
                try:
                    status.name = name
                    dbconn.commit()
                except:
                    self.errors.append(u'Изменения не были сохранены')
        elif action == 'delete':
            try:
                status = dbconn.query(Status_order).filter(Status_order.status_order_id == status_id).one()
            except sqlalchemy.orm.exc.NoResultFound:
                sys.exc_clear()
                return
            try:
                dbconn.delete(status)
                dbconn.commit()
            except:
                self.errors.append(u'Изменения не были сохранены')
        if self.results:
            self.form['status_id'] = 0
            self.form['name'] = ''
    def E_data(self):
        dbconn = self.dbconn
        status = dbconn.query(Status_order)
        data = E.data()
        data_tag = data.xpath('//data')[0]
        for p in status:
            data_tag.append(E.status(status_id=str(p.status_order_id), name=p.name))
        return data



class banner_page(template_base):
    cls__kwds = set([ 'other' ])
    cls__title = u"Баннеры"
    cls__xsllist = [
        ('', '__root__.xsl'),
        ('body', 'banner.xsl'),
        ('form', '__simpleedit__.xsl'),
    ]
    class callback_form(form_base):
        fields = [
            field('banner_id', 0, int, ValueError),
            field('name',None, complexity=True),
            field('mark',''),
            field('link',''),
            field('alt',''),
            field('title',''),
            field('action',''),
            ]
        labels = {
                'name':u'Загрузиет баннер',
                'mark':u'Выберите тип',
                'link':u'Ссылка',
                'alt':u'Подсказка',
                'title':u'Название',
                }
        ftypes = {
                'name':'file',
                'mark':'select'
                }
        def select_mark(self, field):
            return E.options(E.option(E.value('left'), u'слева'),
                            E.option(E.value('right'), u'справа'), 
                            E.option(E.value('top'), u'сверху'), 
                            E.option(E.value('bottom'), u'снизу'), 
                            )
    def E_form(self):
        return template_base.E_form(self, multipart='yes')
    
    
    
    def logic(self):
        action = self.form['action']
        banner_id = self.form['banner_id']
        name = self.form['name']
        link = self.form['link']
        alt = self.form['alt']
        title = self.form['title']
        mark = self.form['mark']
        self.form['action'] = 'check'
        dbconn = self.dbconn
        if action == 'check':
            if  banner_id == 0 and name is not None  and mark and link and alt and title:
                filename = name.filename
                f = name.file
                img = Image.open(f)
                img.save(htdocs_dir+'/data/'+filename)
                banner = Banners(filename, link, alt, title, mark)
                dbconn.add(banner)
                try:
                    dbconn.commit()
                except:
                    self.errors.append(u'Конфликт имен')
            elif banner_id  and mark and link and alt and title:
                try: 
                    banner = dbconn.query(Banners).filter(Banners.banner_id == banner_id).one()
                except sqlalchemy.orm.exc.NoResultFound:
                    sys.exc_clear()
                    return
                try:
                    banner.alt = alt
                    banner.title = title
                    banner.link = link
                    banner.mark = mark
                    dbconn.commit()
                except:
                    self.errors.append(u'Изменения не были сохранены')
        elif action == 'delete':
            try:
                banner = dbconn.query(Banners).filter(Banners.banner_id == banner_id).one()
            except sqlalchemy.orm.exc.NoResultFound:
                sys.exc_clear()
                return
            try:
                dbconn.delete(banner)
                dbconn.commit()
            except:
                self.errors.append(u'Изменения не были сохранены')
        if self.results:
            self.form['banner_id'] = 0
            self.form['name'] = ''
            self.form['alt'] = ''
            self.form['title'] = ''
            self.form['link'] = ''


    def E_data(self):
        dbconn = self.dbconn
        status = dbconn.query(Banners)
        data = E.data()
        data_tag = data.xpath('//data')[0]
        for p in status:
            data_tag.append(E.banner(banner_id=str(p.banner_id), name=p.name, title=p.title, alt=p.alt, link=p.link, mark=p.mark))
        return data
