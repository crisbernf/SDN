from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER,CONFIG_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet,arp,ipv4
from ryu.lib.packet import ether_types
from ryu.lib.dpid import dpid_to_str,str_to_dpid
from ryu.lib import hub

class SimpleL2Switch(app_manager.RyuApp): #creating a simple switch as a Ryu App
	OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]
	
	#SECTION-1
	
	def __init__(self, *args, **kwargs):
		super(SimpleL2Switch, self).__init__(*args, **kwargs) #simpleL2switchis a child of Ryu App.
		self.mac_to_port = {} #{port1:[mac1,ip1],port2:[mac2,ip2]...},...} #to store the details of switch and connected hosts IP and mac address
	
	@set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
	def switch_features_handler(self, event): #this method handles switch feature requests and we install initial flow to forward all the packets to the controller incase of a table miss.
		self.sendto_controller(event)#Send to controller
        	
        	
        @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
        def _packet_in_handler(self, event):
        	pkt =packet.Packet(data=event.msg.data) # creating a packet with msg's data as payload
        	eth = pkt.get_protocols(ethernet.ethernet)[0] # fetching ethernet dataframe
        	if eth.ethertype == ether_types.ETH_TYPE_ARP: #handling ARP requests # ARP packet is ethernet dataframe's
        		self.handle_ARP(event) # Call method to handle ARP packets
        	elif eth.ethertype == ether_types.ETH_TYPE_IP:
        		self.handle_IP(event) # Call method to handle ipv4 packets
        		
        
        #SECTION-2
        
        def handle_ARP(self,event):# handle ARP packets
        	datapath = event.msg.datapath # datapath connection
        	ofproto = datapath.ofproto #ofproto of the datapath
        	in_port = event.msg.match['in_port'] # port through which the switch recieved this packet
        	parser = datapath.ofproto_parser
        	pkt = packet.Packet(data=event.msg.data)
        	eth = pkt.get_protocols(ethernet.ethernet)[0] # fetching ethernet dataframe
        	
        	arp_pkt = pkt.get_protocol(arp.arp)  #Extract ARP payload
        	self.mac_to_port[in_port] = [arp_pkt.src_mac,arp_pkt.src_ip] # Store details of switch, mapped host IPs and mac addresses
        	out_port = self.check_mactable(ofproto,'arp',arp_pkt.dst_mac) # If dst mac present return mac address from check_mactable function
        	actions = [parser.OFPActionOutput(out_port)] # list actions
        	match = self.simplematch(parser,eth.src,eth.dst,in_port) # create match object (match sequence)
        	self.add_flow(datapath, 1, match, actions, buffer_id=None) # add flow rule on datapath to handle packet
        	
        	
        def handle_IP(self,event): #handle IP packets
        	datapath = event.msg.datapath # datapath connection
        	ofproto = datapath.ofproto # ofproto of the datapath
        	in_port = event.msg.match['in_port'] # port through which the switch received this packet
        	parser = datapath.ofproto_parser
        	pkt = packet.Packet(data=event.msg.data)
        	eth = pkt.get_protocols(ethernet.ethernet)[0] # Fetching ethernet dataframes
        	
        	ip_pkt = pkt.get_protocol(ipv4.ipv4) #extract Ip payload
        	
        	out_port = self.check_mactable(ofproto,'ip',ip_pkt.dst) # If mac present return mac address from check_mactable function
        	match = self.simplematch(parser,eth.src,eth.dst,in_port) # Instructions for creation of match (match sequence)
        	actions = [parser.OFPActionOutput(port=out_port)] # list actions
        	if event.msg.buffer_id != ofproto.OFP_NO_BUFFER:
        		self.add_flow(datapath, 1, match,actions, event.msg.buffer_id) # adding a flow in case of no buffer
        	else:
        		self.add_flow(datapath, 1, match, actions)
        		
        		
        def check_mactable(self,ofproto,caller,para): # to check if an mac addr or IP addr exists in mac table
        	if caller == 'arp': # if the calling function is arp, then check mac address
        		for p in self.mac_to_port:
        			if self.mac_to_port[p][0] == para: #[p][0] If mac is a match to request
        				return p # return p as outport # if found return
        	elif caller == 'ip': # if calling function is ip , then check ip addr
        		for p in self.mac_to_port:
        			if self.mac_to_port[p][1] == para: # If mac is a match to request
        				return p # return corresponding port
        	return ofproto.OFPP_FLOOD # if no port is found flood all ports
        	
        	
        def sendto_controller(self,event): # initial installation of table miss flow
        	datapath = event.msg.datapath # datapath connection
        	ofproto = datapath.ofproto # ofproto of datapath
        	parser = datapath.ofproto_parser # parsing of packet
        	match = parser.OFPMatch() # creation of match sequence
        	actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,ofproto.OFPCML_NO_BUFFER)] #list actions - send to controller
        	inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,actions)]
        	mod = parser.OFPFlowMod(datapath=datapath,priority=0,match=match,instructions=inst)
        	datapath.send_msg(mod)
        	
        	
        def add_flow(self, datapath, priority, match, actions, buffer_id=None): # Function to add flow
        	ofproto = datapath.ofproto
        	parser = datapath.ofproto_parser
        	idle_timeout=45 # idle-timeout set to 45 seconds
        	hard_timeout=45
        	inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,actions)] #forming instructions
        	if buffer_id:
        		mod = parser.OFPFlowMod(datapath=datapath,buffer_id=buffer_id,priority=priority,idle_timeout=idle_timeout,hard_timeout = hard_timeout, match=match,instructions=inst)
        	else:
        		mod = parser.OFPFlowMod(datapath=datapath,priority=priority,match=match,idle_timeout=idle_timeout,hard_timeout = hard_timeout,instructions=inst)
        	self.logger.info("added flow for %s",mod)
        	datapath.send_msg(mod)
        	
        	
        #### request the packet to be forwarded onto a specific port from the switch ####
        
        def switchport_out(self,pkt,datapath,port): #accept raw data , serialise it and packetout from a OF switch
        	ofproto = datapath.ofproto #ofproto of datapath
        	parser = datapath.ofproto_parser # parsinf of packet
        	pkt.serialize() #serialise packet  (ie convert raw data)
        	self.logger.info("packet-out %s" %(pkt,)) #log packet info
        	data = pkt.data # Generate byte sequence
        	actions = [parser.OFPActionOutput(port=port)] # list actions
        	out = parser.OFPPacketOut(datapath = datapath,buffer_id=ofproto.OFP_NO_BUFFER,in_port=ofproto.OFPP_CONTROLLER,actions=actions,data=data) #
        	datapath.send_msg(out) # Send packet
        
        
        def simplematch(self,parser,src,dst,in_port):
        	match = parser.OFPMatch(in_port=in_port,eth_dst=dst,eth_src=src) # Instructions on what to do upon match (match sequence)
        	return match 
