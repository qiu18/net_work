from pysnmp.entity.rfc3413.oneliner import cmdgen
class oid_get:
    def __init__(self, snmpip, port):
        self.snmpip = snmpip
        self.snmpport = port

    def snmp_get(self,port_oid):
        cg = cmdgen.CommandGenerator()  # 获得CommandGenerator对象
        errorindication, errorstatus, errorindex, varbindtable = cg.getCmd(
            # 社区信息，my-agent ,public 表示社区名,1表示snmp v2c版本，0代表v1,1代表v2c
            cmdgen.CommunityData('my-agent', 'public', 1),
            # 这是传输的通道，传输到IP 192.168.70.237, 端口 161上(snmp标准默认设备端UDP161端口,采集端UDP162端口)
            cmdgen.UdpTransportTarget(('172.106.219.201', 161)),
            '.1.3.6.1.2.1.2.2.1.8.' + port_oid,
            '.1.3.6.1.4.1.25506.2.70.1.1.1.12.' + port_oid
        )
        return (varbindtable)
