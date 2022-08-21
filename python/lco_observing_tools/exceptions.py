# !usr/bin/env python
# -*- coding: utf-8 -*-
#
# Licensed under a 3-clause BSD license.
#
# @Author: Brian Cherinka
# @Date:   2017-12-05 12:01:21
# @Last modified by:   Brian Cherinka
# @Last Modified time: 2017-12-05 12:19:32

from __future__ import print_function, division, absolute_import


class Lco_observing_toolsError(Exception):
    """A custom core Lco_observing_tools exception"""

    def __init__(self, message=None):

        message = 'There has been an error' \
            if not message else message

        super(Lco_observing_toolsError, self).__init__(message)


class Lco_observing_toolsNotImplemented(Lco_observing_toolsError):
    """A custom exception for not yet implemented features."""

    def __init__(self, message=None):

        message = 'This feature is not implemented yet.' \
            if not message else message

        super(Lco_observing_toolsNotImplemented, self).__init__(message)


class Lco_observing_toolsAPIError(Lco_observing_toolsError):
    """A custom exception for API errors"""

    def __init__(self, message=None):
        if not message:
            message = 'Error with Http Response from Lco_observing_tools API'
        else:
            message = 'Http response error from Lco_observing_tools API. {0}'.format(message)

        super(Lco_observing_toolsAPIError, self).__init__(message)


class Lco_observing_toolsApiAuthError(Lco_observing_toolsAPIError):
    """A custom exception for API authentication errors"""
    pass


class Lco_observing_toolsMissingDependency(Lco_observing_toolsError):
    """A custom exception for missing dependencies."""
    pass


class Lco_observing_toolsWarning(Warning):
    """Base warning for Lco_observing_tools."""


class Lco_observing_toolsUserWarning(UserWarning, Lco_observing_toolsWarning):
    """The primary warning class."""
    pass


class Lco_observing_toolsSkippedTestWarning(Lco_observing_toolsUserWarning):
    """A warning for when a test is skipped."""
    pass


class Lco_observing_toolsDeprecationWarning(Lco_observing_toolsUserWarning):
    """A warning for deprecated features."""
    pass
