# -*- encoding: utf-8 -*-
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase
from Products.CMFCore.utils import getToolByName
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from Products.CMFCore.utils import getToolByName


class AlertViewlet(ViewletBase):
    index = ViewPageTemplateFile('viewlet_templates/alert.pt')

    def message(self):
        registry = getUtility(IRegistry)

        missatge = registry.records['cerclefolk.alert'].value
        if missatge != '':
            return missatge
        else:
            return None


class AddEventViewlet(ViewletBase):
    index = ViewPageTemplateFile('viewlet_templates/add_event.pt')

    def is_authenticated(self):
        return self.context.portal_membership.isAnonymousUser() == 0

    def linkAddEvent(self):
        authenticated = self.is_authenticated()
        portal_url = getToolByName(self.context, 'portal_url')()

        if authenticated:
            membership = getToolByName(self.context, 'portal_membership')
            member = membership.getAuthenticatedMember()
            if membership.getHomeFolder(member.getId()):
                url = membership.getHomeFolder(member.getId()).absolute_url() + '/++add++Event'
            return {'url': url, 'text': 'Afegir esdeveniment'}
        else:
            return None
