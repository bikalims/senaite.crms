# -*- coding: utf-8 -*-

from Products.Archetypes.Widget import IntegerWidget
from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender
from archetypes.schemaextender.interfaces import ISchemaExtender
from zope.component import adapts
from zope.interface import implementer

from .fields import ExtIntegerField
from bika.lims.interfaces import IBikaSetup
from senaite.crms import _
from senaite.crms.interfaces import ISenaiteCrmsLayer

expiry_warning_field = ExtIntegerField(
    "ExpiryWarning",
    mode="rw",
    default=0,
    schemata="Sampling",
    widget=IntegerWidget(
        label=_(u"Reference Sample Expiry Warning"),
        description=_(u"Number of days before expiry an alert will be raised"),
        ))


@implementer(ISchemaExtender, IBrowserLayerAwareExtender)
class BikaSetupSchemaExtender(object):
    adapts(IBikaSetup)
    layer = ISenaiteCrmsLayer

    fields = [
        expiry_warning_field,
    ]

    def __init__(self, context):
        self.context = context

    def getOrder(self, schematas):
        return schematas

    def getFields(self):
        return self.fields
