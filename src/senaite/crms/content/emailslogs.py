# -*- coding: utf-8 -*-

from senaite.core.interfaces import IHideActionsMenu
from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implementer


class IEmailsLogs(model.Schema):
    pass


@implementer(IEmailsLogs, IHideActionsMenu)
class EmailsLogs(Container):
    _catalogs = ['portal_catalog']
