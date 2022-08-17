# -*- coding: utf-8 -*-

import os
from bika.lims import api
from bika.lims.utils import render_html_attributes


def get_local_image(name, **kwargs):
    """Returns a well-formed image
    :param name: file name of the image
    :param kwargs: additional attributes and values
    :return: a well-formed html img
    """
    if not name:
        return ""
    portal = api.get_portal()
    theme = portal.restrictedTraverse("@@senaite_theme")
    basename, ext = os.path.splitext(name)
    if basename in theme.icons():
        if "width" not in kwargs:
            kwargs["width"] = "16"
        return theme.icon_tag(basename, **kwargs)
    portal_url = api.get_url(portal)
    attr = render_html_attributes(**kwargs)
    html = '<img src="{}/++resource++senaite.crms.images/{}" {}/>'
    return html.format(portal_url, name, attr)
