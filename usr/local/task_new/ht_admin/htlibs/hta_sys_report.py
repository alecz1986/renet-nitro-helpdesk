#
# -*- coding: utf-8 -*-

import sys
import re
import sqlalchemy
import sqlalchemy.orm
from sqlalchemy import func
from sqlalchemy import not_
from rrduet.rr_template import field, E
import datetime
from sqlalchemy import desc
import hta_config
from hta_base import check_action
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
import csv
import cStringIO
from lxml import etree
import cStringIO
import tempfile
from hta_config import htdocs_dir
import os

class report_order(template_base):
    cls__title = u"Отчет по заказам"
    cls__kwds = set([ 'report' ])
    cls__xsllist = [
        ('', '__root__.xsl'),
        ('body', 'report_order.xsl'),
        ('form', '__simpleedit__.xsl'),
    ]
    class callback_form(form_base):
        fields = [
            field('date_begin', ''),
            field('date_end', ''),
            field('distrib_id', -1, int, ValueError),
            ]
        labels = {
            'date_begin':u'Начало периода',
            'date_end':u'Конец периода',
            'distrib_id':u'Поставщик',
                }
        ftypes = {
            'date_begin':'date',
            'date_end':'date',
            'distrib_id':'select',
                }
        def select_distrib_id(self, field):
            options = []
            options.append(E.option(E.value('0'),u'все'))
            for r in self.template_ref().dbconn.query(Distributor).filter(Product.distrib_id==Distributor.distrib_id):
                options.append(E.option(E.value(str(r.distrib_id)), "%s" % (r.discription)))
#            options.append(E.option(E.value('-1'),u'----------------'))
            return E.options(*options)
    def E_data(self):
        dbconn = self.dbconn
        form = self.form
        date_begin = form['date_begin']
        date_end = form['date_end']
        distrib_id = form['distrib_id']
        orders_tag = E.orders()
        data = E.data(orders_tag)
        limit = 100
        if distrib_id==--1:
            return E.data()
        ids = set(r[0] for r in dbconn.execute('select * from(select * from (select order_id, status_order_id from porder join history_prod using(order_id) order by porder.order_id, history_prod.datetime desc) as c  group by order_id ) as d where status_order_id=9'))
        query = dbconn.query(Order).filter(not_(Order.order_id.in_(ids)))
        if date_begin:
            limit = 0
            query = query.filter(Order.datetime >= date_begin)
        if date_end:
            limit = 0
            query = query.filter(Order.datetime <= date_end)
        if distrib_id:
            query = query.filter(Order.order_id == Prod_order.order_id).filter(Prod_order.product_id == Product.product_id).filter(Product.distrib_id == distrib_id)
            for order in query:
                res = 0
                test = dbconn.query(Prod_order.amount,Prod_order.count, Prod_order.close, Prod_order.sale).filter(Prod_order.order_id == order.order_id).filter(Prod_order.close == "no").filter(Prod_order.product_id == Product.product_id).filter(Product.distrib_id == distrib_id)
                for amount, count, close, sale in test:
                    res += float(amount)*float(count)-float(sale)
                order.amount = float(res)
        all_amount = 0
        query = query.order_by(desc(Order.datetime))
        if limit:
            query = query.limit(limit)
        count = 0
        for order in query:
            count += 1
            all_amount += float(order.amount)
            orders_tag.append(E.order(datetime=order.datetime.strftime('%Y-%m-%d'), order_id=str(order.order_id), amount=str(order.amount)))
        orders_tag.append(E.all_amount(str(all_amount)))
        if limit:
            str_limit =u"Выведены %s заказов" % str(limit)
        elif (date_begin or date_end or distrib_id):
            str_limit =u"Выведены все заказы"
        data.append(E.limit(limit=str_limit))
        data.append(E.count(str(count)))
        return data

def get_xml():
    import httplib
    import urllib
    conn = httplib.HTTPSConnection('spreadsheets.google.com')
#    query='/pub?key=0AvrCgOS5tokYdEtzLTlBVFlSR0hENEZNY1hiczZQdVE&hl=ru&single=true&gid=0&output=csv'
    query='/pub?key=0Ambqbsv_BCEodE52NHlwN19GeWI4cnNibnRWcWRjUXc&authkey=CKP8jtcD&hl=en&output=csv'
    try:
        conn.request("GET", query, None, {})
        resp = conn.getresponse()
        answer = resp.read()
        return answer
    except Exception, ex:
        return None

