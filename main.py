import tkinter as tk
from tkinter import ttk, Spinbox, messagebox
from matplotlib.figure import Figure
from tkcalendar import DateEntry
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import csv
from datetime import datetime

canvas = None

def update_graph():
    global canvas 
    if canvas:
        canvas.get_tk_widget().destroy()
    
    dates = []
    values1 = []
    values2 = []
    values3 = []
    values4 = []
    values5 = []

    start_date_str = start_date_picker.get()
    end_date_str = end_date_picker.get()
    start_time_str = start_time_picker.get()
    end_time_str = end_time_picker.get()
 #   print(f"1 --- {start_time_str}  {end_time_str}")
 #  or not start_time_str or not end_time_str
    if not start_date_str or not end_date_str or not start_time_str or not end_time_str:
        print(f"All params are required")
        return     
    
    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
        start_time = datetime.strptime(start_time_str, '%H:%M:%S').time()
        end_time = datetime.strptime(end_time_str, '%H:%M:%S').time()
        #print(f"2 --- {start_time}  {end_time}")

    except ValueError:
        return

    for row in data:
        try:
            date_str = row[0]
            time_str = row[1]
            if date_str:
                date = datetime.strptime(date_str, '%Y-%m-%d')
                time = datetime.strptime(time_str, '%H:%M:%S').time()
                #  and start_time <= time <= end_time
                if start_date <= date <= end_date:
                    if start_time <= time <= end_time:
                        dates.append(date_str)
                        values1.append(int(row[3])) 
                        values2.append(int(row[5])) 
                        values3.append(int(row[7])) 
                        values4.append(int(row[9])) 
                        values5.append(int(row[11])) 
        except (ValueError, IndexError):
            continue

    fig = Figure(figsize=(10, 7.5), dpi=100)
    ax = fig.add_subplot(111)
    ax.plot(dates, values1, label='value 1')
    ax.plot(dates, values2, label='value 2')
    ax.plot(dates, values3, label='value 3')
    ax.plot(dates, values4, label='value 4')
    ax.plot(dates, values5, label='value 5')

    ax.set_xlabel('Date - Time')
    ax.set_ylabel('Value')
    ax.set_title('Statistics')
    ax.tick_params(rotation=45)
    ax.legend()

    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack()


def exit_fullscreen(event):
    if messagebox.askyesno("Exit Fullscreen", "Are you sure you want to exit fullscreen mode?"):
        window.attributes("-fullscreen", False)


filename = 'data.csv'  
data = []
with open(filename, 'r') as file:
    csv_reader = csv.reader(file, delimiter=';')
    header = next(csv_reader) 
    for row in csv_reader:
        data.append(row)

window = tk.Tk()
window.title("Graph Statistics")
window.attributes("-fullscreen", True)
window.bind("<Escape>", exit_fullscreen)

filter_container = ttk.Frame(window)
filter_container.pack(padx=15, pady=15)

filter_date_frame = ttk.LabelFrame(filter_container, text="Date Filters")
filter_date_frame.grid(row=0, column=0, padx=10, pady=10)

start_label = ttk.Label(filter_date_frame, text="Start Date:")
start_label.pack()
start_date_picker = DateEntry(filter_date_frame, date_pattern='yyyy-mm-dd')
start_date_picker.pack()

end_label = ttk.Label(filter_date_frame, text="End Date:")
end_label.pack()
end_date_picker = DateEntry(filter_date_frame, date_pattern='yyyy-mm-dd')
end_date_picker.pack()

filter_time_frame = ttk.LabelFrame(filter_container, text="Time Filters")
filter_time_frame.grid(row=0, column=1, padx=10, pady=10)

time_values = [f"{hour:02d}:00:00" for hour in range(24)]

start_time_label = ttk.Label(filter_time_frame, text="Start Time:")
start_time_label.pack()
start_time_picker = Spinbox(filter_time_frame, values=time_values)  
start_time_picker.pack()


end_time_label = ttk.Label(filter_time_frame, text="End Time:")
end_time_label.pack()
end_time_picker = Spinbox(filter_time_frame, values=time_values) 
end_time_picker.pack()


filter_button = ttk.Button(window, text="Filter", command=update_graph)
filter_button.pack()

fig = Figure(figsize=(8, 5), dpi=100)
canvas = FigureCanvasTkAgg(fig, master=window)
canvas.get_tk_widget().pack()

update_graph()

window.mainloop()
