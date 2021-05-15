#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, OVSKernelSwitch, Host, RemoteController
from mininet.cli import CLI
from mininet.link import TCLink, Intf
from mininet.log import setLogLevel, info
from subprocess import call
from mn_wifi.net import Mininet_wifi
from mn_wifi.node import Station, OVSKernelAP
from mn_wifi.link import wmediumd
from mn_wifi.wmediumdConnector import interference

def myNetwork():

    net = Mininet_wifi(topo=None,
                       build=False,
                       link=wmediumd,
                       wmediumd_mode=interference,
                       )

    info( '*** Adding controller\n' )
    c0 = net.addController(name='c0',
                           controller=RemoteController,
                           protocol='tcp',
                           port=6653)

    
    info( '*** Adding Router\n')
    r0=net.addHost('r0', cls=Host)
    r0.cmd('sysctl -w net.ipv4.ip_forward=1')
    
    info( '*** Add sitches/APs\n')
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch) #Reception Bldg 1
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch) #Ground Office Bldg 1
    s3 = net.addSwitch('s3', cls=OVSKernelSwitch) #RD Servers Bldg 1
    s4 = net.addSwitch('s4', cls=OVSKernelSwitch) #Software Lab Bldg 1
    s5 = net.addSwitch('s5', cls=OVSKernelSwitch) #Seminar Room 1 Bldg 1
    s6 = net.addSwitch('s6', cls=OVSKernelSwitch) #Seminar Room 2 Bldg 1
    s7 = net.addSwitch('s7', cls=OVSKernelSwitch) #Prototyping Lab Bldg 1
    s8 = net.addSwitch('s8', cls=OVSKernelSwitch) #Management Team Office Bldg 1
    s9 = net.addSwitch('s9', cls=OVSKernelSwitch) #Small Office Building 2
    s10 = net.addSwitch('s10', cls=OVSKernelSwitch) #Warehouse Building 2

    info( '*** Add hosts/stations\n')
    
    #Reception Bldg 1
    Reception1 = net.addHost('h1', cls=Host, ip='172.16.11.50/24', defaultRoute='via 172.16.11.1')
    Reception2 = net.addHost('h2', cls=Host, ip='172.16.11.51/24', defaultRoute='via 172.16.11.1')

    #Ground Office Bldg 1
    of_gf_number = 5
    ip = 0
    Office_GF = [None] * (of_gf_number+1)
    for i in range(1, of_gf_number+1):
        ip = 50+(i-1)
        host_id = i+2
        Office_GF[i] = net.addHost("h%d"%host_id, cls=Host,ip="172.16.12.%d/24"%ip, defaultRoute='via 172.16.12.1')
        
    #RD Servers Bldg 1
    RD_SERVER1 = net.addHost('h104', cls=Host, ip='172.16.13.130/27', defaultRoute='via 172.16.13.129')
    RD_SERVER2 = net.addHost('h105', cls=Host, ip='172.16.13.131/27', defaultRoute='via 172.16.13.129')
    RD_SERVER3 = net.addHost('h106', cls=Host, ip='172.16.13.132/27', defaultRoute='via 172.16.13.129')
    RD_SERVER4 = net.addHost('h107', cls=Host, ip='172.16.13.133/27', defaultRoute='via 172.16.13.129')
    
    #Software Lab Bldg 1
    softLab_1f_number = 15
    Soft_Lab = [None] * (softLab_1f_number+1)
    for i in range(1, softLab_1f_number+1):
        ip = 60+(i-1)
        host_id = i+7
        Soft_Lab[i] = net.addHost("h%d"%host_id, cls=Host,ip="172.16.12.%d/24"%ip, defaultRoute='via 172.16.12.1')
    
    #Seminar Room 1 Bldg 1
    semroom1_1f_number = 20
    Semroom1 = [None] * (semroom1_1f_number+1)
    for i in range(1, semroom1_1f_number+1):
        ip = 80+(i-1)
        host_id = i+22
        Semroom1[i] = net.addHost("h%d"%host_id, cls=Host, ip="172.16.12.%d/24"%ip, defaultRoute='via 172.16.12.1')
    
    #Instructor PC Seminar Room 1
    Instr_PC1 = net.addHost('h63', cls=Host, ip='172.16.11.60/24', defaultRoute='via 172.16.11.1')
    
    #Seminar Room 2 Bldg 1
    semroom2_1f_number = 20
    Semroom2 = [None] * (semroom2_1f_number+1)
    for i in range(1, semroom2_1f_number+1):
        ip = 100+(i-1)
        host_id = i+42
        Semroom2[i] = net.addHost("h%d"%host_id, cls=Host, ip="172.16.12.%d/24"%ip, defaultRoute='via 172.16.12.1')
    
    #Instructor PC Seminar Room 2
    Instr_PC2 = net.addHost('h64', cls=Host, ip='172.16.11.61/24', defaultRoute='via 172.16.11.1')

    #Prototyping Lab Bldg 1    
    PLab_number = 10
    PLab = [None] * (PLab_number+1)
    for i in range(1, PLab_number+1):
        ip = 129+(i-1)
        host_id = i+64
        PLab[i] = net.addHost("h%d"%host_id, cls=Host, ip="172.16.12.%d/24"%ip, defaultRoute='via 172.16.12.1')   
   
    #Management Team Office Bldg 1
    Office1_SF_RD = net.addHost('h75', cls=Host, ip='172.16.12.139/24', defaultRoute='via 172.16.12.1')
    Office2_SF = net.addHost('h76', cls=Host, ip='172.16.12.150/24', defaultRoute='via 172.16.12.1')
    Office3_SF = net.addHost('h77', cls=Host, ip='172.16.12.151/24', defaultRoute='via 172.16.12.1')
    Office4_SF = net.addHost('h78', cls=Host, ip='172.16.12.152/24', defaultRoute='via 172.16.12.1')
    Office5_SF = net.addHost('h79', cls=Host, ip='172.16.12.153/24', defaultRoute='via 172.16.12.1')
    Office6_SF = net.addHost('h80', cls=Host, ip='172.16.12.154/24', defaultRoute='via 172.16.12.1')
    
    #Demonstration Room Connected to Management  Team Office
    Demo_PC = net.addHost('h81', cls=Host, ip='172.16.11.70/24', defaultRoute='via 172.16.11.1')
    
    #Small Office Building 2
    B2_PC1 = net.addHost('h102', cls=Host, ip='172.16.13.30/26', defaultRoute='via 172.16.13.1')
    B2_PC2 = net.addHost('h103', cls=Host, ip='172.16.13.31/26', defaultRoute='via 172.16.13.1')
    
    #Warehouse Building 2 - Cameras
    Cams_number = 10
    Cams = [None] * (Cams_number+1)
    for i in range(1, Cams_number + 1):
        ip = 10 + (i - 1)
        host_id = i + 81
        Cams[i] = net.addHost("h%d" % host_id, cls=Host, ip="172.16.13.%d/26" % ip, defaultRoute='via 172.16.13.1')

    #Warehouse Building 2 - Sensors
    Sens_number = 10
    Sens = [None] * (Sens_number+1)
    for i in range(1, Sens_number + 1):
        ip = 20 + (i - 1)
        host_id = i + 91
        Sens[i] = net.addHost("h%d" % host_id, cls=Host, ip="172.16.13.%d/26" % ip, defaultRoute='via 172.16.13.1')
    
    info("*** Creating Wireless Access Points\n")
    
    #Building 1 Access Points
    ap_number = 7
    aps = [None] * (ap_number+2)
    for i in range(1, ap_number+1):
        aps[i] = net.addAccessPoint("ap%d"% i,ssid="ap%d-ssid"% i, mode="g")
    
    #Building 2 Access Point
    aps[8] = net.addAccessPoint("ap8",ssid="ap8-ssid", mode="g")
    info("*** Configuring Propagation Model\n")
    net.setPropagationModel(model="logDistance", exp=4.5)
    info("*** Configuring wifi nodes \n")
    net.configureWifiNodes()
    
    info( '*** Add links\n')
    
    #Link Between Network Devices
    net.addLink(s1, s2, 48, 48)
    net.addLink(s2, s3, 47, 47)
    net.addLink(s3, s4, 46, 47)
    net.addLink(s3, r0, 45, 1)
    net.addLink(s3, r0, 44, 2)
    net.addLink(s4, s5, 48, 48)
    net.addLink(s5, s6, 47, 47)
    net.addLink(s6, s7, 48, 48)
    net.addLink(s7, s8, 47, 47)
    net.addLink(s8, s9, 48, 48)
    net.addLink(s9, s10, 47, 47)
    
    #Links Reception Bldg 1
    net.addLink(Reception1, s1)
    net.addLink(Reception2, s1)
    net.addLink(s1, aps[1]) #Wi-fi   

    #Links Ground Office Bldg 1
    for i in range(1, of_gf_number + 1):
        net.addLink(Office_GF[i], s2)
    net.addLink(s2, aps[2]) #Wi-fi
    
    #Links RD Servers Bldg 1
    net.addLink(RD_SERVER1, s3)
    net.addLink(RD_SERVER2, s3)
    net.addLink(RD_SERVER3, s3)
    net.addLink(RD_SERVER4, s3)
    
    #Links Software Lab Bldg 1
    for i in range(1, softLab_1f_number + 1):
        net.addLink(Soft_Lab[i], s4)
    net.addLink(s4, aps[3]) #Wi-fi

    #Links Seminar Room 1 Bldg 1
    for i in range(1, semroom1_1f_number + 1):
        net.addLink(Semroom1[i], s5)
    net.addLink(s5, aps[4])    

    #Link Instructor PC Seminar Room 1
    net.addLink(s5,Instr_PC1, 30,1)
    
    #Links Seminar Room 2 Bldg 1
    for i in range(1, semroom2_1f_number + 1):
        net.addLink(Semroom2[i], s6)
    net.addLink(s6, aps[5])

    #Link Instructor PC Seminar Room 2
    net.addLink(s6,Instr_PC2, 30, 1)
    
    #Links Prototyping Lab Bldg 1 
    for i in range(1, PLab_number + 1):
        net.addLink(PLab[i], s7)
    net.addLink(s7, aps[6])
    
    #Links Management Team Office Bldg 1
    net.addLink(s8, aps[7])
    net.addLink(s8, Office1_SF_RD)
    net.addLink(s8, Office2_SF)
    net.addLink(s8, Office3_SF)
    net.addLink(s8, Office4_SF)
    net.addLink(s8, Office5_SF)
    net.addLink(s8, Office6_SF)
    
    #Demonstration Room Link to Management Team Office
    net.addLink(s8, Demo_PC, 21, 1)
    
    #Links Small Office Building 2
    net.addLink(s9, B2_PC1)
    net.addLink(s9, B2_PC2)
    net.addLink(s9, aps[8])
    
    #Links Warehouse Building 2 - Cameras
    for i in range(1, Cams_number + 1):
        net.addLink(Cams[i], s10)

    #Links Warehouse Building 2 - Sensors
    for i in range(1, Sens_number + 1):
        net.addLink(Sens[i], s10)

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches/APs\n')
    net.get('ap1').start([])
    net.get('ap2').start([])
    net.get('ap3').start([])
    net.get('ap4').start([])
    net.get('ap5').start([])
    net.get('ap6').start([])
    net.get('ap7').start([])
    net.get('ap8').start([])
    net.get('s1').start([c0])
    net.get('s2').start([c0])
    net.get('s3').start([c0])
    net.get('s4').start([c0])
    net.get('s5').start([c0])
    net.get('s6').start([c0])
    net.get('s7').start([c0])
    net.get('s8').start([c0])
    net.get('s9').start([c0])
    net.get('s10').start([c0])
    
    info(' *** Defining Trunk Ports\n')
    s1.cmd('ovs-vsctl set port s1-eth48 trunks=11,12,13,15')
    s1.cmd('ovs-vsctl set port s2-eth48 trunks=11,12,13,15')
    s1.cmd('ovs-vsctl set port s2-eth47 trunks=11,12,13,15')
    s1.cmd('ovs-vsctl set port s3-eth47 trunks=11,12,13,15')
    s1.cmd('ovs-vsctl set port s3-eth46 trunks=11,12,13,15')
    s1.cmd('ovs-vsctl set port s3-eth48 trunks=11,12,13,15')
    s1.cmd('ovs-vsctl set port s4-eth47 trunks=11,12,13,15')
    s1.cmd('ovs-vsctl set port s4-eth48 trunks=11,12,13,15')
    s1.cmd('ovs-vsctl set port s5-eth47 trunks=11,12,13,15')
    s1.cmd('ovs-vsctl set port s5-eth48 trunks=11,12,13,15')
    s1.cmd('ovs-vsctl set port s6-eth47 trunks=11,12,13,15')
    s1.cmd('ovs-vsctl set port s6-eth48 trunks=11,12,13,15')
    s1.cmd('ovs-vsctl set port s7-eth47 trunks=11,12,13,15')    
    s1.cmd('ovs-vsctl set port s7-eth48 trunks=11,12,13,15')
    s1.cmd('ovs-vsctl set port s8-eth47 trunks=11,12,13,15')
    s1.cmd('ovs-vsctl set port s8-eth48 trunks=11,12,13,15')
    s1.cmd('ovs-vsctl set port s9-eth47 trunks=11,12,13,15')
    s1.cmd('ovs-vsctl set port s9-eth48 trunks=11,12,13,15')
    s1.cmd('ovs-vsctl set port s10-eth47 trunks=11,12,13,15')
    
    info(' ***Defining Access Ports\n')
    
    #Recepcion
    s1_port_num = 20
    for i in range(1, s1_port_num + 1):
        s1.cmd('ovs-vsctl set port %i s1-eth%d tag=11')
    
    #Ground Office Bldg 1
    s2_port_num = 20
    for i in range(1, s2_port_num + 1):
        s1.cmd('ovs-vsctl set port %i s2-eth%d tag=12')
    
    #RD Servers Bldg 1
    s3_port_num = 20
    for i in range(1, s3_port_num + 1):
        s1.cmd('ovs-vsctl set port %i s3-eth%d tag=15')

    #Software Lab Bldg 1
    s4_port_num = 20
    for i in range(1, s4_port_num + 1):
        s1.cmd('ovs-vsctl set port %i s4-eth%d tag=12')

    #Seminar Room 1 Bldg 1
    s5_port_num = 25
    for i in range(1, s5_port_num + 1):
        s1.cmd('ovs-vsctl set port %i s5-eth%d tag=12')

    #Instructor PC Seminar Room 1
    s1.cmd('ovs-vsctl set port s5-eth30 tag=11')
    
    #Seminar Room 2 Bldg 1
    s6_port_num = 25
    for i in range(1, s6_port_num + 1):
        s1.cmd('ovs-vsctl set port %i s6-eth%d tag=12')
    
    #Instructor PC Seminar Room 2
    s1.cmd('ovs-vsctl set port s6-eth30 tag=11')
    
    #Prototyping Lab Bldg 1
    s7_port_num = 20
    for i in range(1, s7_port_num + 1):
        s1.cmd('ovs-vsctl set port %i s7-eth%d tag=12')  

    #Management Team Office Bldg 1
    s8_port_num = 20
    for i in range(1, s8_port_num + 1):
        s1.cmd('ovs-vsctl set port %i s8-eth%d tag=12')

    #Demonstration Room Connected to Management Team Office
    s1.cmd('ovs-vsctl set port s8-eth21 tag=11')
    
    #Small Office Building 2
    s9_port_num = 20
    for i in range(1, s9_port_num + 1):
        s1.cmd('ovs-vsctl set port %i s9-eth%d tag=13')
        
    #Warehouse Building 2 - Cameras ans Sensors
    s10_port_num = 20
    for i in range(1, s10_port_num + 1):
        s1.cmd('ovs-vsctl set port %i s10-eth%d tag=13')
        
    #Access Port Between s3 and r0
    s1.cmd('ovs-vsctl set port s3-eth45 tag=15')
    s1.cmd('ovs-vsctl set port s3-eth44 tag=12')
    
    info(' ***Creating IP Addresses r0\n')
    r0.cmd('ifconfig r0-eth1 172.16.13.129 netmask 255.255.255.224')
    r0.cmd('ifconfig r0-eth2 172.16.12.1 netmask 255.255.255.0')

    info( '*** Post configure nodes\n')

    CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()

