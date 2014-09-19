# -*- encoding:utf-8 -*-
""" Add esdeveniment widget
"""
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from eea.facetednavigation.widgets.widget import Widget as AbstractWidget
from eea.facetednavigation import EEAMessageFactory as _


class Widget(AbstractWidget):
    """ Widget
    """
    # Widget properties
    widget_type = 'add_esdeveniment'
    widget_label = _('Afegir esdeveniment widget')
    view_js = '++resource++eea.facetednavigation.widgets.portlet.view.js'
    view_css = '++resource++eea.facetednavigation.widgets.portlet.view.css'
    edit_css = '++resource++eea.facetednavigation.widgets.portlet.edit.css'

    index = ZopeTwoPageTemplateFile('widget.pt', globals())
    edit_schema = AbstractWidget.edit_schema.copy()
    edit_schema['title'].default = 'HTML'

    def usuari_registrat(self):
        return self.context.portal_membership.isAnonymousUser() == 0

    def get_register_url(self):
        return getToolByName(self.context, 'portal_url')() + '/register'

    def get_login_url(self):
        return getToolByName(self.context, 'portal_url')() + '/login?came_from=' + self.context.absolute_url()

    def get_add_esdeveiment_url(self):
        membership = getToolByName(self.context, 'portal_membership')
        member = membership.getAuthenticatedMember()
        portal_url = getToolByName(self.context, 'portal_url')()
        if membership.getHomeFolder(member.getId()):
            path = membership.getHomeFolder(member.getId()).absolute_url() + '/createObject?type_name=Event'
        else:
            path = portal_url + '/login?came_from=' + self.context.absolute_url()
        return path
