# -*- encoding: utf-8 -*-

from five import grok
from plone.app.dexterity.behaviors.metadata import IBasic
from collective.dexteritytextindexer.utils import searchable
from zope import schema
from apuntador.core import _
from plone.namedfile.field import NamedBlobFile
from collective import dexteritytextindexer
from plone.directives import form
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.schema.interfaces import IContextSourceBinder
# from plone.app.event.dx.behaviors import IEventSummary
from plone.app.contenttypes.behaviors.richtext import IRichText
from plone.app.event.dx.behaviors import EventAccessor
from plone.app.event.browser.event_summary import EventSummaryView
from plone.event.interfaces import IRecurrenceSupport
from plone.indexer.decorator import indexer
import random
import datetime


def make_terms(items):
    """ Create zope.schema terms for vocab from tuples """
    terms = [SimpleTerm(value=pair[0], token=pair[0], title=pair[1]) for pair in items]
    return terms


@grok.provider(IContextSourceBinder)
def etiquetes_vocabulary(context):
    """ Populate vocabulary with values from portal_catalog
    """
    root = context.portal_url.getPortalObject()
    portal_catalog = root.portal_catalog
    brains = portal_catalog.searchResults(portal_type="tag", sort_on="sortable_title")
    result = [(brain["UID"], brain["Title"]) for brain in brains]
    terms = make_terms(result)
    return SimpleVocabulary(terms)


@grok.provider(IContextSourceBinder)
def publics_vocabulary(context):
    """ Populate vocabulary with values from portal_catalog
    """
    root = context.portal_url.getPortalObject()
    portal_catalog = root.portal_catalog
    brains = portal_catalog.searchResults(portal_type="public", sort_on="sortable_title")
    result = [(brain["UID"], brain["Title"]) for brain in brains]
    terms = make_terms(result)
    return SimpleVocabulary(terms)


@grok.provider(IContextSourceBinder)
def cicles_vocabulary(context):
    """ Populate vocabulary with values from portal_catalog
    """
    root = context.portal_url.getPortalObject()
    portal_catalog = root.portal_catalog
    brains = portal_catalog.searchResults(portal_type="cicle", sort_on="sortable_title")
    result = [(brain["UID"], brain["Title"]) for brain in brains]
    terms = make_terms(result)
    return SimpleVocabulary(terms)


@grok.provider(IContextSourceBinder)
def descriptors_vocabulary(context):
    """ Populate vocabulary with values from portal_catalog
    """
    root = context.portal_url.getPortalObject()
    portal_catalog = root.portal_catalog
    brains = portal_catalog.searchResults(portal_type="descriptor", sort_on="sortable_title")
    result = [(brain["UID"], brain["Title"]) for brain in brains]
    terms = make_terms(result)
    return SimpleVocabulary(terms)


@grok.provider(IContextSourceBinder)
def portals_vocabulary(context):
    """ Populate vocabulary with values from portal_catalog
    """
    root = context.portal_url.getPortalObject()
    portal_catalog = root.portal_catalog
    brains = portal_catalog.searchResults(portal_type="portal", sort_on="sortable_title")
    result = [(brain["UID"], brain["Title"]) for brain in brains]
    terms = make_terms(result)
    return SimpleVocabulary(terms)


freq_vocabulary = SimpleVocabulary([
    SimpleTerm(value=u"DAILY", title=_(u"dies")),
    SimpleTerm(value=u"WEEKLY", title=_(u"setmanes")),
    SimpleTerm(value=u"MONTHLY", title=_(u"mesos")),
    SimpleTerm(value=u"YEARLY", title=_(u"anys"))
])


month_vocabulary = SimpleVocabulary([
    SimpleTerm(value=u"1", title=_(u"gener")),
    SimpleTerm(value=u"2", title=_(u"febrer")),
    SimpleTerm(value=u"3", title=_(u"març")),
    SimpleTerm(value=u"4", title=_(u"abril")),
    SimpleTerm(value=u"5", title=_(u"maig")),
    SimpleTerm(value=u"6", title=_(u"juny")),
    SimpleTerm(value=u"7", title=_(u"juliol")),
    SimpleTerm(value=u"8", title=_(u"agost")),
    SimpleTerm(value=u"9", title=_(u"setembre")),
    SimpleTerm(value=u"10", title=_(u"octubre")),
    SimpleTerm(value=u"11", title=_(u"novembre")),
    SimpleTerm(value=u"12", title=_(u"decembre"))
])


