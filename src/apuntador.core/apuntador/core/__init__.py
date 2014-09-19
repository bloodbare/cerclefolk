# -*- coding: utf-8 -*-
from zope.i18nmessageid import MessageFactory

_ = MessageFactory('apuntador.core')

import plone
from behaviors import data_postprocessing as new_data_postprocessing

# plone.app.event.dx.behaviors.data_postprocessing = new_data_postprocessing

def initialize(context):
    """Initializer called when used as a Zope 2 product."""


import binascii
import re
import six
import sys
import types
import string
import zope.interface
import zope.contenttype
import zope.schema

from z3c.form import interfaces
from z3c.form.i18n import MessageFactory as _


def changed2Field(field, value, context=None):
    """Figure if a field's value changed

    Comparing the value of the context attribute and the given value"""
    if context is None:
        context = field.context
    if context is None:
        # IObjectWidget madness
        return True
    if zope.schema.interfaces.IObject.providedBy(field):
        return True

    # Get the datamanager and get the original value
    dm = zope.component.getMultiAdapter(
        (context, field), interfaces.IDataManager)
    # now figure value chaged status
    # Or we can not get the original value, in which case we can not check
    # Or it is an Object, in case we'll never know
    import datetime
    if isinstance(value, datetime.datetime):
        if (not dm.canAccess() or (dm.query() and (dm.query() is interfaces.NOVALUE or dm.query().replace(tzinfo=None) != value.replace(tzinfo=None)))):
            return True
        else:
            return False
    if (not dm.canAccess() or dm.query() != value):
        return True
    else:
        return False

from z3c.form import util

util.changedField = changed2Field
