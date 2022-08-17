# -*- coding: utf-8 -*-

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from bika.lims.browser.reports import AdministrationView as AV


class AdministrationView(AV):
    """ Administration View form
    """
    template = ViewPageTemplateFile("templates/administration.pt")
