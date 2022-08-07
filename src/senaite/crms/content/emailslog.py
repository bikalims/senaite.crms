# -*- coding: utf-8 -*-

from senaite.crms import _
from senaite.core.interfaces import IHideActionsMenu

from plone.dexterity.content import Item
from plone.supermodel import model

from zope import schema
from zope.interface import implementer


class IEmailsLog(model.Schema):
    actor = schema.TextLine(
        title=_('Actor'),
        description=_('Actor who sent the email'),
    )
    actor_fullname = schema.TextLine(
        title=_('Actor fullname'),
        description=_("Actor's Fullname who sent the email"),
    )
    email_send_date = schema.Datetime(
        title=_('Email send date'),
        description=_('Date email sent'),
    )
    email_recipients = schema.TextLine(
        title=_('Email recipients'),
        description=_('Emails receivers'),
    )
    email_responsibles = schema.TextLine(
        title=_('Email responsibles'),
        description=_('Emails receivers'),
    )
    email_subject = schema.TextLine(
        title=_('Email subject'),
        description=_('Emails subject'),
    )
    email_body = schema.TextLine(
        title=_('Email body'),
        description=_('Emails body'),
    )
    email_attachments = schema.TextLine(
        title=_('Email attachments'),
        description=_('Emails attachments'),
    )


@implementer(IEmailsLog, IHideActionsMenu)
class EmailsLog(Item):
    _catalogs = ['portal_catalog']