class report_management(template_base):
    cls__title = u"Управленческий учет"
    cls__kwds = set([ 'report' ])
    cls__xsllist = [
        ('', '__root__.xsl'),
        ('body', 'report_management.xsl'),
    ]
    def E_data(self):
        colors = ['red', '#000080', '#006400', '#B22222', 'black','#FF1493', '#CC00CC',  '#8B0A50','#660066', '#0033CC', '#666600', '#666666', 'green', 'blue', '#000000', '#B22222', '#CC0099', '#663300', '#6633CC', '#663366', '#00FFFF', '#000080', '#006400', '#B22222', 'black',  '#8B0A50','#660066', '#0033CC']
        get = self.req.POST
        f = get.get('csv')

        if f is not None:
            try:
                f = f.file
                content = f.read() 
#                content = content.read()
                tempfd, fname = tempfile.mkstemp(prefix='change', suffix='.csv', dir=htdocs_dir+'/csv/')
                temp = os.fdopen(tempfd, "w")
                temp.write(content)
                temp.close()
                del temp
                get['csv'] = fname
                xml = cStringIO.StringIO(content)
            except:
                xml = cStringIO.StringIO(get_xml())
        else:
            xml = cStringIO.StringIO(get_xml())
        get_params = E.gets(* [etree.Element(p, value=get.get(p)) for p in get])
        res = []
        for p in get:
            res.append(p+'='+get.get(p))
        get_params.append(E.params('&'.join(res)))
        if xml is None:
            return E.data()
        reader = csv.reader(xml, dialect='excel', delimiter=str(','), lineterminator='\r\n')
        test = iter(reader)
        params_name = reader.next()[2:]
        params = reader.next()[2:]
        params_name.append('количество заказов')
        params.append('_count_order')
        res = []
        for i in params:
            if i.startswith('_'):
                res.append((i, params_name[params.index(i)], params.index(i)))
        all_params = E.params(*[E.param(name=p[0], color=colors[res.index(p)], check=str(int(get.get(p[0]) is not None)), count=str(res.index(p)+1), value=p[1].decode('utf-8')) for p in res])
        return E.data(get_params, all_params)
def date(date):
    d = date.split('-')
    return datetime.date(int(d[0]), int(d[1]), int(d[2]))

class data(template_base):
    cls_title=''
    cls_kwds = set([' report'])
    cls_xsllist = [
        ('', '__root__.xsl')
            ]
    def logic(self):
        get = self.req.GET
        date_begin = get.get('date_begin')
        date_end = get.get('date_end')
        f = get.get('csv')
        if f:
            xml = open(f, 'r') 
        else:
            xml = cStringIO.StringIO(get_xml())
        if xml is None:
            return
        reader = csv.reader(xml, dialect='excel', delimiter=str(','), lineterminator='\r\n')
        it = iter(reader)
        names = it.next()
        params = it.next()
        kaka = it.next()
        params_dict={}
        index_count = -1
        all_params = 0
        for i in range(len(params)):
            if params[i] == 'sale_name':
                index_count = i
            if  params[i].startswith('_'):
                all_params+=1
            params_dict[params[i]] = i
        do = False
        for i in get:
            if i in params or i=='_count_order':
                do = True
        do = True
        if not date_begin and do:
            date_begin=datetime.date(1900, 1, 1).strftime('%Y-%m-%d')
        if not date_end and do:
            date_end=datetime.date(9999, 12, 31).strftime('%Y-%m-%d')
        start_date = date(date_begin)
        date_end = date(date_end)
        res = ''
        dt = ''
        opts ={} 
        count = 0
        for i, line in enumerate(it):
            d = line[0]
            #.replace('.', '-').split('-')
            #d = '-'.join([d[2],d[1], d[0]])
            check_date = date(d)
            if start_date<=check_date and check_date<=date_end:
                if dt != line[0]:
                    dt = line[0]
                    count = ','+str(count)
                    vals = []
                    if res:
                        for name in params:
                            if name.startswith('_') and name in opts:
                                vals.append(str(opts[name]))
                            elif name.startswith('_'):
                                vals.append('0')
                    if vals:
 #                       res+=','.join(vals)+count+'\n'+d+'T12:00:00,'
                        res+=','.join(vals)+count+'\n'+d+','
                    else:
