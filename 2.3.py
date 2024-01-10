import subprocess
import beepy
from dataclasses import dataclass
import time
from deepdiff import DeepDiff

@dataclass
class ArpRecord():
    ip: str
    mac: str
    interface: str

def get_arp_table() -> list():
    arp_cmd = ["cat", "/proc/net/arp"]
    proc = subprocess.Popen(arp_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (arp_cache, arp_err) = proc.communicate()

    ret_arp_table = list()

    arp_entries = arp_cache.decode().split("\n")
    for entry in arp_entries.copy():
        if entry and not entry.startswith("IP address"):
            split_entry = entry.split()
            ret_arp_table.append(ArpRecord(ip=split_entry[0], mac=split_entry[3], interface=split_entry[5]))

    return ret_arp_table

def main():
    arp_table = get_arp_table()
    while True:
        new_arp_table = get_arp_table()
        print(new_arp_table)
        diff = DeepDiff(arp_table, new_arp_table)
        if diff:
            print(diff)
            beepy.beep()

        arp_table = new_arp_table
        time.sleep(1)

if __name__ == "__main__":
    main()
