import tkinter as tk
from tkinter import ttk, messagebox

def priority(process_list):
    gantt = []
    t = 0
    completed = {}
    while process_list != []:
        available = [p for p in process_list if p[3] <= t]
        
        if not available:
            gantt.append("Idle")
            t += 1
            continue

        available.sort()  # Sort by priority (first element)
        process = available[0]
        process_list.remove(process)
        pid = process[1]
        burst_time = process[2]
        arrival_time = process[3]
        t += burst_time
        ct = t
        tt = ct - arrival_time
        wt = tt - burst_time
        completed[pid] = [ct, tt, wt]
        gantt.extend([pid] * burst_time)

    return gantt, completed

# GUI Part
class CPUSchedulerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Priority CPU Scheduling (Non-preemptive)")
        self.geometry("700x500")

        self.process_list = [
            [5, "p1", 6, 2],
            [4, "p2", 2, 5],
            [1, "p3", 8, 1],
            [2, "p4", 3, 0],
            [3, "p5", 4, 4]
        ]

        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self, text="Processes: [Priority, PID, Burst Time, Arrival Time]", font=('Arial', 12))
        self.label.pack(pady=10)

        self.text = tk.Text(self, height=5, width=80)
        self.text.insert(tk.END, str(self.process_list))
        self.text.pack()

        self.run_button = tk.Button(self, text="Run Scheduler", command=self.run_scheduler)
        self.run_button.pack(pady=10)

        self.gantt_label = tk.Label(self, text="Gantt Chart:", font=('Arial', 12, 'bold'))
        self.gantt_label.pack()

        self.gantt_chart = tk.Text(self, height=2, width=80, bg="#f0f0f0")
        self.gantt_chart.pack()

        self.result_label = tk.Label(self, text="Completion Time, Turnaround Time, Waiting Time", font=('Arial', 12, 'bold'))
        self.result_label.pack(pady=5)

        self.result_table = tk.Text(self, height=10, width=80, bg="#f0f0f0")
        self.result_table.pack()

    def run_scheduler(self):
        try:
            process_list = eval(self.text.get("1.0", tk.END))
            gantt, completed = priority(process_list)

            self.gantt_chart.delete("1.0", tk.END)
            self.gantt_chart.insert(tk.END, ' | '.join(gantt))

            self.result_table.delete("1.0", tk.END)
            for pid, (ct, tt, wt) in completed.items():
                self.result_table.insert(tk.END, f"{pid}: CT={ct}, TT={tt}, WT={wt}\n")
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    app = CPUSchedulerApp()
    app.mainloop()