#                        res+=d+'T12:00:00,'
                        res+=d+','
                    count = 0
                    opts ={} 
                for j in range(len(line)):
                    if params[j].startswith('_'):
                        if 'amount' in params[j]:
                            if params[j] in opts:
                                if line[j]:
                                    opts[params[j]] = float(opts[params[j]])+float(line[j])
                            elif line[j]:
                                try:
                                    opts[params[j]] = float(line[j])
                                except:
                                    sys.exc_clear
                        elif line[j]!='':
                            try:
                                opts[params[j]] = float(line[j])
                            except:
                                sys.exc_clear
                        elif params[j] not in opts:
                            opts[params[j]] = 0
                    elif j == index_count and line[j]!='':
                        count+=1
        count = ','+str(count)
        vals = []
        for name in params:
            if name.startswith('_') and name in opts:
                vals.append(str(opts[name]))
            elif name.startswith('_'):
                vals.append('0')
        if res:
            for i in range(all_params-len(vals)):
                vals.append('0')
        if vals:
            for i in range(all_params-len(vals)):
                vals.append('0')
            res+=','.join(vals)+count
        self.resp.content_type = 'text/x-csv'
        self.resp.body = '#\n#\n#\n'+res 
#       self.resp.headers['Content-Disposition'] = 'attachment; filename="export_pricelist%s.csv"'% str(distrib_id)
        return True

months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
def create_date(date):
	date_params=str(date).split('-')
	t = months[int(date_params[1])-1]+' '+str(date_params[2])+' '+str(date_params[0])+' 0:00:00 GMT+3'
	return t
def create_date_end(date):
	date_params=str(date).split('-')
	t = months[int(date_params[1])-1]+' '+str(date_params[2])+' '+str(date_params[0])+' 23:59:59 GMT+3'
	return t
class event(template_base):
    cls_title=''
    cls_kwds = set([' report'])
    cls_xsllist = [
        ('', '__root__.xsl')
            ]
    def logic(self):
        get = self.req.GET
        date_begin = get.get('date_begin')
        date_end = get.get('date_end')
        f = get.get('csv')
        if f:
            xml = open(f, 'r') 
        else:
            xml = cStringIO.StringIO(get_xml())
        if xml is None:
            return
        reader = csv.reader(xml, dialect='excel', delimiter=str(','), lineterminator='\r\n')
        it = iter(reader)
        names = it.next()
        params = it.next()
        kaka = it.next()
        res = ''
        do = False 
        for i in get:
            if i in params or i=='_count_order':
                do = True
        if not date_begin and do:
            date_begin=datetime.date(1900, 1, 1).strftime('%Y-%m-%d')
        if not date_end and do:
            date_end=datetime.date(9999, 12, 31).strftime('%Y-%m-%d')
        start_date = date(date_begin)
        date_end = date(date_end)
        dt = ''
        res_event = ''
        for i, line in enumerate(it):
#            d = line[0].replace('.', '-').split('-')
            t = line[0]
            #'-'.join([d[2],d[1], d[0]])
            check_date = date(t)
            if start_date<=check_date and check_date<=date_end:
                if dt!=line[0] and len(line)>1 and line[1]:
                    dt = line[0]
                    if res_event:
                        res+=res_event+'\n</event>\n'
                    if len(line)>1 and line[1]:
                        res+='<event start="'+create_date(t)+'" end="'+create_date_end(t)+'" isDuration="false" title="'+t+'">\n'
#                        res+='<event start="'+create_date(t)+'"   title="'+t+'">\n'
                    res_event=''
                if len(line)>1 and line[1]:
                    if res_event:
                        res_event+=','
                    res_event+=line[1]
        if res_event:
            res+=res_event+'\n</event>\n'
        self.resp.content_type = 'text/xml'
        self.resp.body = '<?xml version="1.0" encoding="utf-8"?>\n<data>\n'+res+'</data>'
#       self.resp.headers['Content-Disposition'] = 'attachment; filename="export_pricelist%s.csv"'% str(distrib_id)
        f = open('test.xml', 'w')
        f.write(self.resp.body)
        f.close()
        return True
class params(template_base):
    cls_title=''
    cls_kwds = set([' report'])
    cls_xsllist = [
        ('', '__root__.xsl')
            ]
    def logic(self):
        get = self.req.POST
        f = get.get('file')
        res = ''
        if f is not None:
            content = f.file
            xml= cStringIO.StringIO(content)
            reader = csv.reader(xml, dialect='excel', delimiter=str(','), lineterminator='\r\n')
            test = iter(reader)
            params = reader.next()[2:]
            res = ','.join(params)
        return True
