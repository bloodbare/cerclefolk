# -*- encoding:utf-8 -*-
""" Add esdeveniment widget
"""
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from eea.facetednavigation.widgets.widget import Widget as AbstractWidget
from eea.facetednavigation import EEAMessageFactory as _
import datetime


class Widget(AbstractWidget):
    """ Widget
    """
    # Widget properties
    widget_type = 'esdeveniment_destacat'
    widget_label = _('Widget esdeveniment destacat')
    view_js = '++resource++eea.facetednavigation.widgets.portlet.view.js'
    view_css = '++resource++eea.facetednavigation.widgets.portlet.view.css'
    edit_css = '++resource++eea.facetednavigation.widgets.portlet.edit.css'

    index = ZopeTwoPageTemplateFile('widget.pt', globals())
    edit_schema = AbstractWidget.edit_schema.copy()
    edit_schema['title'].default = 'Esdeveniment destacat'

    def get_esdeveniment_destacat(self):
        pc = getToolByName(self.context, 'portal_catalog')
        esdeveniments_destacats = pc(portal_type="esdeveniment",
                                     destacat=True,
                                     sort_on="start",
                                     start={'query': (datetime.datetime.now()),
                                            'range': 'min'})
        if esdeveniments_destacats:
            return esdeveniments_destacats[0].getObject()
        return None