ordinal_numbers_vocabulary = SimpleVocabulary([
    SimpleTerm(value=u"1", title=_(u"primer")),
    SimpleTerm(value=u"2", title=_(u"segon")),
    SimpleTerm(value=u"3", title=_(u"tercer")),
    SimpleTerm(value=u"4", title=_(u"quart"))
])


weekdays_vocabulary = SimpleVocabulary([
    SimpleTerm(value=u"MO", title=_(u"dilluns")),
    SimpleTerm(value=u"TU", title=_(u"dimarts")),
    SimpleTerm(value=u"WE", title=_(u"dimecres")),
    SimpleTerm(value=u"TH", title=_(u"dijous")),
    SimpleTerm(value=u"FR", title=_(u"divendres")),
    SimpleTerm(value=u"SA", title=_(u"dissabte")),
    SimpleTerm(value=u"SU", title=_(u"diumenge"))
])


class IEsdeveniment(form.Schema):

    event_url = schema.Text(title=_(u"URL de l'esdeveniment"),
                            description=_(u"Adreça web amb més informació sobre l'esdeveniment. Afegiu http:// si es tracta d'un enllaç extern."),
                            required=False)

    event_image = NamedBlobFile(title=_(u"Imatge de l'esdeveniment"),
                             description=_(u"Es recomana que sigui una imatge rectangular horitzontal."),
                             required=False)

    dexteritytextindexer.searchable('event_keywords')
    event_keywords = schema.Text(title=_(u"Paraules clau"),
                                 description=_(u'Introdueix les paraules clau separades per una coma i un espai, per exemple "Manresa, Bages, Acte"'),
                                 required=False)

    inscriptions_available = schema.Bool(title=_(u"Hi ha inscripcions?"),
                                         description=_(u""),
                                         required=False)

    start_inscription = schema.Datetime(title=_(u"Inici inscripció"),
                                        description=_(u""),
                                        required=False)

    end_inscription = schema.Datetime(title=_(u"Fi inscripció"),
                                      description=_(u""),
                                      required=False)

    form.write_permission(destacat="cmf.ReviewPortalContent")
    destacat = schema.Bool(title=_(u"Destacat?"),
                           description=_(u""),
                           required=False)

    form.read_permission(paper="cmf.ReviewPortalContent")
    form.write_permission(paper="cmf.ReviewPortalContent")
    paper = schema.Bool(title=_(u"Aquest acte va a paper?"),
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

    portals = schema.List(title=_(u"Portals"),
                          description=u"",
                          required=False,
                          value_type=schema.Choice(source=portals_vocabulary))

    searchable(IBasic, "title")
    searchable(IBasic, "description")


@form.default_value(field=IEsdeveniment['start_inscription'])
def start_inscriptionDefaultValue(data):
    return datetime.datetime.today()


@form.default_value(field=IEsdeveniment['end_inscription'])
def end_inscriptionDefaultValue(data):
    return datetime.datetime.today()


class EsdevenimentBaseView(object):

    def _get_strftime(self, time):
        accessor = EventAccessor(self.context)
        whole_day = accessor.whole_day
        format = '%d/%m/%Y %H:%M'
        if whole_day:
            format = '%d/%m/%Y'
        if time is not None:
            return time.strftime(format)
        else:
            return None

    def get_start_inscription(self):
        return self._get_strftime(self.context.start_inscription)

    def get_end_inscription(self):
        return self._get_strftime(self.context.end_inscription)

    def get_start(self):
        accessor = EventAccessor(self.context)
        if hasattr(accessor, 'start'):
            return accessor.start
        else:
            return None

    def get_end(self):
        accessor = EventAccessor(self.context)
        if hasattr(accessor, 'end'):
            return accessor.end
        else:
            return None

    def _get_terms(self, vocabulary, values):
        terms = [vocabulary.getTerm(a).title for a in values if a in vocabulary]
        return terms

    def get_etiquetes(self):
        vocabulary = etiquetes_vocabulary(self.context)
        return self._get_terms(vocabulary, self.context.etiquetes)

    def get_publics(self):
        vocabulary = publics_vocabulary(self.context)
        return self._get_terms(vocabulary, self.context.publics)

    def get_cicles(self):
        vocabulary = cicles_vocabulary(self.context)
        return self._get_terms(vocabulary, self.context.cicles)

    def get_descriptors(self):
        vocabulary = descriptors_vocabulary(self.context)
        return self._get_terms(vocabulary, self.context.descriptors)

    def get_portals(self):
        vocabulary = portals_vocabulary(self.context)
        return self._get_terms(vocabulary, self.context.portals)

    def get_text(self):
        behavior = IRichText(self.context, None)
        return getattr(behavior, 'text', None)

    def get_location(self):
        accessor = EventAccessor(self.context)
        if 'location' in accessor:
            return accessor.location
        return None

    # def get_html_dates(self):
    #     """ retorna l'html per pintar les dates de l'esdeveniment, tant si és
    #     recurrent com si no, per no haver de repetir la lógica a cada .pt
    #     """
    #     accessor = EventAccessor(self.context)
    #     html_dates = ""

    #     if accessor.recurrence:
    #         html_dates += "<span class='esdeveniment_recursiu'>" + _("Esdeveniment recursiu") + "</span>"
    #         html_dates += "<br/><span class='explicacio_recursivitat'>" + self.explain_recurrence() + "</span>"
    #         html_dates += " <span class='a_partir_de'>" + _("a partir de") + "</span> <span class='start_date'>" + self.get_start() + "</span>"
    #         # més ocurrències
    #         all_occurrences = self.all_occurrences()
    #         events = all_occurrences['events']
    #         html_dates += "<br/><span class='mes_ocurrencies'>" + _("Mes ocurrencies daquest esdeveniment:") + "</span>"
    #         html_dates += "<ul class='llistat_ocurrencies'>"
    #         for occ in events:
    #             html_dates += "<li>" + self.formatted_date(occ) + "</li>"
    #         tail = all_occurrences['tail']
    #         if tail:
    #             html_dates += "<li class='punts_suspensius'>...</li><li class='ultima_ocurrencia'>" + self.formatted_date(tail) + "</li>"
    #         html_dates += "</ul>"

    #     else:
    #         if accessor.open_end:
    #             html_dates = "<span class='a_partir_de'>" + _("A partir de") + "</span> <span class='start_date'>" + self.get_start() + "</span>"
    #         else:
    #             html_dates = "<span class='del'>" + _("Del") + "</span> <span class='start_date'>" + self.get_start() + "</span> <span class='al'>" + _("al") + "</span> <span class='end_date'>" + self.get_end() + "</span>"

    #     return html_dates

    def get_dades_event_accessor(self):
        dades = {}
        accessor = EventAccessor(self.context)
        dades['start'] = self.get_start()
        dades['end'] = self.get_end()
        dades['whole_day'] = accessor.whole_day
        dades['open_end'] = accessor.open_end
        dades['recurrence'] = accessor.recurrence
        dades['timezone'] = accessor.timezone
        dades['location'] = accessor.location
        dades['event_url'] = accessor.event_url
        dades['subjects'] = accessor.subjects
        dades['text'] = accessor.text
        return dades

    def all_occurrences(self):
        """ Returns all occurrences for this context
        The maximum defaults to 7 occurrences. If there are more occurrences
        defined for this context, the result will contain the last item
        of the occurrence list.

        :returns: Dictionary with ``events`` and ``tail`` as keys.
        :rtype: dict

        """
        occ_dict = dict(events=[], tail=None)
        context = self.context
        adapter = IRecurrenceSupport(context, None)
        if adapter is not None:
            occurrences = adapter.occurrences()
            occ_dict['events'], occ_dict['tail'] = (
                self._get_occurrences_helper(occurrences)
            )
        return occ_dict

    def _regles_recurrencia(self, recurrence):
        recurrence = recurrence.replace("RRULE:", "")
        parts = recurrence.split(';')
        regles = {}
        for part in parts:
            aux = part.split("=")
            regles[aux[0]] = aux[1]
        return regles

    def _process_until(self, string):
        """ given a string "20140131T000000", return "31/01/2014"
        """
        return string[4:6] + "/" + string[6:8] + "/" + string[0:4]

    def _traduccio_regla(self, regles):
        """ claus: FREQ, INTERVAL, COUNT, UNTIL, BYDAY, BYMONTH, BYMONTHDAY
        """

        strings_traduccio = [_("Es repeteix ")]

        if "INTERVAL" in regles:
            strings_traduccio.append(_(" cada ") + regles["INTERVAL"] + " " + freq_vocabulary.getTerm(regles["FREQ"]).title)

        if "BYDAY" in regles:
            if "+" in regles["BYDAY"]:
                ordinal = ordinal_numbers_vocabulary.getTerm(regles["BYDAY"][1:2]).title
                weekday = weekdays_vocabulary.getTerm(regles["BYDAY"][2:4]).title
                strings_traduccio.append(_(" el ") + ordinal + " " + weekday + _(" del mes"))
            elif "-" in regles["BYDAY"]:
                weekday = weekdays_vocabulary.getTerm(regles["BYDAY"][2:4]).title
                strings_traduccio.append(_(" lultim ") + weekday + _(" del mes"))
            else:
                weekdays = ", ".join([weekdays_vocabulary.getTerm(a).title for a in regles["BYDAY"].split(",")])
                # replaces last ", " with " i "
                weekdays = weekdays[::-1].replace(", "[::-1], " i "[::-1], 1)[::-1]
                strings_traduccio.append(" " + weekdays)

        elif "BYMONTH" in regles:
            if "BYMONTHDAY" in regles:
                strings_traduccio.append(_(" el ") + regles["BYMONTHDAY"] + _(" de ") + month_vocabulary.getTerm(regles["BYMONTH"]).title)

        elif "BYMONTHDAY" in regles:
            strings_traduccio.append(_(" el dia ") + regles["BYMONTHDAY"] + _(" del mes"))

        if "COUNT" in regles:
            strings_traduccio.append(_(", acaba despres de ") + regles["COUNT"] + _(" repeticions"))

        if "UNTIL" in regles:
            data = self._process_until(regles["UNTIL"])
            strings_traduccio.append(_(", acaba el ") + data)

        return "".join(strings_traduccio)

    # def explain_recurrence(self):
    #     """ Translates strings like "RRULE:FREQ=MONTHLY;INTERVAL=2;BYDAY=+3TU;COUNT=7" in a
    #     more understandable string like "Es repeteix cada 2 mesos el tercer dimarts del mes, acaba després de 7 repeticions".
    #     Examples:
    #         "RRULE:FREQ=DAILY;INTERVAL=2;COUNT=7"
    #             Es repeteix cada 2 dies, acaba després de 7 repeticions
    #         "RRULE:FREQ=DAILY;INTERVAL=2;UNTIL=20140131T000000"
    #             Es repeteix cada 2 dies, acaba el 01/31/2014
    #         "RRULE:FREQ=WEEKLY;BYDAY=MO,FR;COUNT=7"
    #             Es repeteix dilluns i divendres, acaba després de 7 repeticions
    #         "RRULE:FREQ=WEEKLY;BYDAY=MO,FR;UNTIL=20140131T000000"
    #             Es repeteix dilluns i divendres, acaba el 01/31/2014
    #         "RRULE:FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR;COUNT=7"
    #             Es repeteix dilluns, dimarts, dimecres, dijous i divendres, acaba després de 7 repeticions
    #         "RRULE:FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR;UNTIL=20140131T000000"
    #             Es repeteix dilluns, dimarts, dimecres, dijous i divendres, acaba el 01/31/2014
    #         "RRULE:FREQ=WEEKLY;INTERVAL=3;BYDAY=SU,WE;COUNT=7"
    #             Es repeteix cada 3 setmanes diumenge i dimecres, acaba després de 7 repeticions
    #         "RRULE:FREQ=WEEKLY;INTERVAL=3;BYDAY=SU,WE;UNTIL=20140121T000000"
    #             Es repeteix cada 3 setmanes diumenge i dimecres, acaba el 01/21/2014
    #         "RRULE:FREQ=MONTHLY;INTERVAL=2;BYMONTHDAY=21;COUNT=7"
    #             Es repeteix cada 2 mesos el dia 21 del mes, acaba després de 7 repeticions
    #         "RRULE:FREQ=MONTHLY;BYDAY=-1TU;COUNT=7"
    #             Es repeteix l'últim dimarts del mes, acaba després de 7 repeticions
    #         "RRULE:FREQ=MONTHLY;INTERVAL=2;BYDAY=+3TU;COUNT=7"
    #             Es repeteix cada 2 mesos el tercer dimarts del mes, acaba després de 7 repeticions
    #         "RRULE:FREQ=MONTHLY;INTERVAL=2;BYMONTHDAY=21;UNTIL=20150129T000000"
    #             Es repeteix cada 2 mesos el dia 21 del mes, acaba el 01/29/2015
    #         "RRULE:FREQ=YEARLY;INTERVAL=4;BYMONTH=1;BYMONTHDAY=21;COUNT=7"
    #             Es repeteix cada 4 anys el 21 de gener, acaba després de 7 repeticions
    #     """
    #     recurrence = self.get_dades_event_accessor()["recurrence"]
    #     regles = self._regles_recurrencia(recurrence)
    #     traduccio = self._traduccio_regla(regles)
    #     return traduccio

    def get_all_tags(self):
        return self.get_publics() + self.get_etiquetes() + self.get_cicles() + self.get_descriptors() + self.get_portals()

    def getEventImage(self):
        """ cridada quan l'esdeveniment no té imatge, si l'esdeveniment té
        assignades etiquetes busca una imatge relacionada amb la primera
        etiqueta a /tags/imatges-generiques/id+etiqueta; si no en té o no troba
        cap imatge relacionada amb l'etiqueta, busca una imatge a
        /tags/imatges-generiques
        """
        root = self.context.portal_url.getPortalObject()
        portal_catalog = root.portal_catalog
        portal_id = root.id

        etiquetes = self.context.etiquetes

        if etiquetes:
            etiqueta = portal_catalog({'UID': etiquetes[0]})[0].id
            folder_path = '/' + portal_id + '/tags/imatges-generiques/' + etiqueta
        else:
            folder_path = '/' + portal_id + '/tags/imatges-generiques'

        results = portal_catalog(path={'query': folder_path, 'depth': 1}, portal_type='Image')
        if results:
            n = random.randint(0, len(results) - 1)
            return results[n].getObject()
        else:
            folder_path = '/' + portal_id + '/tags/imatges-generiques'
            results = portal_catalog(path={'query': folder_path, 'depth': 1}, portal_type='Image')
            if results:
                n = random.randint(0, len(results) - 1)
                return results[n].getObject()
            else:
                return None


@indexer(IEsdeveniment)
def is_more_than_one_day_index(object, **kw):
    days = (object.end - object.start).days
    return str(days)


class View(grok.View, EventSummaryView, EsdevenimentBaseView):
    grok.context(IEsdeveniment)
    grok.require('zope2.View')


class faceted_preview_item(grok.View, EventSummaryView, EsdevenimentBaseView):
    grok.context(IEsdeveniment)
    grok.name('faceted-preview-item')
    grok.require('zope2.View')


class destacat_view(grok.View, EventSummaryView, EsdevenimentBaseView):
    grok.context(IEsdeveniment)
    grok.name('destacat_view')
    grok.require('zope2.View')
