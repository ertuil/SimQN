from qns.quantum.node import QuantumNodeGenerationProtocol, QuantumNodeSwappingProtocol, QuantumNodeDistillationProtocol
from qns.schedular import Simulator, Protocol, simulator
from qns.quantum.link import QuantumChannel, GenerationProtocal
from qns.quantum import QuantumNode
from qns.quantum import QuantumNetwork
from qns.log import log
import time


class PrintProtocol(Protocol):
    def handle(_self, simulator: Simulator, msg: object, source=None, event=None):
        self = _self.entity
        count = 0
        log.info("check {}: {}", self, self.registers)


s = Simulator(0, 3600, 100000)
log.set_debug(True)
log.install(s)

n1 = QuantumNode(name="n1", registers_number=10)
ngp1 = QuantumNodeGenerationProtocol(n1)
nsp1 = QuantumNodeSwappingProtocol(n1)
ndp1 = QuantumNodeDistillationProtocol(n1, threshold=0.9)
npp1 = PrintProtocol(n1)
n1.inject_protocol([ngp1, ndp1, nsp1])

n2 = QuantumNode(name="n2", registers_number=20)
ngp2 = QuantumNodeGenerationProtocol(n2)
nsp2 = QuantumNodeSwappingProtocol(n2)
ndp2 = QuantumNodeDistillationProtocol(n2, threshold=0.9)
npp2 = PrintProtocol(n2)
n2.inject_protocol([ngp2, ndp2, nsp2])

n3 = QuantumNode(name="n3", registers_number=20)
ngp3 = QuantumNodeGenerationProtocol(n3)
nsp3 = QuantumNodeSwappingProtocol(n3)
npp3 = PrintProtocol(n3)
n3.inject_protocol([ngp3, nsp3])

n4 = QuantumNode(name="n4", registers_number=10)
ngp4 = QuantumNodeGenerationProtocol(n4)
nsp4 = QuantumNodeSwappingProtocol(n4)
ndp4 = QuantumNodeDistillationProtocol(n4, threshold=0.9)
npp4 = PrintProtocol(n4)
n4.inject_protocol([ngp4, ndp4, nsp4])

n1.install(s)
n2.install(s)
n3.install(s)
n4.install(s)

n2.route = [[n1], [n3, n4]]
n3.route = [[n1, n2], [n4]]
n1.allow_distillation = [n3, n2]
n2.allow_distillation = [n3]
n4.allow_distillation = [n2, n3]

c1 = QuantumChannel(nodes=[n1, n2], name="c1")
cgp1 = GenerationProtocal(c1, rate=20, possible=0.8, fidelity=0.93)
c1.inject_protocol(cgp1)
c1.install(s)

c2 = QuantumChannel(nodes=[n2, n3], name="c2")
cgp2 = GenerationProtocal(c2, rate=10, possible=0.8, fidelity=0.93)
c2.inject_protocol(cgp2)
c2.install(s)

c3 = QuantumChannel(nodes=[n3, n4], name="c3")
cgp3 = GenerationProtocal(c3, rate=20, possible=0.8, fidelity=0.93)
c3.inject_protocol(cgp3)
c3.install(s)

a = time.time()
print(a)
s.run()
b = time.time()
print(b)

de = []
for e in n4.registers:
    if n1 in e.nodes:
        de.append(e)

log.info("final distributed: {}: {}", len(de), de)
log.info(f"runtime {b - a}, {s.total_events} events, sim_time {s.end_time - s.start_time}")
