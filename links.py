import sys

from mininet.node import Controller, OVSKernelSwitch, Host
from mininet.log import setLogLevel, info
from mn_wifi.net import Mininet_wifi
from mn_wifi.node import Station, OVSKernelAP
from mn_wifi.cli import CLI
from mn_wifi.link import wmediumd
from mn_wifi.wmediumdConnector import interference


# r1 - VLAN 8 - WLAN_Staff - 172.16.8.0/23
# r1 - VLAN 10 - Management - 172.16.10.0/24
# r1 - VLAN 11 - Intranet - 172.16.11.0/24
# r1 - VLAN 12 - Internet - 172.16.12.0/24
# r1 - VLAN 13 - Control - 172.16.13.0/26
# r1 - VLAN 14 - WLAN_VIP - 172.16.13.64/26
# r1 - VLAN 15 - RD - 172.16.13.128/27
# r1 - VLAN 55 - Native
# server   -  172.16.0.1/30

def topology(args):
    "Create a network."
    net = Mininet_wifi(topo=None,
                       build=False,
                       link=wmediumd,
                       wmediumd_mode=interference,
                       )


    info("*** Creating hosts in Building 1 \n")

    info("*** Reception \n")
    Reception1 = net.addHost('h1', ip='172.16.11.50/24', defaultRoute='via 172.16.11.1')
    Reception2 = net.addHost('h2', ip='172.16.11.51/24', defaultRoute='via 172.16.11.1')

    info("*** Ground floor Office \n")
    of_gf_number = 5
    ip = 0
    Office_GF = [None] * (of_gf_number+1)
    for i in range(1, of_gf_number+1):
        ip = 50+(i-1)
        host_id = i+2
        Office_GF[i] = net.addHost("h%d"%host_id,ip="172.16.12.%d/24"%ip, defaultRoute='via 172.16.12.1')

    info("*** Creating Router \n")
    r1 = net.addHost('r1', ip='172.16.11.1/24')

    info("*** Software Lab \n")
    softLab_1f_number = 15
    Soft_Lab = [None] * (softLab_1f_number+1)
    for i in range(1, softLab_1f_number+1):
        ip = 60+(i-1)
        host_id = i+7
        Soft_Lab[i] = net.addHost("h%d"%host_id,ip="172.16.12.%d/24"%ip, defaultRoute='via 172.16.12.1')

    info("*** Seminar room 1 \n")
    semroom1_1f_number = 20
    Semroom1 = [None] * (semroom1_1f_number+1)
    for i in range(1, semroom1_1f_number+1):
        ip = 80+(i-1)
        host_id = i+22
        Semroom1[i] = net.addHost("h%d"%host_id,ip="172.16.12.%d/24"%ip, defaultRoute='via 172.16.12.1')
    Instr_PC1 = net.addHost('h63', ip='172.16.11.60/24', defaultRoute='via 172.16.11.1')

    info("*** Seminar room 2 \n")
    semroom2_1f_number = 20
    Semroom2 = [None] * (semroom2_1f_number+1)
    for i in range(1, semroom2_1f_number+1):
        ip = 100+(i-1)
        host_id = i+42
        Semroom2[i] = net.addHost("h%d"%host_id,ip="172.16.12.%d/24"%ip, defaultRoute='via 172.16.12.1')
    Instr_PC2 = net.addHost('h64', ip='172.16.11.61/24', defaultRoute='via 172.16.11.1')


    info("*** Prototyping Lab \n")
    PLab_number = 10
    PLab = [None] * (PLab_number+1)
    for i in range(1, PLab_number+1):
        ip = 129+(i-1)
        host_id = i+64
        PLab[i] = net.addHost("h%d"%host_id,ip="172.16.12.%d/24"%ip, defaultRoute='via 172.16.12.1')

    info("*** Management Team Office \n")
    Office1_SF_RD = net.addHost('h75', ip='172.16.12.139/24', defaultRoute='via 172.16.12.1')
    Office2_SF = net.addHost('h76', ip='172.16.12.150/24', defaultRoute='via 172.16.12.1')
    Office3_SF = net.addHost('h77', ip='172.16.12.151/24', defaultRoute='via 172.16.12.1')
    Office4_SF = net.addHost('h78', ip='172.16.12.152/24', defaultRoute='via 172.16.12.1')
    Office5_SF = net.addHost('h79', ip='172.16.12.153/24', defaultRoute='via 172.16.12.1')
    Office6_SF = net.addHost('h80', ip='172.16.12.154/24', defaultRoute='via 172.16.12.1')

    info("*** Demonstration room \n")
    Demo_PC = net.addHost('h81', ip='172.16.11.70/24', defaultRoute='via 172.16.11.1')

    ap_number = 7
    aps = [None] * (ap_number+2)
    info("*** Creating wireless access points in Building 1\n")
    for i in range(1, ap_number+1):
        aps[i] = net.addAccessPoint("ap%d"% i,ssid="ap%d-ssid"% i, mode="g")

    info("*** Creating hosts in Building 2 \n")

    Cams_number = 10
    Cams = [None] * (Cams_number+1)
    for i in range(1, Cams_number + 1):
        ip = 10 + (i - 1)
        host_id = i + 81
        Cams[i] = net.addHost("h%d" % host_id, ip="172.16.13.%d/26" % ip, defaultRoute='via 172.16.13.1')

    Sens_number = 10
    Sens = [None] * (Sens_number+1)
    for i in range(1, Sens_number + 1):
        ip = 20 + (i - 1)
        host_id = i + 91
        Sens[i] = net.addHost("h%d" % host_id, ip="172.16.13.%d/26" % ip, defaultRoute='via 172.16.13.1')

    B2_PC1 = net.addHost('h102', ip='172.16.13.30/26', defaultRoute='via 172.16.13.1')
    B2_PC2 = net.addHost('h103', ip='172.16.13.31/26', defaultRoute='via 172.16.13.1')

    info("*** Creating wireless access point in Building 2\n")

    aps[8] = net.addAccessPoint("ap8",ssid="ap8-ssid", mode="g")
    info("*** Configuring Propagation Model\n")
    net.setPropagationModel(model="logDistance", exp=4.5)
    info("*** Configuring wifi nodes \n")
    net.configureWifiNodes()

    info("*** Creating server room equipment \n")
    RD_SERVER1 = net.addHost('h104', ip='172.16.13.130/27', defaultRoute='via 172.16.13.129')
    RD_SERVER2 = net.addHost('h104', ip='172.16.13.131/27', defaultRoute='via 172.16.13.129')
    RD_SERVER3 = net.addHost('h104', ip='172.16.13.132/27', defaultRoute='via 172.16.13.129')
    RD_SERVER4 = net.addHost('h104', ip='172.16.13.133/27', defaultRoute='via 172.16.13.129')
    server = net.addSwitch('s0', ip='172.16.0.1/30')
    c0 = net.addController(name='c0',
                           controller=Controller,
                           protocol='tcp',
                           port=6653)
    
    info("*** Creating switches in Building 1\n")
    
    info("*** Creating switch in the reception \n")
    
    sw1= net.addSwitch('sw1',cls=OVSKernelSwitch)
    
    info("*** Creating switch in the ground Office \n")
    sw2 = net.addSwitch('sw2',cls=OVSKernelSwitch)

    info("*** Creating switch for RD servers \n")
    sw3 = net.addSwitch('sw3',cls=OVSKernelSwitch)

    info("*** Creating switch in the Software Lab \n")
    sw4 = net.addSwitch('sw4',cls=OVSKernelSwitch)

    info("*** Creating switch in the Seminar room 1 \n")
    sw5 = net.addSwitch('sw5',cls=OVSKernelSwitch)
    
    info("*** Creating switch in the Seminar room 2 \n")
    sw6 = net.addSwitch('sw6',cls=OVSKernelSwitch)
    
    info("*** Creating switch in the Prototyping Lab \n")
    sw7 = net.addSwitch('sw7',cls=OVSKernelSwitch)

    info("*** Creating switch in the Management Team Office \n")

    sw8 = net.addSwitch('sw8',cls=OVSKernelSwitch)
    
    info("*** Creating switches in Building 2\n")
    
    info("*** Creating switch in the Small Office \n")

    sw9= net.addSwitch('sw9',cls=OVSKernelSwitch)

    info("*** Creating switch in the Warehouse \n")
    sw10= net.addSwitch('sw10',cls=OVSKernelSwitch)

    info("*** Adding Links in Building 1 \n")

    info("*** Reception \n")
    net.addLink(Reception1, sw1)
    net.addLink(Reception2, sw1)
    net.addLink(sw1, aps[1]) #Wi-fi
    net.addLink(sw1, server)

    info("*** Ground floor offices \n")
    for i in range(1, of_gf_number + 1):
        net.addLink(Office_GF[i], sw2)
    net.addLink(sw2, aps[2]) #Wi-fi
    net.addLink(sw2, server)

    info("*** Server room \n")
    net.addLink(RD_SERVER1, sw3)
    net.addLink(RD_SERVER2, sw3)
    net.addLink(RD_SERVER3, sw3)
    net.addLink(RD_SERVER4, sw3)

    info("*** Software lab \n")
    for i in range(1, softLab_1f_number + 1):
        net.addLink(Soft_Lab[i], sw4)
    net.addLink(sw4, aps[3]) #Wi-fi
    net.addLink(sw4, server)

    info("*** Seminar room 1 \n")
    for i in range(1, semroom1_1f_number + 1):
        net.addLink(Semroom1[i], sw5)
    net.addLink(sw5, aps[4])
    #net.addLink(sw5, server)
    net.addLink(sw5,Instr_PC1)

    info("*** Seminar room 2 \n")
    for i in range(1, semroom2_1f_number + 1):
        net.addLink(Semroom2[i], sw6)
    net.addLink(sw6, aps[5])
    #net.addLink(sw6, server)
    net.addLink(sw6,Instr_PC2)

    info("*** Prototyping Lab \n")
    for i in range(1, PLab_number + 1):
        net.addLink(PLab[i], sw7)
    net.addLink(sw7, aps[6])
    net.addLink(sw7, server)

    info("*** Management Team Office \n")
    net.addLink(sw8, aps[7])
    net.addLink(sw8, server)
    net.addLink(sw8, Office1_SF_RD)
    net.addLink(sw8, Office2_SF)
    net.addLink(sw8, Office3_SF)
    net.addLink(sw8, Office4_SF)
    net.addLink(sw8, Office5_SF)
    net.addLink(sw8, Office6_SF)
    net.addLink(sw8, Demo_PC)

    info("*** Adding Links in Building 2 \n")

    info("*** Small Office \n")
    net.addLink(sw9, B2_PC1)
    net.addLink(sw9, B2_PC2)
    net.addLink(sw9, aps[8])
    net.addLink(sw9, server)
    info("*** Warehouse \n")
    for i in range(1, Cams_number + 1):
        net.addLink(Cams[i], sw10)
    for i in range(1, Sens_number + 1):
        net.addLink(Sens[i], sw10)
    net.addLink(sw9, sw10)

    info("*** Adding Links between switches \n")

    net.addLink(sw1,sw2,24,24)
    net.addLink(sw2,sw3,23,23)
    net.addLink(sw3,sw4,22,23)
    net.addLink(sw3,sw9,21,23)
    net.addLink(sw3,r1,24,1)
    net.addLink(sw4,sw5,24,24)
    net.addLink(sw5,sw6,23,23)
    net.addLink(sw6,sw7,24,24)
    net.addLink(sw7,sw8,23,23)
    net.addLink(sw9,sw10,24,24)

    info("*** Adding VLAN Trunking \n")
    sw1.cmd('sh ovs-vsctl set port sw1-eth24 trunks=8,10,11,12,13,14,15,55')
    sw2.cmd('sh ovs-vsctl set port sw2-eth24 trunks=8,10,11,12,13,14,15,55')
    sw2.cmd('sh ovs-vsctl set port sw2-eth23 trunks=8,10,11,12,13,14,15,55')
    sw3.cmd('sh ovs-vsctl set port sw3-eth23 trunks=8,10,11,12,13,14,15,55')
    sw3.cmd('sh ovs-vsctl set port sw3-eth22 trunks=8,10,11,12,13,14,15,55')
    sw3.cmd('sh ovs-vsctl set port sw3-eth21 trunks=8,10,11,12,13,14,15,55')
    sw3.cmd('sh ovs-vsctl set port sw3-eth24 trunks=8,10,11,12,13,14,15,55')
    sw4.cmd('sh ovs-vsctl set port sw4-eth24 trunks=8,10,11,12,13,14,15,55')
    sw4.cmd('sh ovs-vsctl set port sw4-eth23 trunks=8,10,11,12,13,14,15,55')
    sw5.cmd('sh ovs-vsctl set port sw5-eth24 trunks=8,10,11,12,13,14,15,55')
    sw5.cmd('sh ovs-vsctl set port sw5-eth23 trunks=8,10,11,12,13,14,15,55')
    sw6.cmd('sh ovs-vsctl set port sw6-eth24 trunks=8,10,11,12,13,14,15,55')
    sw6.cmd('sh ovs-vsctl set port sw6-eth23 trunks=8,10,11,12,13,14,15,55')
    sw7.cmd('sh ovs-vsctl set port sw7-eth24 trunks=8,10,11,12,13,14,15,55')
    sw7.cmd('sh ovs-vsctl set port sw7-eth23 trunks=8,10,11,12,13,14,15,55')
    sw8.cmd('sh ovs-vsctl set port sw8-eth23 trunks=8,10,11,12,13,14,15,55')
    sw9.cmd('sh ovs-vsctl set port sw9-eth24 trunks=8,10,11,12,13,14,15,55')
    sw9.cmd('sh ovs-vsctl set port sw9-eth23 trunks=8,10,11,12,13,14,15,55')
    sw10.cmd('sh ovs-vsctl set port sw10-eth24 trunks=8,10,11,12,13,14,15,55')

    info("*** Adding VLAN Tagging \n")
    
    sw1_port_num = 4
    for i in range(1, sw1_port_num + 1):
        sw1.cmd('sh ovs-vsctl set port %i sw1-eth%d tag=11')

    sw2_port_num = 7
    for i in range(1, sw2_port_num + 1):
        sw2.cmd('sh ovs-vsctl set port %i sw2-eth%d tag=12')

    sw3_port_num = 4
    for i in range(1, sw3_port_num + 1):
        sw3.cmd('sh ovs-vsctl set port %i sw3-eth%d tag=15')

    sw4_port_num = 17
    for i in range(1, sw4_port_num + 1):
        sw4.cmd('sh ovs-vsctl set port %i sw4-eth%d tag=12')

    sw5_port_num = 22
    for i in range(1, sw5_port_num + 1):
        sw5.cmd('sh ovs-vsctl set port %i sw5-eth%d tag=12')

    sw5.cmd('sh ovs-vsctl set port sw5-eth23 tag=11')

    sw6_port_num = 22
    for i in range(1, sw6_port_num + 1):
        sw6.cmd('sh ovs-vsctl set port %i sw6-eth%d tag=12')

    sw6.cmd('sh ovs-vsctl set port sw6-eth23 tag=11')

    sw7_port_num = 12
    for i in range(1, sw7_port_num + 1):
        sw7.cmd('sh ovs-vsctl set port %i sw7-eth%d tag=12')

    sw8_port_num = 8
    for i in range(1, sw8_port_num + 1):
        sw8.cmd('sh ovs-vsctl set port %i sw8-eth%d tag=12')

    sw8.cmd('sh ovs-vsctl set port sw8-eth9 tag=11')

    sw9_port_num = 5
    for i in range(1, sw9_port_num + 1):
        sw9.cmd('sh ovs-vsctl set port %i sw9-eth%d tag=13')

    sw10_port_num = 21
    for i in range(1, sw10_port_num + 1):
        sw10.cmd('sh ovs-vsctl set port %i sw10-eth%d tag=13')

    info("*** Adding Routing \n")
    r1.cmd('systcl -w net.ipv4.ip_forward=1')
    r1.cmd('ifconfig r1-eth1.8 172.16.8.1 netmask 255.255.254.0')
    r1.cmd('ifconfig r1-eth1.10 172.16.10.1 netmask 255.255.255.0')
    r1.cmd('ifconfig r1-eth1.11 172.16.11.1 netmask 255.255.255.0')
    r1.cmd('ifconfig r1-eth1.12 172.16.12.1 netmask 255.255.255.0')
    r1.cmd('ifconfig r1-eth1.13 172.16.13.1 netmask 255.255.255.192')
    r1.cmd('ifconfig r1-eth1.14 172.16.13.65 netmask 255.255.255.192')
    r1.cmd('ifconfig r1-eth1.15 172.16.13.129 netmask 255.255.255.224')

    info("*** Starting network\n")
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    net.get('s0').start([c0])
    net.get('ap1').start([])
    net.get('ap2').start([])
    net.get('ap3').start([])
    net.get('ap4').start([])
    net.get('ap5').start([])
    net.get('ap6').start([])
    net.get('ap7').start([])
    net.get('ap8').start([])
    net.get('sw1').start([])
    net.get('sw2').start([])
    net.get('sw3').start([])
    net.get('sw4').start([])
    net.get('sw5').start([])
    net.get('sw6').start([])
    net.get('sw7').start([])
    net.get('sw8').start([])
    net.get('sw9').start([])
    net.get('sw10').start([])

    info("*** Running CLI\n")
    CLI(net)
    info("*** Stopping network\n")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology(sys.argv)
