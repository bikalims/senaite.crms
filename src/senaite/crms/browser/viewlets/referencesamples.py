# -*- coding: utf-8 -*-

from string import Template
from DateTime import DateTime
from plone.app.layout.viewlets import ViewletBase
from Products.CMFPlone.utils import safe_unicode
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from bika.lims import api
from bika.lims.api import mail as mailapi
from bika.lims.api.security import get_user
from bika.lims.api.security import get_user_id
from bika.lims.interfaces import IReferenceSample
from bika.lims.interfaces import IReferenceSamplesFolder

from senaite.crms import _


class ReferenceSampleAlerts(ViewletBase):
    """Viewlet for expired reference samples
    """
    index = ViewPageTemplateFile("templates/alerts.pt")
    email_template = ViewPageTemplateFile("templates/email_template.pt")

    title = _("Reference Samples Alerts")
    icon_name = "remarks"

    def __init__(self, context, request, view, manager=None):
        super(ReferenceSampleAlerts, self).__init__(
            context, request, view, manager=manager)
        self.nr_expired = 0
        self.recipients = []
        self.expiring_date = DateTime().Date()
        self.failed = {
            "expired": [],
        }

    @property
    def managers(self):
        departments = api.get_setup().bika_departments.values()
        out = []
        for i, dept in enumerate(departments):
            manager = dept.getManager()
            if not manager:
                continue
            if manager in out:
                continue
            out.append(manager)
        return out

    # Email sending taken from
    # senaite.core/src/bika/lims/browser/publish/emailview.py

    @property
    def email_subject(self):
        """Email subject line to be used in the template
        """
        # request parameter has precedence
        subject = self.request.get("subject", None)
        if subject is not None:
            return subject
        subject = self.context.translate(_("{} Reference Sample(s) will expire on {}"))
        return subject.format(self.nr_expired, self.expiring_date)

    @property
    def email_recipients_and_responsibles(self):
        """Returns a unified list of recipients and responsibles
        """
        return list(set(self.email_recipients))

    @property
    def email_recipients(self):
        """Email addresses of the selected recipients
        """
        managers = self.get_recipients_data(self.managers)
        email_addereses = [i.get('address', '') for i in managers]
        return map(safe_unicode, email_addereses)

    def get_recipients_data(self, managers):
        """Recipients data to be used in the template
        """
        if not managers:
            return []

        recipients = []

        for num, manager in enumerate(managers):
            name = manager.getFullname()
            email = manager.getEmailAddress()
            if not email or not name:
                continue
            address = mailapi.to_email_address(email, name=name)
            record = {
                "name": name,
                "email": email,
                "address": address,
                "valid": True,
            }
            if record not in recipients:
                recipients.append(record)
        return recipients

    def render_email_template(self, template):
        """Return the rendered email template

        This method interpolates the $recipients variable with the selected
        recipients from the email form.

        :params template: Email body text
        :returns: Rendered email template
        """

        recipients = self.email_recipients_and_responsibles
        template_context = {
            "recipients": "\n".join(recipients)
        }

        email_template = Template(safe_unicode(template)).safe_substitute(
            **template_context)

        return email_template

    def email_action_send(self, **kw):
        """Send form handler
        """
        # send email to the selected recipients and responsibles
        recipients = self.email_recipients_and_responsibles
        if not recipients:
            message = _("""
            The manager does not have an email address set.
            Therefore could not send email for expiring Reference Sample """)
            self.add_status_message(message, "error")
            return

        subject = self.email_subject
        body = self.context.translate(_(self.email_template(self)))
        success = self.send_email(recipients, subject, body, [], **kw)

        if success:
            # write email sendlog log to keep track of the email submission
            self.write_sendlog()
            message = _(u"Message sent to {}".format(
                ", ".join(self.email_recipients_and_responsibles)))
            self.add_status_message(message, "info")
        else:
            message = _("Failed to send Email(s)")
            self.add_status_message(message, "error")

    def write_sendlog(self):
        """Create emails log
        """
        timestamp = DateTime()
        parent = api.get_setup().emails_logs
        new_record = self.make_sendlog_record(email_send_date=timestamp)
        api.create(parent, portal_type="EmailsLog", **new_record)

    def make_sendlog_record(self, **kw):
        """Create a new sendlog record
        """
        user = get_user()
        actor = get_user_id()
        userprops = api.get_user_properties(user)
        actor_fullname = userprops.get("fullname", actor)
        email_send_date = DateTime()
        email_recipients = self.email_recipients_and_responsibles
        email_subject = self.email_subject

        record = {
            "title": self.expiring_date,
            "actor": actor,
            "actor_fullname": actor_fullname,
            "email_send_date": email_send_date,
            "email_recipients": email_recipients,
            "email_subject": email_subject,

        }
        # keywords take precedence
        record.update(kw)
        return record

    def add_status_message(self, message, level="info"):
        """Set a portal status message
        """
        return self.context.plone_utils.addPortalMessage(message, level)

    def send_email(self, recipients, subject, body, attachments=None, **kw):
        """Prepare and send email to the recipients

        :param recipients: a list of email or name,email strings
        :param subject: the email subject
        :param body: the email body
        :param attachments: list of email attachments
        :returns: True if all emails were sent, else False
        """
        email_body = self.render_email_template(body)

        success = []
        # Send one email per recipient
        for recipient in recipients:
            # N.B. we use just the email here to prevent this Postfix Error:
            # Recipient address rejected: User unknown in local recipient table
            pair = mailapi.parse_email_address(recipient)
            to_address = pair[1]
            mime_msg = mailapi.compose_email(self.email_sender_address,
                                             to_address,
                                             subject,
                                             email_body,
                                             attachments=attachments,
                                             **kw)
            sent = mailapi.send_email(mime_msg)
            if not sent:
                msg = _("Could not send email to {0} ({1})").format(pair[0],
                                                                    pair[1])
                self.add_status_message(msg, "warning")
            success.append(sent)

        if not all(success):
            return False
        return True

    @property
    def email_sender_address(self):
        """Sender email is either the lab email or portal email "from" address
        """
        lab = api.get_setup().laboratory
        lab_email = lab.getEmailAddress()
        portal_email = api.get_registry_record("plone.email_from_address")
        return lab_email or portal_email or ""

    def get_expired_reference_samples(self):
        """Find expired reference sample

        - instruments who have failed QC tests

        Return a dictionary with all info about expired reference sample
        """
        setup = api.get_setup()
        expiring_warning = setup.Schema().getField('ExpiryWarning').get(setup)
        if not expiring_warning:
            return
        bsc = api.get_tool("senaite_catalog")
        date_from = DateTime()
        date_to = date_from + expiring_warning
        self.expiring_date = date_to.Date()
        query = {"portal_type": "ReferenceSample", "is_active": True}
        query['getExpiryDate'] = {'query': (date_from, date_to),
                                  'range': 'min:max'}
        ref_samples = bsc(query)[0:6]
        for ref_index, i in enumerate(ref_samples):
            i = i.getObject()
            ref_sample = {'uid': i.UID(), 'title': i.Title()}
            self.nr_expired += 1
            ref_sample['link'] = '<a href="%s">%s</a>' % (
                i.absolute_url(), i.Title()
            )
            self.failed['expired'].append(ref_sample)

    def emailslogs(self):
        # has email been sent today
        query = {"portal_type": "EmailsLog"}
        query["created"] = {"query": DateTime().Date(), "range": "min"}
        bsc = api.get_tool("portal_catalog")
        return bsc(query)

    def available(self):
        kw = {"html": True}
        self.email_action_send(**kw)
        if self.nr_expired:
            return True
        return False

    def render(self):
        """Render the viewlet
        """
        self.get_expired_reference_samples()

        if not self.available():
            return ""

        if not self.emailslogs():
            kw = {"html": True}
            self.email_action_send(**kw)
        is_reference_sample = IReferenceSample.providedBy(self.context)
        is_reference_sample_folder = IReferenceSamplesFolder.providedBy(self.context)
        if is_reference_sample or is_reference_sample_folder:
            return self.index()
        return ""
