# -*- coding: utf-8 -*-

import collections
from datetime import datetime
from Products.ATContentTypes.utils import DT2dt
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from bika.lims import api
from bika.lims.utils import get_image
from bika.lims.utils import get_link
from bika.lims.utils import t
from bika.lims.utils import get_link_for
from bika.lims.browser.referencesample import ReferenceSamplesView as RSV
from bika.lims.browser.referencesample import ViewView as VV
from senaite.crms import _
from senaite.crms.utils import get_local_image


class ViewView(VV):
    """Reference Sample View
    """
    template = ViewPageTemplateFile("templates/referencesample_view.pt")


class ReferenceSamplesView(RSV):
    """Main reference samples folder view
    """

    def __init__(self, context, request):
        super(ReferenceSamplesView, self).__init__(context, request)

        self.catalog = "senaite_catalog"

        self.contentFilter = {
            "portal_type": "ReferenceSample",
            "sort_on": "sortable_title",
            "sort_order": "ascending",
            "path": {"query": ["/"], "level": 0},
        }

        self.context_actions = {}
        self.title = self.context.translate(_("Reference Samples"))
        self.icon = "{}/{}".format(
            self.portal_url,
            "++resource++bika.lims.images/referencesample_big.png")

        self.show_select_column = True
        self.pagesize = 25

        self.columns = collections.OrderedDict((
            ("ID", {
                "title": _("ID"),
                "index": "id"}),
            ("Title", {
                "title": _("Title"),
                "index": "sortable_title",
                "toggle": True}),
            ("Supplier", {
                "title": _("Supplier"),
                "toggle": True}),
            ("Manufacturer", {
                "title": _("Manufacturer"),
                "toggle": True}),
            ("Definition", {
                "title": _("Reference Definition"),
                "toggle": True}),
            ("DateSampled", {
                "title": _("Date Sampled"),
                "index": "getDateSampled",
                "toggle": True}),
            ("DateReceived", {
                "title": _("Date Received"),
                "index": "getDateReceived",
                "toggle": True}),
            ("DateOpened", {
                "title": _("Date Opened"),
                "toggle": True}),
            ("ExpiryDate", {
                "title": _("Expiry Date"),
                "index": "getExpiryDate",
                "toggle": True}),
            ("AlertDate", {
                "title": _("Alert Date"),
                "toggle": True}),
            ("state_title", {
                "title": _("State"),
                "toggle": True}),
        ))

        self.review_states = [
            {
                "id": "default",
                "title": _("Current"),
                "contentFilter": {"review_state": "current"},
                "columns": self.columns.keys(),
            }, {
                "id": "expired",
                "title": _("Expired"),
                "contentFilter": {"review_state": "expired"},
                "columns": self.columns.keys(),
            }, {
                "id": "disposed",
                "title": _("Disposed"),
                "contentFilter": {"review_state": "disposed"},
                "columns": self.columns.keys(),
            }, {
                "id": "all",
                "title": _("All"),
                "contentFilter": {},
                "columns": self.columns.keys(),
            }
        ]

    def folderitem(self, obj, item, index):
        """Applies new properties to the item (Client) that is currently being
        rendered as a row in the list

        :param obj: client to be rendered as a row in the list
        :param item: dict representation of the client, suitable for the list
        :param index: current position of the item within the list
        :type obj: ATContentType/DexterityContentType
        :type item: dict
        :type index: int
        :return: the dict representation of the item
        :rtype: dict
        """

        obj = api.get_object(obj)

        # XXX Refactor expiration to a proper place
        # ---------------------------- 8< -------------------------------------
        if item.get("review_state", "current") == "current":
            # Check expiry date
            exdate = obj.getExpiryDate()
            if exdate:
                expirydate = DT2dt(exdate).replace(tzinfo=None)
                if (datetime.today() > expirydate):
                    # Trigger expiration
                    self.workflow.doActionFor(obj, "expire")
                    item["review_state"] = "expired"
                    item["obj"] = obj

        if self.contentFilter.get('review_state', '') \
           and item.get('review_state', '') == 'expired':
            # This item must be omitted from the list
            return None
        # ---------------------------- >8 -------------------------------------

        url = api.get_url(obj)
        id = api.get_id(obj)
        alertdate = obj.getExpiryDate() - self.getExpiryWarning()

        item["ID"] = id
        item["replace"]["ID"] = get_link(url, value=id)
        item["DateSampled"] = self.ulocalized_time(
            obj.getDateSampled(), long_format=True)
        item["DateReceived"] = self.ulocalized_time(obj.getDateReceived())
        item["DateOpened"] = self.ulocalized_time(obj.getDateOpened())
        item["ExpiryDate"] = self.ulocalized_time(obj.getExpiryDate())
        item["AlertDate"] = self.ulocalized_time(alertdate)

        # Icons
        after_icons = ''
        alertdate = DT2dt(alertdate).replace(tzinfo=None)
        if (datetime.today() > alertdate):
            after_icons += get_local_image(
                "red alert icon 16x16.png", title=t(_("Alert Date")))
        if after_icons:
            item["after"]["AlertDate"] = after_icons

        manufacturer = obj.getManufacturer()
        item["replace"]["Manufacturer"] = get_link_for(manufacturer)

        supplier = api.get_parent(obj)
        item["replace"]["Supplier"] = get_link_for(supplier)

        ref_definition = obj.getReferenceDefinition()
        item["replace"]["Definition"] = get_link_for(ref_definition)

        # Icons
        after_icons = ''
        if obj.getBlank():
            after_icons += get_image(
                "blank.png", title=t(_("Blank")))
        if obj.getHazardous():
            after_icons += get_image(
                "hazardous.png", title=t(_("Hazardous")))
        if after_icons:
            item["after"]["ID"] = after_icons

        return item

    def getExpiryWarning(self):
        setup = api.get_setup()
        expiring_warning = setup.Schema().getField('ExpiryWarning').get(setup)
        if not expiring_warning:
            return 0
        return expiring_warning


class SupplierReferenceSamplesView(ReferenceSamplesView):
    """Supplier Reference Samples
    """

    def __init__(self, context, request):
        super(SupplierReferenceSamplesView, self).__init__(context, request)

        self.contentFilter["path"]["query"] = api.get_path(context)

        self.context_actions = {
            _("Add"): {
                "url": "createObject?type_name=ReferenceSample",
                "permission": "Add portal content",
                "icon": "++resource++bika.lims.images/add.png"}
        }

        # Remove the Supplier column from the list
        del self.columns["Supplier"]
        for rs in self.review_states:
            rs["columns"] = [col for col in rs["columns"] if col != "Supplier"]
