# Copyright (c) 2015 Red Hat, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.


from ovs_db.compatibility.config import config

# from oslo_config import cfg

from ovs_db.ovsdb import api as ovsdb

def _connection_to_manager_uri(conn_uri):
    proto, addr = conn_uri.split(':', 1)
    if ':' in addr:
        ip, port = addr.split(':', 1)
        return 'p%s:%s:%s' % (proto, port, ip)
    else:
        return 'p%s:%s' % (proto, addr)


def enable_connection_uri(conn_uri):
    class OvsdbVsctlContext(object):
        vsctl_timeout = config.get_ovs_vsctl_timeout()

    manager_uri = _connection_to_manager_uri(conn_uri)
    api = ovsdb.API.get(OvsdbVsctlContext, 'vsctl')
    api.add_manager(manager_uri).execute(check_error=False, log_errors=True)
