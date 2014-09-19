""" Viewselector widget
"""
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile

from eea.facetednavigation.widgets.widget import Widget as AbstractWidget
from eea.facetednavigation import EEAMessageFactory as _


class Widget(AbstractWidget):
    """ Widget
    """
    # Widget properties
    widget_type = 'viewselector'
    widget_label = _('View selector widget')
    view_js = '++resource++eea.facetednavigation.widgets.portlet.view.js'
    view_css = '++resource++eea.facetednavigation.widgets.portlet.view.css'
    edit_css = '++resource++eea.facetednavigation.widgets.portlet.edit.css'

    index = ZopeTwoPageTemplateFile('widget.pt', globals())
    edit_schema = AbstractWidget.edit_schema.copy()  # + EditSchema
    edit_schema['title'].default = 'View selector widget'
