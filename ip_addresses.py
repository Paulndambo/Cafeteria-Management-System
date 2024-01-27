import ipaddress


def generate_local_ips(start_ip, end_ip):
    start = ipaddress.IPv4Address(start_ip)
    end = ipaddress.IPv4Address(end_ip)

    ip_list = [str(ip) for ip in range(int(start), int(end) + 1)]
    return ip_list

start_ip = '192.168.1.1'
end_ip = '192.168.1.10'

local_ips = generate_local_ips(start_ip, end_ip)
print(local_ips)
