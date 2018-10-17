# Copyright (c) 2014 Amazon.com, Inc. or its affiliates. All Rights Reserved
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish, dis-
# tribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the fol-
# lowing conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABIL-
# ITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
# SHALL THE AUTHOR BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
#
from lib.boto.regioninfo import RegionInfo, get_regions
from lib.boto.regioninfo import connect


def regions():
    """
    Get all available regions for the Amazon CloudSearch Domain service.

    :rtype: list
    :return: A list of :class:`boto.regioninfo.RegionInfo`
    """
    from lib.boto.cloudsearchdomain.layer1 import CloudSearchDomainConnection
    return get_regions('cloudsearchdomain',
                       connection_cls=CloudSearchDomainConnection)


def connect_to_region(region_name, **kw_params):
    from lib.boto.cloudsearchdomain.layer1 import CloudSearchDomainConnection
    return connect('cloudsearchdomain', region_name,
                   connection_cls=CloudSearchDomainConnection, **kw_params)
