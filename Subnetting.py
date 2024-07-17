from twisted.internet import reactor
from ipaddress import ip_network, ip_interface

def compute_number_of_hosts_and_subnets(network_id, subnet_mask, subnet_bits):

	try:
		network = ip_network(network_id + '/' + subnet_mask)
		num_hosts = network.num_addresses - 2 # Subtracting network and broadcast addresses
		subnets = list(network.subnets(new_prefix=subnet_bits))
		
		return num_hosts, subnets
	
	except ValueError as e:
		return None, None
		

def main():

	network_id = '192.168.0.0' # Example network ID
	subnet_mask = '255.255.255.0' # Example subnet mask
	subnet_bits = 27 # Number of bits to be borrowed for subnets

	num_hosts, subnets = compute_number_of_hosts_and_subnets(network_id, subnet_mask, subnet_bits)

	if num_hosts is not None and subnets is not None:

		print("Number of Hosts:", num_hosts)
		print("Subnets:")

		for subnet in subnets:
			subnet_hosts = subnet.num_addresses - 2 # Subtracting network and broadcast addresses per subnet
			print(f"- {subnet} ({subnet_hosts} hosts)")
		print("")

	else:
		print("Error occurred during computation.")


if __name__ == '__main__':
	main()