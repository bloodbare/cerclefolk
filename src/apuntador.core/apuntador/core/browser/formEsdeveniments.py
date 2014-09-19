# -*- coding: utf-8 -*-
from five import grok
from plone.directives import form
from z3c.form import button
from zope import schema
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from apuntador.core import _
from apuntador.core.esdeveniment import etiquetes_vocabulary, publics_vocabulary, cicles_vocabulary, descriptors_vocabulary, portals_vocabulary
from Products.CMFCore.interfaces import ISiteRoot
from datetime import datetime


sort_order_vocabulary = SimpleVocabulary([
    SimpleTerm(value=u"ascending", title=_(u"Ascendent")),
    SimpleTerm(value=u"descending", title=_(u"Descendent"))
])

sort_on_vocabulary = SimpleVocabulary([
    SimpleTerm(value=u"sortable_title", title=_(u"Títol")),
    SimpleTerm(value=u"effective", title=_(u"Data de publicació")),
    SimpleTerm(value=u"start", title=_(u"Data inicial")),
    SimpleTerm(value=u"end", title=_(u"Data final")),
])

output_vocabulary = SimpleVocabulary([
    SimpleTerm(value=u"xml", title=_(u"XML")),
    SimpleTerm(value=u"json", title=_(u"Json")),
    SimpleTerm(value=u"xlsx", title=_(u"Xlsx"))
])


class ISearchEventsSchema(form.Schema):

    data_inici_min = schema.Date(title=_(u"Que comenci com a mínim"),
                                 description=_(u""),
                                 required=False)

    data_inici_max = schema.Date(title=_(u"Que comeci com a màxim"),
                                 description=_(u""),
                                 required=False)

    data_final_min = schema.Date(title=_(u"Que acabi com a mínim"),
                                 description=_(u""),
                                 required=False)

    data_final_max = schema.Date(title=_(u"Que acabi com a màxim"),
                                 description=_(u""),
                                 required=False)

    etiquetes = schema.List(title=_(u"Etiquetes"),
                            description=u"",
                            required=False,
                            value_type=schema.Choice(source=etiquetes_vocabulary))

    publics = schema.List(title=_(u"Públic"),
                          description=u"",
                          required=False,
                          value_type=schema.Choice(source=publics_vocabulary))

    cicles = schema.List(title=_(u"Cicles"),
                         description=u"",
                         required=False,
                         value_type=schema.Choice(source=cicles_vocabulary))

    descriptors = schema.List(title=_(u"Descriptors"),
                              description=u"",
                              required=False,
                              value_type=schema.Choice(source=descriptors_vocabulary))

    destacat = schema.Bool(title=_(u"Destacats"))

    portals = schema.List(title=_(u"Portals"),
                          description=u"",
                          required=False,
                          value_type=schema.Choice(source=portals_vocabulary))

    sort_on = schema.Choice(title=_(u"Ordenar per"),
                            description=u"",
                            required=False,
                            vocabulary=sort_on_vocabulary)

    sort_order = schema.Choice(title=_(u"Ordre"),
                               description=u"",
                               required=False,
                               vocabulary=sort_order_vocabulary)

    output = schema.Choice(title=_(u"Sortida"),
                           description=u"",
                           required=False,
                           vocabulary=output_vocabulary)


class SearchEventsForm(form.SchemaForm):
    grok.require('zope2.View')

    schema = ISearchEventsSchema

    # the form does not care about the context object and should not try to extract field value defaults out of it
    ignoreContext = True

    # only available at the site root only
    grok.context(ISiteRoot)

    # http://yourhost/@@search_events
    grok.name("search_events")

    @button.buttonAndHandler(u'Cercar')
    def handleSave(self, action):
        data, errors = self.extractData()
        if errors:
            return False

        params = []

        # característiques

        if len(data['etiquetes']) > 0:
            params.append('etiquetes=' + ','.join(data['etiquetes']))
        if len(data['publics']) > 0:
            params.append('publics=' + ','.join(data['publics']))
        if len(data['cicles']) > 0:
            params.append('cicles=' + ','.join(data['cicles']))
        if len(data['descriptors']) > 0:
            params.append('descriptors=' + ','.join(data['descriptors']))
        if len(data['portals']) > 0:
            params.append('portals=' + ','.join(data['portals']))

        # ordre

        if data['sort_on']:
            params.append('sort_on=' + data['sort_on'])
        if data['sort_order']:
            params.append('sort_order=' + data['sort_order'])

        # dates

        if data['data_inici_min']:
            params.append('data_inici_min=' + datetime.strftime(data['data_inici_min'], '%d/%m/%Y'))
        if data['data_inici_max']:
            params.append('data_inici_max=' + datetime.strftime(data['data_inici_max'], '%d/%m/%Y'))
        if data['data_final_min']:
            params.append('data_final_min=' + datetime.strftime(data['data_final_min'], '%d/%m/%Y'))
        if data['data_final_max']:
            params.append('data_final_max=' + datetime.strftime(data['data_final_max'], '%d/%m/%Y'))

        # output

        if data['output']:
            params.append('output=' + data['output'])

        if 'destacat' in data:
            if data['destacat']:
                params.append('destacat=true')
            else:
                params.append('destacat=false')

        url = '/@@getEvents'
        if len(params) > 0:
            url += '?'
            url += '&'.join(params)

        self.request.response.redirect(self.context.absolute_url() + url)
