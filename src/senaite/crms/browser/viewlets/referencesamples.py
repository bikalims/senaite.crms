# -*- coding: utf-8 -*-

from DateTime import DateTime
from plone.app.layout.viewlets import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from bika.lims import api
from bika.lims import senaiteMessageFactory as _


class ReferenceSampleAlerts(ViewletBase):
    """Viewlet for expired reference samples
    """
    index = ViewPageTemplateFile("templates/alerts.pt")

    title = _("Reference Samples Alerts")
    icon_name = "remarks"

    def __init__(self, context, request, view, manager=None):
        super(ReferenceSampleAlerts, self).__init__(
            context, request, view, manager=manager)
        self.nr_expired = 0
        self.failed = {
            "expired": [],
        }

    def get_expired_reference_samples(self):
        """Find expired reference sample

        - instruments who have failed QC tests

        Return a dictionary with all info about expired reference sample
        """
        setup = api.get_setup()
        warning_period = setup.WarningPeriod
        if not warning_period:
            return
        bsc = api.get_tool("senaite_catalog")
        date_from = DateTime()
        date_to = date_from + warning_period
        query = {"portal_type": "ReferenceSample", "is_active": True}
        query['getExpiryDate'] = {'query': (date_from, date_to),
                                  'range': 'min:max'}
        ref_samples = bsc(query)
        for i in ref_samples:
            i = i.getObject()
            ref_sample = {'uid': i.UID(), 'title': i.Title()}
            self.nr_expired += 1
            ref_sample['link'] = '<a href="%s">%s</a>' % (
                i.absolute_url(), i.Title()
            )
            self.failed['expired'].append(ref_sample)

    def available(self):
        return True

    def render(self):
        """Render the viewlet
        """
        if not self.available():
            return ""

        self.get_expired_reference_samples()

        if self.nr_expired:
            return self.index()
        else:
            return ""
