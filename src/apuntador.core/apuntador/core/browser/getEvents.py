# -*- coding: utf-8 -*-
from zope.publisher.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from Acquisition import aq_inner
from datetime import datetime
import json
from apuntador.core.browser.dicttoxml import dicttoxml
from plone.app.event.dx.behaviors import EventAccessor

import uuid
import os
import pytz

from xlsxwriter.workbook import Workbook
from plone.app.uuid.utils import uuidToObject


def create_xlsx(dades):
    name = uuid.uuid4().hex
    workbook = Workbook(name + '.xlsx')
    worksheet = workbook.add_worksheet()

    worksheet.set_column('C:C', 20)
    worksheet.set_column('D:D', 70)
    worksheet.set_column('E:E', 20)
    worksheet.set_column('H:H', 70)
    worksheet.set_column('I:I', 70)

    bold = workbook.add_format({'bold': True})

    different_day_format = workbook.add_format({'bg_color': '#C6EFCE',
                                                'font_color': '#006100'})
    row = 0
    col = 0

    main_titles = [
        'Data inici',
        'Data fi',
        'Etiquetes',
        'Títol'.decode('utf-8'),
        'Usuari',
        'Hora inici',
        'Hora fi',
        'Lloc',
        'Descripció'.decode('utf-8')]

    for title in main_titles:
        worksheet.write(row, col, title, bold)
        col += 1

    row += 2
    for esdeveniment in dades:

        obj = uuidToObject(esdeveniment['uid'])

        etiquetes = ''
        for uuid_etiqueta in obj.etiquetes:
            etiquetes += uuidToObject(uuid_etiqueta).title
            etiquetes += ', '
        etiquetes = etiquetes[:-2]

        start = esdeveniment['start'].split(' ')
        start_day = start[0]
        start_hour = start[1]
        end = esdeveniment['end'].split(' ')
        end_day = end[0]
        end_hour = end[1]

        col = 0
        # data inici
        worksheet.write(row, col, start_day)
        col += 1
        # data fi
        if start_day == end_day:
            worksheet.write(row, col, end_day)
        else:
            worksheet.write(row, col, end_day, different_day_format)
        col += 1
        # etiquetes
        worksheet.write(row, col, etiquetes)
        col += 1
        # titol
        worksheet.write(row, col, esdeveniment['title'])
        col += 1
        # usuari
        worksheet.write(row, col, esdeveniment['creator'])
        worksheet.write(row, col, esdeveniment['path'].split('/')[3])
        col += 1
        # hora inici
        worksheet.write(row, col, start_hour)
        col += 1
        # hora fi
        worksheet.write(row, col, end_hour)
        col += 1
        # lloc
        worksheet.write(row, col, esdeveniment['lloc'])
        col += 1
        # descripcio
        worksheet.write(row, col, esdeveniment['description'])
        row += 2

    workbook.close()

    down = open(name + '.xlsx', 'r')
    tornar = down.read()
    down.close()

    os.remove(name + '.xlsx')

    return tornar


