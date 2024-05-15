import psutil

def get_disk_space():
    partitions = psutil.disk_partitions()
    for partition in partitions:
        if 'cdrom' in partition.opts or partition.fstype == '':
            continue
        usage = psutil.disk_usage(partition.mountpoint)
        print(f"Drive: {partition.device} ({partition.mountpoint}) - Total: {usage.total / (1024 * 1024 * 1024):.2f} GB, Used: {usage.used / (1024 * 1024 * 1024):.2f} GB, Free: {usage.free / (1024 * 1024 * 1024):.2f} GB, Percent: {usage.percent}%")

if __name__ == "__main__":
    get_disk_space()
