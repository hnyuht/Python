import os
import psutil

def get_disk_space():
    output_dir = r'C:\temp\xdr'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    output_file = os.path.join(output_dir, 'disk_space.txt')
    with open(output_file, 'w') as f:
        partitions = psutil.disk_partitions()
        for partition in partitions:
            if 'cdrom' in partition.opts or partition.fstype == '':
                continue
            usage = psutil.disk_usage(partition.mountpoint)
            f.write(f"Drive: {partition.device} ({partition.mountpoint}) - Total: {usage.total / (1024 * 1024 * 1024):.2f} GB, Used: {usage.used / (1024 * 1024 * 1024):.2f} GB, Free: {usage.free / (1024 * 1024 * 1024):.2f} GB, Percent: {usage.percent}%\n")

if __name__ == "__main__":
    get_disk_space()
