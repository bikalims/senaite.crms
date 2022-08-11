# -*- coding: utf-8 -*-

import collections

from bika.lims import api
from bika.lims.utils import get_link
from senaite.app.listing import ListingView
from senaite.core.catalog import SETUP_CATALOG
from senaite.samplepointlocations.permissions import AddSamplePointLocation
from senaite.samplepointlocations import _


class EmailsLogsView(ListingView):
    def __init__(self, context, request):
        super(EmailsLogsView, self).__init__(context, request)
        self.catalog = 'portal_catalog'
        path = api.get_path(self.context)
        self.contentFilter = dict(
            portal_type="EmailsLog", sort_on="created"
        )
        self.form_id = "emailslogs"

        self.icon = "{}/{}/{}".format(
            self.portal_url, "/++resource++bika.lims.images", "sampletype_big.png"
        )

        self.title = "Emails Logs"
        self.description = self.context.Description()
        self.show_select_column = True

        self.columns = collections.OrderedDict(
            (
                ("id", dict(title=_("ID"), index="getId")),
                ("ActorFullname", dict(title=_("Actor Fullname"))),
                ("EmailSendDate", dict(title=_("Email Send Date"))),
            )
        )

        self.review_states = [
            {
                "id": "default",
                "title": _("Active"),
                "contentFilter": {"is_active": True},
                "transitions": [
                    {"id": "deactivate"},
                ],
                "columns": self.columns.keys(),
            },
            {
                "id": "inactive",
                "title": _("Inactive"),
                "contentFilter": {"is_active": False},
                "transitions": [
                    {"id": "activate"},
                ],
                "columns": self.columns.keys(),
            },
            {
                "id": "all",
                "title": _("All"),
                "contentFilter": {},
                "columns": self.columns.keys(),
            },
        ]

    def folderitem(self, obj, item, index):
        obj = api.get_object(obj)
        item["replace"]["EmailSendDate"] = get_link(
            href=api.get_url(obj), value=obj.getId()
        )
        return item
