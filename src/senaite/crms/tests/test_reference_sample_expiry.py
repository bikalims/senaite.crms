from DateTime import DateTime
from bika.lims import api
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from senaite.core.browser.viewlets.referencesamples import EXPIRY_CHECKED
from senaite.core.tests.base import BaseTestCase
from senaite.crms.browser.overrides.referencesamples import ReferenceSamplesView
from senaite.crms.browser.viewlets.referencesamples import ReferenceSampleAlerts


class TestReferenceSampleExpiry(BaseTestCase):

    def setUp(self):
        super(TestReferenceSampleExpiry, self).setUp()
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.request.other.pop(EXPIRY_CHECKED, None)
        supplier = api.create(self.portal.setup.suppliers, "Supplier",
                              Name="Supplier")
        self.sample = api.create(supplier, "ReferenceSample", title="Past",
                                 ExpiryDate=DateTime() - 1)

    def test_alert_viewlet_update_expires_overdue_samples(self):
        viewlet = ReferenceSampleAlerts(self.portal, self.request, None)
        viewlet.update()
        self.assertEqual(api.get_workflow_status_of(self.sample), "expired")

    def test_crm_listing_displays_expired_sample_and_red_icon(self):
        ReferenceSampleAlerts(self.portal, self.request, None).update()
        self.request.form["list_review_state"] = "expired"
        view = ReferenceSamplesView(
            self.portal.bika_setup.referencesamples, self.request)
        view.workflow = api.get_tool("portal_workflow")
        view.portal = self.portal
        view.mtool = api.get_tool("portal_membership")
        view.member = api.get_current_user()
        # This test needs no CRM schema extender or email configuration.
        view.getExpiryWarning = lambda: 0
        items = view.get_folderitems()
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["state_title"], "Expired")
        self.assertIn("text-danger", items[0]["after"]["ExpiryDate"])

    def test_alert_viewlet_update_does_not_expire_as_ordinary_member(self):
        setRoles(self.portal, TEST_USER_ID, ["Member"])
        ReferenceSampleAlerts(self.portal, self.request, None).update()
        self.assertEqual(api.get_workflow_status_of(self.sample), "current")
