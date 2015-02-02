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

"""
from collections import OrderedDict

import wx

import odemis.gui
import odemis.gui.conf.util as util

# All values in CONFIG are optional
#
# We only need to define configurations for VAs that a not automatically
# displayed correctly. To force the order, some VAs are just named, without
# specifying configuration.
#
# Format:
#   role of component
#       vigilant attribute name
#           label
#           tooltip
#           control_type * (CONTROL_NONE to hide it)
#           range *
#           choices *
#           scale
#           type
#           format
#           accuracy
#           event (The wx.Event type that will trigger a value update)
#
# The configurations with a * can be replaced with a function, to allow for
# dynamic values which can be depending on the backend configuration.

# This is the default global settings, with ordered dict, to specify the order
# on which they are displayed.
HW_SETTINGS_CONFIG = {
    "ccd":
        OrderedDict((
            ("exposureTime", {
                "control_type": odemis.gui.CONTROL_SLIDER,
                "scale": "log",
                "range": (0.001, 60.0),
                "type": "float",
                "accuracy": 2,
            }),
            ("binning", {
                "control_type": odemis.gui.CONTROL_RADIO,
                "choices": util.binning_1d_from_2d,
            }),
            ("resolution", {
                "control_type": odemis.gui.CONTROL_COMBO,
                "choices": util.resolution_from_range,
            }),
            ("gain", {}),
            ("readoutRate", {}),
            ("temperature", {}),
            # what we don't want to display:
            ("translation", {
                "control_type": odemis.gui.CONTROL_NONE,
            }),
            ("targetTemperature", {
                "control_type": odemis.gui.CONTROL_NONE,
            }),
            ("fanSpeed", {
                "control_type": odemis.gui.CONTROL_NONE,
            }),
            ("pixelSize", {
                "control_type": odemis.gui.CONTROL_NONE,
            }),
        )),
    "light": {
            "power":
            {
                "control_type": odemis.gui.CONTROL_SLIDER,
                "scale": "cubic",
            },
        },
    "e-beam":
        OrderedDict((
            ("accelVoltage", {
                "label": "Accel. voltage",
                "tooltip": "Acceleration voltage"
            }),
            ("probeCurrent", {}),
            ("spotSize", {}),
            ("horizontalFoV", {
                "label": "HFW",
                "tooltip": "Horizontal Field Width",
                "control_type": odemis.gui.CONTROL_COMBO,
                "choices": util.hfw_choices,
                "accuracy": 2,
            }),
            ("magnification", {
                # Depends whether horizontalFoV is available or not
                "control_type": util.mag_if_no_hfw_ctype,
            }),
            ("dwellTime", {
                "control_type": odemis.gui.CONTROL_SLIDER,
                "range": (1e-9, 1),
                "scale": "log",
                "type": "float",
                "accuracy": 2,
                "event": wx.EVT_SCROLL_CHANGED
            }),
            ("scale", {
                # same as binning (but accepts floats)
                "control_type": odemis.gui.CONTROL_RADIO,
                "choices": util.binning_1d_from_2d,
                # means will make sure both dimensions are treated as one
                "type": "1d_binning",
            }),
            ("resolution", {
                "control_type": odemis.gui.CONTROL_COMBO,
                "choices": util.resolution_from_range,
            }),
            ("bpp", {
                "label": "BPP",
                "tooltip": "Bits per pixel",
            }),

             # what we don't want to display:
            ("power", {
                "control_type": odemis.gui.CONTROL_NONE,
            }),
            ("translation", {
                "control_type": odemis.gui.CONTROL_NONE,
            }),
            # TODO: might be useful if it's not read-only
            ("rotation", {
                "control_type": odemis.gui.CONTROL_NONE,
            }),
            ("pixelSize", {
                "control_type": odemis.gui.CONTROL_NONE,
            }),
        )),
    "spectrometer":
        OrderedDict((
            ("exposureTime", {
                "control_type": odemis.gui.CONTROL_SLIDER,
                "scale": "log",
                "range": (0.01, 500.0),
                "type": "float",
                "accuracy": 2,
            }),
            ("binning", {
                "control_type": odemis.gui.CONTROL_RADIO,
                "choices": util.binning_firstd_only,
                # means only 1st dimension can change
                "type": "1std_binning",
            }),
            ("resolution", {}),
            ("gain", {}),
            ("readoutRate", {}),
            ("temperature", {}),
            # what we don't want to display:
            ("targetTemperature", {
                "control_type": odemis.gui.CONTROL_NONE,
            }),
            ("fanSpeed", {
                "control_type": odemis.gui.CONTROL_NONE,
            }),
            ("pixelSize", {
                "control_type": odemis.gui.CONTROL_NONE,
            }),
        )),
    "spectrograph": {
            "wavelength":
            {
                "control_type": odemis.gui.CONTROL_SLIDER,
                "accuracy": 3,
            },
            "grating":  # that select the bandwidth observed
            {
                "control_type": odemis.gui.CONTROL_COMBO,
            },
        },
}

# Allows to override some values based on the microscope role
HW_SETTINGS_CONFIG_PER_ROLE = {
    "sparc": {
        "ccd":
        {
            "exposureTime":
            {
                "range": (0.01, 500.0),  # Typically much longer than on a SECOM
            },
        },
        "filter":
        {
            "band":  # to select the filter used
            {
                "label": "Filter",
                "control_type": odemis.gui.CONTROL_COMBO,
            },
        },
        "streamsem":
        {
            # VAs from the stream
            "dcPeriod":
            {
                "label": "Drift corr. period",
                "tooltip": "Maximum time between anchor region acquisitions",
                "control_type": odemis.gui.CONTROL_SLIDER,
                "scale": "log",
                "range": (1, 300),  # s, the VA allows a wider range, not typically needed
                "accuracy": 2,
            },
        },
        "streamspec":
        {
            # VAs from the stream, temporarily here
            "repetition":
            {
                "control_type": odemis.gui.CONTROL_COMBO,
                "choices": util.resolution_from_range_plus_point,
            },
            "pixelSize":
            {
                "control_type": odemis.gui.CONTROL_FLT,
            },
        },
        "streamar":
        {
            # VAs from the stream, temporarily here
            "repetition":
            {
                "control_type": odemis.gui.CONTROL_COMBO,
                "choices": util.resolution_from_range_plus_point,
            },
        },
    },
    "delphi": {
        # Some settings are continuous values, but it's more convenient to the user
        # to just pick from a small set (as in the Phenom GUI)
        "e-beam":
        {
            "accelVoltage":
            {
                "control_type": odemis.gui.CONTROL_RADIO,
                "choices": {4800, 5000, 7500, 10000},  # V
            },
            "spotSize":
            {
                "control_type": odemis.gui.CONTROL_RADIO,
                "choices": {2.1, 2.4, 2.7, 3, 3.3},  # some weird unit
            },
            "bpp":  # TODO: re-enable if 16-bits ever works correctly
            {
                "control_type": odemis.gui.CONTROL_NONE,
            },
        },
        # what we don't want to display:
        "ccd":
        {
            "temperature":  # On the Delphi it's pretty always at the target temp
            {
                "control_type": odemis.gui.CONTROL_NONE,
            },
            "readoutRate":  # Default value is good for all the standard cases
            {
                "control_type": odemis.gui.CONTROL_NONE,
            },
        },
    },
}
