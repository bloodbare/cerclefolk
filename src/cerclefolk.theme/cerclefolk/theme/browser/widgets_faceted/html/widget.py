""" Text widget
"""
from Products.Archetypes.public import Schema
from Products.Archetypes.public import StringField
from Products.Archetypes.public import StringWidget
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile

from eea.facetednavigation.widgets.widget import Widget as AbstractWidget
from eea.facetednavigation import EEAMessageFactory as _


EditSchema = Schema((
    StringField('html',
        schemata="default",
        required=True,
        widget=StringWidget(
            label=_(u'HTML'),
            description=_(u''),
            i18n_domain="apuntador.theme"
        )
    ),
))

class Widget(AbstractWidget):
    """ Widget
    """
    # Widget properties
    widget_type = 'html'
    widget_label = _('HTML')
    view_js = '++resource++eea.facetednavigation.widgets.portlet.view.js'
    view_css = '++resource++eea.facetednavigation.widgets.portlet.view.css'
    edit_css = '++resource++eea.facetednavigation.widgets.portlet.edit.css'

    index = ZopeTwoPageTemplateFile('widget.pt', globals())
    edit_schema = AbstractWidget.edit_schema.copy() + EditSchema
    edit_schema['title'].default = 'HTML'

    @property
    def html(self):
        """ Get html
        """
        return self.data.get('html', '')
