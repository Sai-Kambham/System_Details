import time
import psutil
import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

p2=psutil.Process()
startTime=time.time()

class LCFS:
    def running_time(self):
        print("Running Time for Last In First Out :",time.time()-startTime)

    def processData(self):
        f = open('data.json')
        # returns JSON object as a dictionary
        p_data = json.load(f)
        process_data = []
        for i in p_data['input_data']:
            process_data.append([i['Process_ID'], i['Arrival_Time'], i['Burst_Time']])
        f.close()
        LCFS.schedulingProcess(self, process_data)

    def schedulingProcess(self, process_data):
        process_data.sort(key=lambda x: x[1],reverse=True)
        start_time = []
        exit_time = []
        s_time = 0
        for i in range(len(process_data)):
            if s_time < process_data[i][1]:
                s_time = process_data[i][1]
            start_time.append(s_time)
            s_time = s_time + process_data[i][2]
            e_time = s_time
            exit_time.append(e_time)
            process_data[i].append(e_time)
        t_time = LCFS.calculateTurnaroundTime(self, process_data)
        w_time = LCFS.calculateWaitingTime(self, process_data)
        LCFS.printData(self, process_data, t_time, w_time)

    def calculateTurnaroundTime(self, process_data):
        total_turnaround_time = 0
        for i in range(len(process_data)):
            turnaround_time = process_data[i][3] - process_data[i][1]
            total_turnaround_time = total_turnaround_time + turnaround_time
            process_data[i].append(turnaround_time)
        average_turnaround_time = total_turnaround_time / len(process_data)
        return average_turnaround_time

    def calculateWaitingTime(self, process_data):
        total_waiting_time = 0
        for i in range(len(process_data)):
            waiting_time = process_data[i][4] - process_data[i][2]
            total_waiting_time = total_waiting_time + waiting_time
            process_data[i].append(waiting_time)
        average_waiting_time = total_waiting_time / len(process_data)
        return average_waiting_time

    def printData(self, process_data, average_turnaround_time, average_waiting_time):
        print(f'Average Turnaround Time: {average_turnaround_time}')
        print(f'Average Waiting Time: {average_waiting_time}')

    def statistics_LCFS_list(self):
        CPU_Usage = psutil.cpu_percent(2) / psutil.cpu_count()
        Memory_Usage = ((p2.memory_info().rss) / 1024 ** 3)
        Virtual_Memory_Usage = psutil.virtual_memory()[2]
        io_counters = p2.io_counters()
        disk_usage_process = io_counters[2] + io_counters[3]  # read_bytes + write_bytes
        disk_io_counter = psutil.disk_io_counters()
        disk_total = disk_io_counter[2] + disk_io_counter[3]
        Hard_drive_Usage = ((disk_usage_process / disk_total) * 100)
        RSS = p2.memory_info()[0]
        VMS = p2.memory_info()[1]
        Page_Faults = p2.memory_info()[2]
        stt_values = [CPU_Usage, Memory_Usage, Virtual_Memory_Usage, Hard_drive_Usage, RSS, VMS, Page_Faults]
        return stt_values

    def Visualization(self):
        p_lifo = []
        p_lifo.extend(lcfs.statistics_LCFS_list())
        x = ["CPU_Usage", "Memory_usage", "Disk_Usage"]
        values = [p_lifo[0], p_lifo[2], p_lifo[3]]
        bar1 = np.arange(len(x))
        plt.bar(bar1, values, 0.5, label="x")
        plt.title("LIFO")
        plt.xticks(bar1, x)
        plt.savefig("p1.LIFO.png")

if __name__ == "__main__":
    lcfs = LCFS()
    lcfs.processData()
    p = []
    p.extend(lcfs.statistics_LCFS_list())
    y = {'CPU_Usage': [p[0]], 'Memory_Used_in_GB': [p[1]], 'Virtual_Memory_USage': [p[2]], 'HardDrive_Usage': [p[3]],'RSS': [p[4]], 'VMS': [p[5]], 'Page Faults': [p[6]]}
    df = pd.DataFrame(y)
    print(df.to_string())
    lcfs.running_time()
    lcfs.Visualization()