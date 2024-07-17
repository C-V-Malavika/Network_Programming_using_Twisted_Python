import json
import heapq
from twisted.internet import reactor, protocol, task

class OSPFProtocol(protocol.DatagramProtocol):

    def __init__(self, router_id, neighbors):

        self.router_id = router_id
        self.neighbors = neighbors
        self.link_state_db = {router_id: neighbors}
        self.sequence_number = 0
        self.received_lsas = set()
        self.lsa_cooldown = {}


    def startProtocol(self):

        self.transport.joinGroup("224.0.0.9")
        self.send_lsa()
        task.LoopingCall(self.send_lsa).start(10.0)
        task.LoopingCall(self.cleanup_cooldown).start(60.0)


    def send_lsa(self):

        lsa = {
            "router_id": self.router_id,
            "neighbors": self.neighbors,
            "sequence_number": self.sequence_number
        }
        self.sequence_number += 1
        self.transport.write(json.dumps(lsa).encode('utf-8'), ("224.0.0.9", 9999))


    def datagramReceived(self, datagram, address):

        lsa = json.loads(datagram.decode('utf-8'))
        lsa_id = (lsa["router_id"], lsa["sequence_number"])

        if lsa_id not in self.received_lsas:
            self.received_lsas.add(lsa_id)
            self.link_state_db[lsa["router_id"]] = lsa["neighbors"]

            # Propagate the LSA if it's new
            if lsa["router_id"] not in self.lsa_cooldown:
                self.send_lsa()
                self.lsa_cooldown[lsa["router_id"]] = reactor.seconds()
                self.compute_shortest_paths()


    def cleanup_cooldown(self):

        current_time = reactor.seconds()
        cooldown_period = 30  # 30 seconds cooldown
        self.lsa_cooldown = {router_id: timestamp for router_id, timestamp in self.lsa_cooldown.items() if current_time - timestamp < cooldown_period}


    def compute_shortest_paths(self):

        # Initialize distances with all routers in the link_state_db
        graph = self.link_state_db
        distances = {router: float('inf') for router in graph}
        distances[self.router_id] = 0
        pq = [(0, self.router_id)]

        while pq:
            current_distance, current_router = heapq.heappop(pq)

            if current_distance > distances[current_router]:
                continue

            for neighbor, weight in graph.get(current_router, {}).items():
                # Ensure the neighbor is in the distances dictionary
                if neighbor not in distances:
                    distances[neighbor] = float('inf')

                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(pq, (distance, neighbor))

        print(f"Shortest paths from router {self.router_id}: {distances}")


if __name__ == '__main__':

    router_id = "A"
    neighbors = {"B": 2, "C": 5}

    protocol = OSPFProtocol(router_id, neighbors)
    reactor.listenMulticast(9999, protocol, listenMultiple = True)
    reactor.run()