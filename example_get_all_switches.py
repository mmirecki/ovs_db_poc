

from ovs_db.ovndb.impl_idl_ovn import OvsdbNbOvnIdl


idl = OvsdbNbOvnIdl(None, None)
lswitches = idl.get_all_logical_switches_with_ports()
print('lswitches:' + str(lswitches))