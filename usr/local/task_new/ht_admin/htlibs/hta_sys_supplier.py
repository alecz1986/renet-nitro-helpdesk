# -*- coding: utf-8 -*-

import os
import sys
import re
from rrduet.rr_template import field, E
import hta_config
from hta_base import check_action
from hta_page import form_base, template_base, menu_base
from fullshopapi import Supplier
from fullshopapi import Category
import lxml.etree as et
import sqlalchemy
import sqlalchemy.orm
import csv
import cStringIO
import htu_main
from hta_config import htdocs_dir, prod_dir
from lxml.html import fragment_fromstring



class supplier(template_base):
    cls__kwds = set([ 'product' ])
    cls__title = u"Поставщики"
    cls__xsllist = [
        ('', '__root__.xsl'),
        ('body', 'supplier.xsl'),
        ('form', '__simpleedit__.xsl'),
    ]
    class callback_form(form_base):
        fields = [
            field('supplier_id',0, int, ValueError),
            field('name',''),
            field('vat',''),
            field('contact',''),
            field('phone',''),
            field('procent',''),
            field('cct',''),
            field('action',''),
        ]
        labels = {
            'name':u'Название',
            'vat':u'Тип поставщика',
            'contact': u'Контактное лицо',
            'phone':u'Телефон,icq, skype',
            'procent':u'Процент',
            'cct':u'Договор',
        }
    def logic(self):
        form = self.form

        action = form['action']
        supplier_id = form['supplier_id']
        name = form['name']
        vat = form['vat']
        contact = form['contact']
        phone = form['phone']
        procent = form['procent']
        cct = form['cct']


        form['action'] = 'check'
        dbconn = self.dbconn
        if action == 'check':
            if  supplier_id == 0 and  name and vat and contact and phone and procent and cct:
                suppl = Supplier(name, contact, vat, phone, procent, cct)
                dbconn.add(suppl)
                try:
                    dbconn.commit()
                except:
                    self.errors.append(u'Конфликт имен')
            elif supplier_id and  name and vat and contact and phone and procent and cct:
                try: 
                    suppl = dbconn.query(Supplier).filter(Supplier.supplier_id == supplier_id).one()
                except sqlalchemy.orm.exc.NoResultFound:
                    sys.exc_clear()
                    self.errors.append(u'Изменения не были сохранены')
                    return
                suppl.name = name
                suppl.contact = contact
                suppl.vat = vat
                suppl.phone = phone
                suppl.procent = procent
                suppl.cct = cct
                try:
                    dbconn.commit()
                    self.results.append(u"Изменения сохранены")
                except:
                    self.errors.append(u'Изменения не были сохранены')
                    return
        elif action == 'delete':
            try:
                suppl = dbconn.query(Supplier).filter(Supplier.supplier_id == supplier_id).one()
            except sqlalchemy.orm.exc.NoResultFound:
                sys.exc_clear()
                self.errors.append(u'Изменения не были сохранены')
                return
            dbconn.delete(suppl)
            dbconn.commit()
        if supplier_id:
            try:
                suppl = dbconn.query(Supplier).filter(Supplier.supplier_id == supplier_id).one()
            except sqlalchemy.orm.exc.NoResultFound:
                sys.exc_clear()
                form['supplier_id'] = 0
                return
            form['name'] = suppl.name
            form['contact'] = suppl.contact
            form['vat'] = suppl.vat
            form['phone'] = suppl.phone
            form['procent'] = suppl.procent
            form['cct'] = suppl.cct
            self.errors.append(u'Внимание! Режим редактирования')

    def E_data(self):
        dbconn = self.dbconn
        suppls = dbconn.query(Supplier).all()
        data = E.data()
        data_tag = data.xpath('//data')[0]
        for p in suppls: 
            data_tag.append(E.suppl(supplier_id=str(p.supplier_id),  name=p.name, vat=p.vat, contact=p.contact, phone=p.phone, procent=p.procent, cct=p.cct))
        return data

