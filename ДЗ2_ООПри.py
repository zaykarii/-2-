from abc import ABC, abstractmethod

class Component(ABC):
    @abstractmethod
    def print_me(self, prefix, is_last):
        pass
    
    @abstractmethod
    def clone(self):
        pass


class IPAddress(Component):
    def __init__(self, address):
        self.address = address
    
    def print_me(self, prefix, is_last):
        connector = '\\-' if is_last else '+-'
        print(f"{prefix}{connector}{self.address}")
    
    def clone(self):
        return IPAddress(self.address)


class CPU(Component):
    def __init__(self, cores, speed):
        self.cores = cores
        self.speed = speed
    
    def print_me(self, prefix, is_last):
        connector = '\\-' if is_last else '+-'
        print(f"{prefix}{connector}CPU, {self.cores} cores @ {self.speed}MHz")
    
    def clone(self):
        return CPU(self.cores, self.speed)


class Memory(Component):
    def __init__(self, size):
        self.size = size
    
    def print_me(self, prefix, is_last):
        connector = '\\-' if is_last else '+-'
        print(f"{prefix}{connector}Memory, {self.size} MiB")
    
    def clone(self):
        return Memory(self.size)


class HDD(Component):
    def __init__(self, size):
        self.size = size
        self.partitions = []
    
    def add_partition(self, number, size, purpose):
        self.partitions.append({
            'number': number,
            'size': size,
            'purpose': purpose
        })
    
    def print_me(self, prefix, is_last):
        connector = '\\-' if is_last else '+-'
        print(f"{prefix}{connector}HDD, {self.size} GiB")
        
        new_prefix = prefix + ('  ' if is_last else '| ')
        for i, part in enumerate(self.partitions):
            is_last_part = i == len(self.partitions) - 1
            part_connector = '\\-' if is_last_part else '+-'
            print(f"{new_prefix}{part_connector}[{part['number']}]: {part['size']} GiB, {part['purpose']}")
    
    def clone(self):
        new_hdd = HDD(self.size)
        for part in self.partitions:
            new_hdd.add_partition(part['number'], part['size'], part['purpose'])
        return new_hdd


class Host(Component):
    def __init__(self, name):
        self.name = name
        self.ips = []
        self.components = []
    
    def add_ip(self, ip):
        self.ips.append(IPAddress(ip))
    
    def add_component(self, component):
        self.components.append(component)
    
    def print_me(self, prefix, is_last):
        connector = '\\-' if is_last else '+-'
        print(f"{prefix}{connector}Host: {self.name}")
        
        new_prefix = prefix + ('  ' if is_last else '| ')
        
        for ip in self.ips:
            ip.print_me(new_prefix, False)
        
        for i, comp in enumerate(self.components):
            comp.print_me(new_prefix, i == len(self.components) - 1)
    
    def clone(self):
        new_host = Host(self.name)
        for ip in self.ips:
            new_host.add_ip(ip.address)
        for comp in self.components:
            new_host.add_component(comp.clone())
        return new_host


class Network:
    def __init__(self, name):
        self.name = name
        self.hosts = []
    
    def add_host(self, host):
        self.hosts.append(host)
    
    def print_network(self):
        print(f"Network: {self.name}")
        for i, host in enumerate(self.hosts):
            host.print_me("", i == len(self.hosts) - 1)
    
    def clone(self):
        new_net = Network(self.name)
        for host in self.hosts:
            new_net.add_host(host.clone())
        return new_net
    
    def find_host(self, name):
        for host in self.hosts:
            if host.name == name:
                return host
        return None