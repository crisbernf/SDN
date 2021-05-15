from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet,arp,ipv4
from ryu.lib.packet import ether_types
from ryu.lib.dpid import dpid_to_str,str_to_dpid
from ryu.lib import hub

class SimpleL2Switch(app_manager.RyuApp):

	OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]
	"""docstring for SimpleL2Switch"""
	def __init__(self, *args, **kwargs):
		super(SimpleL2Switch, self).__init__(*args, **kwargs)
		self.mac_to_port = {}

	@set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
	def switch_features_handler(self, event):
		self.sendto_controller(event)

	@set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
	def _packet_in_handler(self, event):
		pkt = packet.Packet(data=event.msg.data)
		eth = pkt.get_protocols(ethernet.ethernet)[0]
		if eth.ethertype == ether_types.ETH_TYPE_ARP:
			self.handle_ARP(event)
			#arp_pkt = pkt.get_protocol(arp.arp)
			#src_ip = arp_pkt.src_ip
		elif eth.ethertype == ether_types.ETH_TYPE_IP:
			#ip_pkt = pkt.get_protocol(ipv4.ipv4)[0]
			#src_ip = ip_pkt.src
			self.handle_IP(event)

	def handle_ARP(self, event):
		datapath = event.msg.datapath
		ofproto = datapath.ofproto
		in_port = event.msg.match['in_port']
		parser = datapath.ofproto_parser
		pkt = packet.Packet(data=event.msg.data)
		eth = pkt.get_protocols(ethernet.ethernet)[0]

		arp_pkt = pkt.get_protocol(arp.arp)
		self.mac_to_port[in_port] = [arp_pkt.src_mac,arp_pkt.src_ip]
		out_port = self.check_mactable(ofproto,'arp',arp_pkt.dst_mac)
		actions = [parser.OFPActionOutput(out_port)]
		match = self.simplematch(parser,eth.src,eth.dst,in_port)
		self.add_flow(datapath,1,match,actions,buffer_id=None)

	def handle_IP(self, event):
		datapath = event.msg.datapath
		ofproto = datapath.ofproto
		in_port = event.msg.match['in_port']
		parser = datapath.ofproto_parser
		pkt = packet.Packet(data=event.msg.data)
		eth = pkt.get_protocols(ethernet.ethernet)[0]

		ip_pkt = pkt.get_protocol(ipv4.ipv4)

		out_port = self.check_mactable(ofproto,'ip', ip_pkt.dst)
		match = self.simplematch(parser,eth.src,eth.dst, in_port)
		actions = [parser.OFPActionOutput(port=out_port)]

		if event.msg.buffer_id != ofproto.OFP_NO_BUFFER:
			self.add_flow(datapath, 1, match, actions, event.msg.buffer_id)
		else:
			self.add_flow(datapath, 1, match, actions)

	def check_mactable(self, ofproto, caller, para):
		if caller == 'arp':
			for p in self.mac_to_port:
				if self.mac_to_port[p][0] == para:
					return p
		elif caller == 'ip':
			for p in self.mac_to_port:
				if self.mac_to_port[p][1] == para:
					return p

		return ofproto.OFPP_FLOOD

	def sendto_controller(self, event):
		datapath = event.msg.datapath
		ofproto = datapath.ofproto
		parser = datapath.ofproto_parser
		match = parser.OFPMatch()
		actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER, ofproto.OFPCML_NO_BUFFER)]
		inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,actions)]
		mod = parser.OFPFlowMod(datapath=datapath,priority=0,match=match,instructions=inst)
		datapath.send_msg(mod)

	def add_flow(self, datapath, priority, match, actions, buffer_id=None):
		ofproto = datapath.ofproto
		parser = datapath.ofproto_parser
		idle_timeout = 45
		hard_timeout = 45
		inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,actions)]
		if buffer_id:
			mod = parser.OFPFlowMod(datapath=datapath, buffer_id=buffer_id, priority=priority, idle_timeout=idle_timeout, hard_timeout=hard_timeout, match=match, instructions=inst)
		else:
			mod = parser.OFPFlowMod(datapath=datapath, priority=priority, match=match, idle_timeout=idle_timeout, hard_timeout=hard_timeout, instructions=inst)

		self.logger.info('added flow for %s', mod)
		datapath.send_msg(mod)

	def switchport_out(self,pkt,datapath,port):
		ofproto = datapath.ofproto
		parser = datapath.ofproto_parser
		pkt.serialize()
		self.logger.info('packet-out %s' %(pkt,))
		data = pkt.data
		actions = [parser.OFPActionOutput(port=port)]
		out = parser.EventOFPPacketOut(datapath=datapath, buffer_id=ofproto.OFP_NO_BUFFER, in_port=ofproto.OFPP_CONTROLLER, actions=actions, data=data)
		datapath.send_msg(out)

	def simplematch(self, parser, src, dst, in_port):
		match = parser.OFPMatch(in_port=in_port, eth_dst=dst, eth_src=src)
		return match



