# -*- coding: utf-8 -*-

from Products.CMFCore.utils import getToolByName
from bika.reports.browser.reports.administration_arsnotinvoiced import Report as RA
from bika.lims.utils import t
from bika.lims.utils import formatDateQuery, formatDateParms
from senaite.crms import _


class Report(RA):

    def __call__(self):
        bc = getToolByName(self.context, 'senaite_catalog')
        self.report_content = {}
        parms = []
        headings = {}
        headings['header'] = _("Expiring Reference Samples")
        headings['subheader'] = _(
            "Expiring Reference Samples")

        count_all = 0

        query = {'portal_type': 'ReferenceSample',
                 'is_active': True,
                 'sort_order': 'reverse'}

        date_query = formatDateQuery(self.context, 'ExpiryDate')
        if date_query:
            query['getExpiryDate'] = date_query
            pubished = formatDateParms(self.context, 'ExpiryDate')
        else:
            pubished = 'Undefined'
        parms.append(
            {'title': _('Expiry Date'),
             'value': pubished,
             'type': 'text'})

        # and now lets do the actual report lines
        formats = {'columns': 4,
                   'col_heads': [_('Expiry Date'),
                                 _('Sample ID'),
                                 _('Title'),
                                 _('Reference Definition'),
                                 ],
                   'class': '',
                   }

        datalines = []

        for brain in bc(query):
            obj = brain.getObject()

            dataline = []

            dataitem = {'value': self.ulocalized_time(obj.getExpiryDate())}
            dataline.append(dataitem)

            dataitem = {'value': brain.id}
            dataline.append(dataitem)

            dataitem = {'value': brain.Title}
            dataline.append(dataitem)

            dataitem = {'value': obj.getReferenceDefinition().Title()}
            dataline.append(dataitem)

            datalines.append(dataline)

            count_all += 1

        # table footer data
        footlines = []
        footline = []
        footitem = {'value': _('Number of Reference Samples expiring in this period'),
                    'colspan': 3,
                    'class': 'total_label'}
        footline.append(footitem)
        footitem = {'value': count_all}
        footline.append(footitem)
        footlines.append(footline)

        self.report_content = {
            'headings': headings,
            'parms': parms,
            'formats': formats,
            'datalines': datalines,
            'footings': footlines}

        return {'report_title': t(headings['header']),
                'report_data': self.template()}
