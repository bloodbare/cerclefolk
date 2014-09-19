# -*- encoding: utf-8 -*-

from plone.directives import form
from five import grok
from plone.app.dexterity.behaviors.metadata import IBasic
from collective.dexteritytextindexer.utils import searchable


class IDescriptor(form.Schema):

    searchable(IBasic, 'title')
    searchable(IBasic, 'description')


class View(grok.View):

    grok.context(IDescriptor)
    grok.require('zope2.View')