class getEvents(BrowserView):

    def __call__(self):
        """ Retorna en format json els esdeveniments del sistema.
        Accepta els següents paràmetres:
            - data_inici_min:   data en format dd/mm/aaaa
            - data_inici_max:   data en format dd/mm/aaaa
            - data_final_min:   data en format dd/mm/aaaa
            - data_final_max:   data en format dd/mm/aaaa
            - publics:          llistat uids separat per comes
            - etiquetes:        llistat uids separat per comes
            - cicles:           llistat uids separat per comes
            - descriptors:      llistat uids separat per comes
            - portals:          llistat uids separat per comes
            - destacat:        llista els destacats si true
            - sort_on:          index pel que es pugui ordenar (start, sortable_title, etc)
            - sort_order:       'ascending' o 'descending'
        """

        context = aq_inner(self.context)
        dades = []
        query = {'portal_type': 'esdeveniment'}

        # dates

        data_inici_min = data_inici_max = data_final_min = data_final_max = False

        if 'data_inici_min' in context.REQUEST:
            data_inici_min = datetime.strptime(context.REQUEST.get('data_inici_min'), '%d/%m/%Y')
        if 'data_inici_max' in context.REQUEST:
            data_inici_max = datetime.strptime(context.REQUEST.get('data_inici_max'), '%d/%m/%Y')
        if 'data_final_min' in context.REQUEST:
            data_final_min = datetime.strptime(context.REQUEST.get('data_final_min'), '%d/%m/%Y')
        if 'data_final_max' in context.REQUEST:
            data_final_max = datetime.strptime(context.REQUEST.get('data_final_max'), '%d/%m/%Y')

        if data_inici_min and data_inici_max:
            query['start'] = {'query': (data_inici_min, data_inici_max), 'range': 'min:max'}
        elif data_inici_min:
            query['start'] = {'query': (data_inici_min), 'range': 'min'}
        elif data_inici_max:
            query['start'] = {'query': (data_inici_max), 'range': 'max'}

        if data_final_min and data_final_max:
            query['end'] = {'query': (data_final_min, data_final_max), 'range': 'min:max'}
        elif data_final_min:
            query['end'] = {'query': (data_final_min), 'range': 'min'}
        elif data_final_max:
            query['end'] = {'query': (data_final_max), 'range': 'max'}

        # característiques

        if 'publics' in context.REQUEST:
            publics = context.REQUEST.get('publics')
            query['esdeveniment_publics'] = publics.split(',')

        if 'etiquetes' in context.REQUEST:
            etiquetes = context.REQUEST.get('etiquetes')
            query['esdeveniment_etiquetes'] = etiquetes.split(',')

        if 'cicles' in context.REQUEST:
            cicles = context.REQUEST.get('cicles')
            query['esdeveniment_cicles'] = cicles.split(',')

        if 'descriptors' in context.REQUEST:
            descriptors = context.REQUEST.get('descriptors')
            query['esdeveniment_descriptors'] = descriptors.split(',')

        if 'portals' in context.REQUEST:
            portals = context.REQUEST.get('portals')
            query['esdeveniment_portals'] = portals.split(',')

        # ordre

        if 'sort_on' in context.REQUEST:
            query['sort_on'] = context.REQUEST.get('sort_on')

            if 'sort_order' in context.REQUEST:
                query['sort_order'] = context.REQUEST.get('sort_order')

        if 'destacat' in context.REQUEST and context.REQUEST.get('destacat') == 'true':
            query['destacat'] = True

        pc = getToolByName(context, "portal_catalog")
        esdeveniments = pc(query)

        for esdeveniment in esdeveniments:
            esdeveniment = esdeveniment.getObject()
            accessor = EventAccessor(esdeveniment)

            try:
                uid_text = esdeveniment.UID().decode('utf-8')
            except UnicodeDecodeError:
                uid_text = "Error"

            try:
                title_text = esdeveniment.Title().decode('utf-8')
            except UnicodeDecodeError:
                title_text = "Error"

            try:
                description_text = esdeveniment.Description().decode('utf-8')
            except UnicodeDecodeError:
                description_text = "Error"

            try:
                creator_text = esdeveniment.Creator().decode('utf-8')
            except UnicodeDecodeError:
                creator_text = "Error"

            try:
                try:
                    location_text = accessor.location.decode('utf-8')
                except:
                    location_text = accessor.location
            except UnicodeDecodeError:
                location_text = "Error"

            try:
                text_text = accessor.text
            except UnicodeDecodeError:
                text_text = "Error"
            except UnicodeEncodeError:
                text_text = "Error"

            url_image = ""
            default_image = True
            if esdeveniment.event_image:
                url_image = esdeveniment.absolute_url() + '/@@images/event_image'
                default_image = False
            else:
                path_to_view = '/'.join(esdeveniment.getPhysicalPath())
                try:
                    view = self.context.unrestrictedTraverse(path_to_view + '/faceted-preview-item')
                    url_image = view.getEventImage().absolute_url()
                except:
                    url_image = 'http://lapuntador.cat/tags/imatges-generiques/recurs4.jpg'
                default_image = True

            dades_esdeveniment = {
                'uid': uid_text,
                'id': esdeveniment.id,
                'title': title_text,
                'description': description_text,
                'start': esdeveniment.start.astimezone(pytz.timezone('Europe/Andorra')).strftime('%d/%m/%y %H:%M'),
                'end': esdeveniment.end.astimezone(pytz.timezone('Europe/Andorra')).strftime('%d/%m/%y %H:%M'),
                'path': '/'.join(esdeveniment.getPhysicalPath()),
                'creator': creator_text,
                'lloc': location_text,
                'text': text_text,
                'destacat': str(esdeveniment.destacat),
                'image': url_image,
                'default_image': default_image
            }

            dades.append(dades_esdeveniment)

        # output
        if 'output' in context.REQUEST:
            output = context.REQUEST.get('output')
        else:
            output = 'xml'

        # json output
        if output == 'json':
            self.request.response.setHeader('Content-Type', 'application/json;;charset="utf-8"')
            return json.dumps(dades)

        # xml output
        elif output == 'xml':
            # self.request.RESPONSE.setHeader('Content-Type', 'application/xlsx')
            # self.request.RESPONSE.addHeader("Content-Disposition", "filename=%s.xlsx" % self.context.getId())
            # return create_xlsx(dades)
            self.request.response.setHeader('Content-Type', 'text/xml;;charset="utf-8"')
            return dicttoxml(dades, True, False)

        # xlsx output
        elif output == 'xlsx':
            self.request.RESPONSE.setHeader('Content-Type', 'application/xlsx')
            self.request.RESPONSE.addHeader("Content-Disposition", "filename=%s.xlsx" % self.context.getId())
            return create_xlsx(dades)
