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

        missatge = registry.records['apuntador.alert'].value
        if missatge != '':
            return missatge
        else:
            return None


class FooterViewlet(ViewletBase):
    index = ViewPageTemplateFile('viewlet_templates/footer.pt')

    def linksDocuments(self):
        root = self.context.portal_url.getPortalObject()
        portal_catalog = root.portal_catalog
        portal_id = root.id

        folder_path = '/' + portal_id + '/links-footer'
        results = portal_catalog(path={'query': folder_path, 'depth': 1}, portal_type='Document')
        if results:
            return [{'title': a.Title, 'url': a.getURL()} for a in results]
        return


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
                url = membership.getHomeFolder(member.getId()).absolute_url() + '/++add++esdeveniment'
            return {'url': url, 'text': 'Afegir esdeveniment'}
        else:
            return {'url': portal_url + '/login', 'text': "Identifica't per afegir un esdeveniment"}
