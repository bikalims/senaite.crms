# -*- coding: utf-8 -*-

from DateTime import DateTime
from Products.Archetypes import atapi
from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender
from archetypes.schemaextender.interfaces import ISchemaExtender
from zope.component import adapts
from zope.interface import implementer

from .fields import ExtDateTimeField
from bika.lims import api
from bika.lims.interfaces import IReferenceSample
from senaite.crms import _
from senaite.crms.interfaces import ISenaiteCrmsLayer
from senaite.core.browser.widgets import DateTimeWidget


class AlertDateField(ExtDateTimeField, atapi.IntegerField):

    def getDefault(self, instance):
        setup = api.get_setup()
        expiring_warning = setup.Schema().getField('ExpiryWarning').get(setup)
        default_alert_date = DateTime() + expiring_warning
        return default_alert_date


alert_date_field = AlertDateField(
    "AlertDate",
    mode="rw",
    widget=DateTimeWidget(
        label=_(u"Alert Date"),
        description=_(u"Alert Date"),))


@implementer(ISchemaExtender, IBrowserLayerAwareExtender)
class ReferenceSampleSchemaExtender(object):
    adapts(IReferenceSample)
    layer = ISenaiteCrmsLayer

    fields = [
        alert_date_field,
    ]

    def __init__(self, context):
        self.context = context

    def getOrder(self, schematas):
        return schematas

    def getFields(self):
        return self.fields
