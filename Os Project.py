import tkinter as tk
from tkinter import ttk, messagebox

def priority(process_list):
    gantt = []
    t = 0
    completed = {}
    start_times = {}
    timeline = []  # [(pid, start_time, end_time)]

    while process_list != []:
        available = [p for p in process_list if p[3] <= t]

        if not available:
            gantt.append("Idle")
            timeline.append(("Idle", t, t+1))
            t += 1
            continue

        available.sort()  # Sort by priority (first element)
        process = available[0]
        process_list.remove(process)
        pid = process[1]
        burst_time = process[2]
        arrival_time = process[3]

        start_time = max(t, arrival_time)
        start_times[pid] = start_time

        t = start_time + burst_time
        ct = t
        tt = ct - arrival_time
        wt = tt - burst_time
        rt = start_time - arrival_time
        completed[pid] = [ct, tt, wt, rt]
        gantt.extend([pid] * burst_time)
        timeline.append((pid, start_time, t))

    return gantt, completed, timeline

class CPUSchedulerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Priority CPU Scheduling (Non-preemptive)")
        self.geometry("900x700")

        self.process_list = []

        self.create_widgets()

    def create_widgets(self):
        # Process input form
        form_frame = tk.Frame(self)
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Priority:").grid(row=0, column=0, padx=5)
        tk.Label(form_frame, text="PID:").grid(row=0, column=2, padx=5)
        tk.Label(form_frame, text="Burst:").grid(row=0, column=4, padx=5)
        tk.Label(form_frame, text="Arrival:").grid(row=0, column=6, padx=5)

        self.priority_entry = tk.Entry(form_frame, width=5)
        self.priority_entry.grid(row=0, column=1)

        self.pid_entry = tk.Entry(form_frame, width=5)
        self.pid_entry.grid(row=0, column=3)

        self.burst_entry = tk.Entry(form_frame, width=5)
        self.burst_entry.grid(row=0, column=5)

        self.arrival_entry = tk.Entry(form_frame, width=5)
        self.arrival_entry.grid(row=0, column=7)

        add_button = tk.Button(form_frame, text="Add Process", command=self.add_process)
        add_button.grid(row=0, column=8, padx=10)

        # Process list table
        self.tree = ttk.Treeview(self, columns=("Priority", "PID", "Burst", "Arrival"), show="headings", height=5)
        for col in ("Priority", "PID", "Burst", "Arrival"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=80, anchor='center')
        self.tree.pack(pady=10)

        self.run_button = tk.Button(self, text="Run Scheduler", command=self.run_scheduler)
        self.run_button.pack(pady=10)

        # Gantt chart canvas
        self.gantt_label = tk.Label(self, text="Gantt Chart:", font=('Arial', 12, 'bold'))
        self.gantt_label.pack()
        self.canvas = tk.Canvas(self, height=100, bg='white')
        self.canvas.pack(pady=10, fill='x')

        # Results
        self.result_label = tk.Label(self, text="Completion Time, Turnaround Time, Waiting Time, Response Time", font=('Arial', 12, 'bold'))
        self.result_label.pack(pady=5)

        self.result_table = tk.Text(self, height=10, width=100, bg="#f0f0f0")
        self.result_table.pack()

        self.avg_label = tk.Label(self, text="", font=('Arial', 12, 'bold'))
        self.avg_label.pack(pady=10)

    def add_process(self):
        try:
            priority = int(self.priority_entry.get())
            pid = self.pid_entry.get()
            burst = int(self.burst_entry.get())
            arrival = int(self.arrival_entry.get())

            if priority < 0 or burst <= 0 or arrival < 0 or not pid:
                raise ValueError("Invalid input values.")

            self.process_list.append([priority, pid, burst, arrival])
            self.tree.insert("", tk.END, values=(priority, pid, burst, arrival))

            # Clear entries
            self.priority_entry.delete(0, tk.END)
            self.pid_entry.delete(0, tk.END)
            self.burst_entry.delete(0, tk.END)
            self.arrival_entry.delete(0, tk.END)

        except Exception as e:
            messagebox.showerror("Input Error", str(e))

    def run_scheduler(self):
        if not self.process_list:
            messagebox.showwarning("No Processes", "Please add at least one process.")
            return

        gantt, completed, timeline = priority(list(self.process_list))  # Pass a copy

        # Draw Gantt chart
        self.canvas.delete("all")
        unit_width = 40
        x = 10
        for pid, start, end in timeline:
            color = "#%02x%02x%02x" % (hash(pid) % 256, (hash(pid)*2) % 256, (hash(pid)*3) % 256)
            self.canvas.create_rectangle(x, 20, x + (end - start) * unit_width, 60, fill=color)
            self.canvas.create_text(x + ((end - start) * unit_width) / 2, 40, text=pid)
            self.canvas.create_text(x, 70, text=str(start))
            x += (end - start) * unit_width
        self.canvas.create_text(x, 70, text=str(timeline[-1][2]))

        # Show results
        self.result_table.delete("1.0", tk.END)
        total_tt = total_wt = total_rt = 0
        n = len(completed)

        for pid, (ct, tt, wt, rt) in completed.items():
            self.result_table.insert(tk.END, f"{pid}: CT={ct}, TT={tt}, WT={wt}, RT={rt}\n")
            total_tt += tt
            total_wt += wt
            total_rt += rt

        avg_tt = total_tt / n
        avg_wt = total_wt / n
        avg_rt = total_rt / n

        self.avg_label.config(text=f"Average TT: {avg_tt:.2f} | Average WT: {avg_wt:.2f} | Average RT: {avg_rt:.2f}")

if __name__ == "__main__":
    app = CPUSchedulerApp()
    app.mainloop()
