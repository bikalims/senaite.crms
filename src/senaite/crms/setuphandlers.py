# -*- coding: utf-8 -*-
from bika.lims import api
from senaite.crms import logger
from senaite.crms import PROFILE_ID, PRODUCT_NAME
from senaite.core.setuphandlers import add_dexterity_items
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer


# An array of dicts. Each dict represents an ID formatting configuration
ID_FORMATTING = [
    {
        "portal_type": "EmailsLog",
        "form": "EML{seq:06d}",
        # "prefix": "location",
        "sequence_type": "generated",
        "counter_type": "",
        "split_length": 1,
    }
]


@implementer(INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return [
            'senaite.crms:uninstall',
        ]


def post_install(context):
    """Post install script"""
    # Do something at the end of the installation of this package.
    # if context.readDataFile("senaite.core.txt") is None:
    #     return

    logger.info("SENAITE CRMS install handler [BEGIN]")
    context = context._getImportContext(PROFILE_ID)
    portal = context.getSite()

    add_dexterity_setup_items(portal)


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.


def setup_handler(context):
    """Generic setup handler"""
    if context.readDataFile("{}.txt".format(PRODUCT_NAME)) is None:
        return

    logger.info("{} setup handler [BEGIN]".format(PRODUCT_NAME.upper()))
    portal = context.getSite()

    # Apply ID format to content types
    setup_id_formatting(portal)

    logger.info("{} setup handler [DONE]".format(PRODUCT_NAME.upper()))


def add_dexterity_setup_items(portal):
    """Adds the Dexterity Container in the Setup Folder

    N.B.: We do this in code, because adding this as Generic Setup Profile in
          `profiles/default/structure` flushes the contents on every import.
    """
    # Tuples of ID, Title, FTI
    items = [
        ("emails_logs",  # ID
         "Emails Logs",  # Title
         "EmailsLogs"),  # FTI
    ]
    setup = api.get_setup()
    add_dexterity_items(setup, items)


def setup_id_formatting(portal, format_definition=None):
    """Setup default ID formatting"""
    if not format_definition:
        logger.info("Setting up ID formatting ...")
        for formatting in ID_FORMATTING:
            setup_id_formatting(portal, format_definition=formatting)
        logger.info("Setting up ID formatting [DONE]")
        return

    bs = portal.bika_setup
    p_type = format_definition.get("portal_type", None)
    if not p_type:
        return

    form = format_definition.get("form", "")
    if not form:
        logger.info("Param 'form' for portal type {} not set [SKIP")
        return

    logger.info("Applying format '{}' for {}".format(form, p_type))
    ids = list()
    for record in bs.getIDFormatting():
        if record.get("portal_type", "") == p_type:
            continue
        ids.append(record)
    ids.append(format_definition)
    bs.setIDFormatting(ids)
