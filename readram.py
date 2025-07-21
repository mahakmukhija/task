import psutil
import os

def bytes_to_human(n):
    """Convert bytes to a human-readable string (KB, MB, GB)."""
    symbols = ('B', 'KB', 'MB', 'GB', 'TB', 'PB')
    prefix = 1024.0
    for sym in symbols:
        if n < prefix:
            return f"{n:.2f} {sym}"
        n /= prefix
    return f"{n:.2f} PB"

def get_system_memory():
    mem = psutil.virtual_memory()
    return {
        "Total": bytes_to_human(mem.total),
        "Available": bytes_to_human(mem.available),
        "Used": bytes_to_human(mem.used),
        "Free": bytes_to_human(mem.free),
        "Usage (%)": f"{mem.percent}%",
    }

def get_process_memory():
    proc = psutil.Process(os.getpid())
    mem_info = proc.memory_info()
    return {
        "RSS (Resident Memory)": bytes_to_human(mem_info.rss),
        "VMS (Virtual Memory)": bytes_to_human(mem_info.vms),
    }

def main():
    print("🔄 System Memory Usage:")
    for k, v in get_system_memory().items():
        print(f"  {k}: {v}")

    print("\n🧠 Current Process Memory Usage:")
    for k, v in get_process_memory().items():
        print(f"  {k}: {v}")

if __name__ == "__main__":
    main()
