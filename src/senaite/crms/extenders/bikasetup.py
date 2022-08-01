# -*- coding: utf-8 -*-

from Products.Archetypes.Widget import IntegerWidget
from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender
from archetypes.schemaextender.interfaces import ISchemaExtender
from zope.component import adapts
from zope.interface import implementer

from .fields import ExtIntegerField
from bika.lims.interfaces import IBikaSetup
from senaite.batch.invoices import _
from senaite.crms.interfaces import ISenaiteCrmsLayer

warning_period_field = ExtIntegerField(
    "WarningPeriod",
    mode="rw",
    schemata="Sampling",
    widget=IntegerWidget(
        label=_(u"Warning Period"),
        description=_(u"How long before Reference Samples expiry"),
        ))


@implementer(ISchemaExtender, IBrowserLayerAwareExtender)
class BikaSetupSchemaExtender(object):
    adapts(IBikaSetup)
    layer = ISenaiteCrmsLayer

    fields = [
        warning_period_field,
    ]

    def __init__(self, context):
        self.context = context

    def getOrder(self, schematas):
        return schematas

    def getFields(self):
        return self.fields
