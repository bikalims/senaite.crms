# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from zope.publisher.interfaces.browser import IDefaultBrowserLayer

from bika.reports.interfaces import IBikaReportsLayer


class ISenaiteCRMSLayer(IBikaReportsLayer):
    """Marker interface that defines a Zope 3 browser layer.
    """

class ISenaiteCrmsLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""
