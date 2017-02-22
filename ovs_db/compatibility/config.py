class Config(object):
    def get_ovsdb_type(self):
        # MM: We do not want vsctl - this is the cmd line way
        return 'native'

    def get_ovsdb_connection(self):
        return 'tcp:127.0.0.1:6640'

    def get_ovs_vsctl_timeout(self):
        return 10

    def get_ovn_nb_connection(self):
        return 'tcp:127.0.0.1:6641'

    def get_ovn_sb_connection(self):
        return 'tcp:127.0.0.1:6642'

    def get_ovn_ovsdb_timeout(self):
        return 180

    def is_ovn_l3(self):
        return True

config = Config()
