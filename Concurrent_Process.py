import psutil
import time
import Multi_Process
import multiprocessing
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

p = psutil.Process()
startTime = time.time()
C_Pro = Multi_Process.Multi_Process()
class Concurrent_Process:
    def running_time(self):
        print("Running Time for both the algorithms running concurrently:",time.time()-startTime)
    def combined_statistics(self):
        CPU_Usage = psutil.cpu_percent(2) / psutil.cpu_count()
        Memory_Usage = ((p.memory_info().rss) / 1024 ** 3)
        Virtual_Memory_Usage = psutil.virtual_memory()[2]
        io_counters = p.io_counters()
        disk_usage_process = io_counters[2] + io_counters[3]  # read_bytes + write_bytes
        disk_io_counter = psutil.disk_io_counters()
        disk_total = disk_io_counter[2] + disk_io_counter[3]
        Hard_drive_Usage = ((disk_usage_process / disk_total) * 100)
        RSS = p.memory_info()[0]
        VMS = p.memory_info()[1]
        Page_Faults = p.memory_info()[2]
        stt_values = [CPU_Usage, Memory_Usage, Virtual_Memory_Usage, Hard_drive_Usage, RSS, VMS, Page_Faults]
        return stt_values

    def Visualization(self):
        p_Conc = []
        p_Conc.extend(Combined_Pro.combined_statistics())
        x = ["CPU_Usage", "Memory_usage", "Disk_Usage"]
        values = [p_Conc[0], p_Conc[2], p_Conc[3]]
        bar1 = np.arange(len(x))
        plt.bar(bar1, values, 0.5, label="x")
        plt.title("FIFO and LIFO")
        plt.xticks(bar1, x)
        plt.savefig("p.Conc.png")

if __name__ == "__main__":
    Combined_Pro=Concurrent_Process()
    Combined_proc = multiprocessing.Process(target=C_Pro.Concurrent_Processing)
    Combined_proc.start()
    Combined_proc.join()
    pf = []
    pf.extend(Combined_Pro.combined_statistics())
    y = {'CPU_Usage': [pf[0]], 'Memory_Used_in_GB': [pf[1]], 'Virtual_Memory_USage': [pf[2]], 'HardDrive_Usage': [pf[3]],'RSS': [pf[4]], 'VMS': [pf[5]], 'Page Faults': [pf[6]]}
    df = pd.DataFrame(y)
    print(df.to_string())
    Combined_Pro.Visualization()
    Combined_Pro.running_time()
