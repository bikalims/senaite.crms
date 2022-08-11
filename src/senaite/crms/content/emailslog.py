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
        description=_('Person who sent the email'),
        required=False,
    )
    actor_fullname = schema.TextLine(
        title=_('Actor fullname'),
        description=_("Fullname of the Person who sent the email"),
        required=False,
    )
    email_send_date = schema.Datetime(
        title=_('Email send date'),
        description=_('Date email sent'),
        required=False,
    )
    email_recipients = schema.TextLine(
        title=_('Email recipients'),
        description=_('Emails receivers'),
        required=False,
    )
    email_responsibles = schema.TextLine(
        title=_('Email responsibles'),
        description=_('Emails receivers'),
        required=False,
    )
    email_subject = schema.TextLine(
        title=_('Email subject'),
        description=_('Emails subject'),
    )
    email_body = schema.TextLine(
        title=_('Email body'),
        description=_('Emails body'),
        required=False,
    )
    email_attachments = schema.TextLine(
        title=_('Email attachments'),
        description=_('Emails attachments'),
        required=False,
    )


@implementer(IEmailsLog, IHideActionsMenu)
class EmailsLog(Item):
    _catalogs = ['portal_catalog']
