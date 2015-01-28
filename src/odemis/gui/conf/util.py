# -*- coding: utf-8 -*-

"""
:author: Rinze de Laat <laat@delmic.com>
:copyright: © 2013 Rinze de Laat, Delmic

This file is part of Odemis.

.. license::
    Odemis is free software: you can redistribute it and/or modify it under the terms  of the GNU
    General Public License version 2 as published by the Free Software  Foundation.

    Odemis is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;  without
    even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR  PURPOSE. See the GNU
    General Public License for more details.

    You should have received a copy of the GNU General Public License along with Odemis. If not,
    see http://www.gnu.org/licenses/.

Module purpose
--------------

This module contains functions that help in the generation of dynamic configuration values.

"""

from __future__ import division

import logging
import math

from odemis import model
import odemis.gui
from odemis.model import NotApplicableError


def resolution_from_range(comp, va, conf, init=None):
    """ Construct a list of resolutions depending on range values

    init (set or None): values that will be always in the choices. If None, it will just ensure that
        the current value is present.

    """

    cur_val = va.value

    if len(cur_val) != 2:
        logging.warning("Got a resolution not of length 2: %s", cur_val)
        return [cur_val]

    try:
        if init is None:
            choices = {cur_val}
        else:
            choices = init
        num_pixels = cur_val[0] * cur_val[1]
        res = va.range[1]  # start with max resolution

        for _ in range(10):
            choices.add(res)
            res = (res[0] // 2, res[1] // 2)

            if len(choices) >= 4 and (res[0] * res[1] < num_pixels):
                break

        return sorted(choices)  # return a list, to be sure it's in order
    except NotApplicableError:
        return [cur_val]


def resolution_from_range_plus_point(comp, va, conf):
    """ Same as _resolution_from_range() but also add a 1x1 value """
    return resolution_from_range(comp, va, conf, init={va.value, (1, 1)})


def binning_1d_from_2d(comp, va, conf):
    """ Find simple binnings available in one dimension

    We assume pixels are always square. The binning provided by a camera is normally a 2-tuple of
    integers.

    """

    cur_val = va.value
    if len(cur_val) != 2:
        logging.warning("Got a binning not of length 2: %s, will try anyway",
                        cur_val)

    try:
        choices = set([cur_val[0]])
        minbin = max(va.range[0])
        maxbin = min(va.range[1])

        # add up to 5 binnings
        b = int(math.ceil(minbin))  # in most cases, that's 1
        for _ in range(6):
            if minbin <= b <= maxbin:
                choices.add(b)

            if len(choices) >= 5 and b >= cur_val[0]:
                break

            b *= 2
            # logging.error(choices)

        return sorted(choices)  # return a list, to be sure it's in order
    except NotApplicableError:
        return [cur_val[0]]


def binning_firstd_only(comp, va, conf):
    """ Find simple binnings available in the first dimension

    The second dimension stays at a fixed size.

    """

    cur_val = va.value[0]

    try:
        choices = set([cur_val])
        minbin = va.range[0][0]
        maxbin = va.range[1][0]

        # add up to 5 binnings
        b = int(math.ceil(minbin))  # in most cases, that's 1
        for _ in range(6):
            if minbin <= b <= maxbin:
                choices.add(b)

            if len(choices) >= 5 and b >= cur_val:
                break

            b *= 2

        return sorted(choices)  # return a list, to be sure it's in order
    except NotApplicableError:
        return [cur_val]


def hfw_choices(comp, va, conf):
    """ Return a list of HFW choices

    If the VA has predefined choices, return those. Otherwise calculate the choices using the range
    of the VA.

    """

    try:
        choices = va.choices
    except NotApplicableError:
        mi, ma, = va.range
        choices = [mi]
        step = 1
        while choices[-1] < ma:
            choices.append(mi * 10 ** step)
            step += 1

    return choices


def mag_if_no_hfw_ctype(comp, va, conf):
    """ Return the control type for ebeam magnification

    This control is only useful if horizontalFoV is available.

    :return: (int) The control type

    """

    if (hasattr(comp, "horizontalFoV") and isinstance(comp.horizontalFoV,
                                                      model.VigilantAttributeBase)):
        return odemis.gui.CONTROL_NONE
    else:
        # Just use a text field => it's for copy-paste
        return odemis.gui.CONTROL_FLT
