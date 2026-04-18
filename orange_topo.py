from mininet.topo import Topo

class OrangeTopo(Topo):
    def build(self):
        # Adding a switch and 3 hosts
        s1 = self.addSwitch('s1')
        h1 = self.addHost('h1', ip='10.0.0.1')
        h2 = self.addHost('h2', ip='10.0.0.2')
        h3 = self.addHost('h3', ip='10.0.0.3')

        self.addLink(h1, s1)
        self.addLink(h2, s1)
        self.addLink(h3, s1)

topos = { 'orangetopo': (lambda: OrangeTopo()) }
