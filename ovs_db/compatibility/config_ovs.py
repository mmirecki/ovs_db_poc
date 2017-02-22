from ovs_db.compatibility.config import Config
from oslo_config import cfg
from ovs_db.compatibility.i18n import i18n

# ovs_db api.py

# TODO: Do we want to handle command line?
interface_map = {
    'vsctl': 'neutron.agent.ovsdb.impl_vsctl.OvsdbVsctl',
    'native': 'neutron.agent.ovsdb.impl_idl.NeutronOvsdbIdl',
}

DEFAULT_OVS_VSCTL_TIMEOUT = 10

OPTS = [
    cfg.StrOpt('ovsdb_interface',
               choices=interface_map.keys(),
               default='native',
               help=i18n.translate('The interface for interacting with the'
                                    ' OVSDB')),
    cfg.StrOpt('ovsdb_connection',
               default='tcp:127.0.0.1:6640',
               help=i18n.translate('The connection string for the '
                                   'OVSDB backend. Will be used by '
                                   'ovsdb-client when monitoring and used for '
                                   'the all ovsdb commands when native '
                                   'ovsdb_interface is enabled')),
    # impl_idl.py -> #neutron/conf/agent/ovs_conf.py
    cfg.IntOpt('ovs_vsctl_timeout',
               default=DEFAULT_OVS_VSCTL_TIMEOUT,
               help=i18n.translate('Timeout in seconds for ovs_db-vsctl commands.'
                                   'If the timeout expires, ovs_db commands will'
                                   ' fail with ALARMCLOCK error.')),
    # impl_idl_ovn
    cfg.StrOpt('ovn_nb_connection',
               default='tcp:127.0.0.1:6641',
               help=i18n.translate('The connection string for the '
                                   'OVN_Northbound OVSDB')),
    cfg.StrOpt('ovn_sb_connection',
               default='tcp:127.0.0.1:6642',
               help=i18n.translate('The connection string for the '
                                   'OVN_Southbound OVSDB')),
    cfg.IntOpt('ovsdb_connection_timeout',
               default=180,
               help=i18n.translate('Timeout in seconds for the OVSDB '
                                   'connection transaction')),
    cfg.BoolOpt('ovn_l3_mode',
                default=True,
                help=i18n.translate('Whether to use OVN native L3 support. '
                                    'Do not change '
                                    'the value for existing deployments that '
                                    'contain routers.')),
]
cfg.CONF.register_opts(OPTS, 'OVS')

cfg.CONF.import_opt('ovs_vsctl_timeout', 'neutron.agent.common.ovs_lib')


class OvsConfig(Config):
    def get_ovsdb_type(self):
        return cfg.CONF.OVS.ovsdb_interface

    def get_ovsdb_connection(self):
        return cfg.CONF.OVS.ovsdb_connection

    def get_ovs_vsctl_timeout(self):
        return cfg.CONF.OVS.ovs_vsctl_timeout

    def get_ovn_nb_connection(self):
        return cfg.CONF.ovn.ovn_nb_connection

    def get_ovn_sb_connection(self):
        return cfg.CONF.ovn.ovn_sb_connection

    def get_ovn_ovsdb_timeout(self):
        return cfg.CONF.ovn.ovsdb_connection_timeout
