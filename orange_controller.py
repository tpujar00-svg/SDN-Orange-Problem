from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

class OrangeController (object):
  def __init__ (self, connection):
    self.connection = connection
    connection.addListeners(self)
    self.mac_to_port = {} 

  def _handle_PacketIn (self, event):
    packet = event.parsed
    if not packet.parsed: return

    # 1. Learning Logic
    self.mac_to_port[packet.src] = event.port

    if packet.dst in self.mac_to_port:
        out_port = self.mac_to_port[packet.dst]

        # 2. Match-Action Rule (For future packets)
        msg = of.ofp_flow_mod()
        msg.match = of.ofp_match.from_packet(packet, event.port)
        msg.actions.append(of.ofp_action_output(port = out_port))
        msg.idle_timeout = 30
        self.connection.send(msg)

        # 3. Packet Out (For the CURRENT packet)
        msg_out = of.ofp_packet_out()
        msg_out.data = event.ofp
        msg_out.actions.append(of.ofp_action_output(port = out_port))
        self.connection.send(msg_out)
        log.info("Flow Rule & Packet Out: %s -> %s", packet.src, packet.dst)
    else:
        # 4. Flood if destination unknown
        msg = of.ofp_packet_out()
        msg.data = event.ofp
        msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
        self.connection.send(msg)

def launch ():
  def start_switch (event):
    log.info("Switch %s connected. Orange Logic Active.", event.dpid)
    OrangeController(event.connection)
  core.openflow.addListenerByName("ConnectionUp", start_switch)
