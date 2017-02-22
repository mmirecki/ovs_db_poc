from ovs_db.compatibility.config import config as ovn_config
from ovs_db.compatibility import constants

from neutron_lib.plugins import directory


class DI(object):
    def l3_plugin_schedule_unhosted_gateways(self):
        pass


class DI_OVS(object):
    def l3_plugin_schedule_unhosted_gateways(self):
        if ovn_config.is_ovn_l3():
            l3_plugin = directory.get_plugin(constants.L3)
            l3_plugin.schedule_unhosted_gateways()


di = DI()
