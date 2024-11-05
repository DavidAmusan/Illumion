#import libraries
import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#movie and time data
movie = np.time = np.load('time.npy')
load('movie.npy')

#Tkinter window
root = tk.Tk()
root.title("Movie Time Graph Analysis")
root.geometry("1400x450")  

#Main Frame
main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)

#frame for the movie plot
frame_plot = tk.Frame(main_frame)
frame_plot.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

#frame for the intensity plot
frame_intensity = tk.Frame(main_frame)
frame_intensity.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

#plot for the movie
fig, ax = plt.subplots()
frames = movie[0]
frame_plot_image = ax.imshow(frames, cmap='gray', vmin=0, vmax=4095)
ax.set_title("12-bit Movie by the Second")

#create a canvas for the movie plot
canvas_plot = FigureCanvasTkAgg(fig, master=frame_plot)
canvas_plot.get_tk_widget().pack(fill=tk.BOTH, expand=True)

#rectangle drawing
rectangles = []
rect = None
start_x = None
start_y = None
drawing_mode = False  
rect_color = ['red', 'green', 'blue', 'orange', 'purple', 'indigo', 'tan', 'grey', 'peach']  
color_index = 0  

#plot for relative intensity
fig_intensity, ax_intensity = plt.subplots(figsize=(5, 4))
ax_intensity.set_title("Relative Intensity")
ax_intensity.set_xlabel("Time (s)")
ax_intensity.set_ylabel("Relative Intensity")

#canvas for the intensity plot
canvas_intensity = FigureCanvasTkAgg(fig_intensity, master=frame_intensity)
canvas_intensity.get_tk_widget().pack(fill=tk.BOTH, expand=True)

#time format for intensity plot
def format_time(seconds):
    return f"{int(seconds // 3600):02}:{int((seconds % 3600) // 60):02}:{int(seconds % 60):02}"

#function to update movie frame based on slider
def frameByTime(val):
    second = int(slider.get())
    frame_plot_image.set_data(movie[second])
    ax.set_title(f"12-bit Movie Analysis")
    canvas_plot.draw()

#function to toggle drawing mode
def toggle_drawing():
    global drawing_mode
    drawing_mode = not drawing_mode  
    if drawing_mode:
        root.config(cursor="crosshair")  
    else:
        root.config(cursor="")  
        if rect is not None:
            ax.patches.remove(rect)  
            rect = None
        canvas_plot.draw()

#mouse event handlers for rectangle drawing
def on_button_press(event):
    global start_x, start_y, rect, drawing_mode
    if drawing_mode and event.xdata is not None and event.ydata is not None:
        start_x = event.xdata  
        start_y = event.ydata  
        global color_index
        rect = plt.Rectangle((start_x, start_y), 0, 0, edgecolor=rect_color[color_index], fill=False)
        ax.add_patch(rect) 
        rectangles.append(rect)  


def on_mouse_drag(event):
    global rect, drawing_mode
    if drawing_mode and rect is not None and event.xdata is not None and event.ydata is not None:
        width = event.xdata - start_x
        height = event.ydata - start_y
        rect.set_width(width)
        rect.set_height(height)
        canvas_plot.draw()

def on_button_release(event):
    global rect, drawing_mode, color_index
    if drawing_mode and rect is not None:
        x0, y0 = int(start_x), int(start_y)
        x1, y1 = int(event.xdata), int(event.ydata)

        mean_intensities = []
        for frame in movie:
            mean_intensity = np.mean(frame[y0:y1, x0:x1])
            mean_intensities.append(mean_intensity)

        mean_intensities = np.array(mean_intensities)
        relative_intensities = (mean_intensities / mean_intensities[0]) * 100

        ax_intensity.set_title("Relative Intensity")
        ax_intensity.set_xlabel("Time(s)")
        ax_intensity.set_ylabel("Relative Intensity (%)")
        

        ax_intensity.plot(time, relative_intensities, color=rect_color[color_index], label=f'Rectangle {color_index + 1}')

        ax_intensity.legend()
        canvas_intensity.draw()

        color_index = (color_index + 1) % len(rect_color)

        rect = None  

#reset rectangles
def reset_rectangles():
    global rectangles, drawing_mode, color_index
    drawing_mode = False
    color_index = 0 

    for rect in rectangles:
        ax.patches.remove(rect)  
    rectangles.clear() 
    
    ax_intensity.cla()  
    ax_intensity.set_title("Relative Intensity")
    ax_intensity.set_xlabel("Time (s)")
    ax_intensity.set_ylabel("Relative Intensity (%)")
    canvas_intensity.draw() 
    canvas_plot.draw()
    root.config(cursor="")  # Reset the cursor when rectangles are reset

canvas_plot.mpl_connect("button_press_event", on_button_press)
canvas_plot.mpl_connect("motion_notify_event", on_mouse_drag)
canvas_plot.mpl_connect("button_release_event", on_button_release)

#slider for movie frames
slider = tk.Scale(root, from_=0, to=len(time) - 1, orient=tk.HORIZONTAL, command=frameByTime)
slider.pack(side=tk.BOTTOM, fill=tk.X)

#button frame 
button_frame = tk.Frame(root)
button_frame.pack(side=tk.BOTTOM, pady=(10, 0))

#button to toggle rectangle drawing mode
draw_button = tk.Button(button_frame, text="Draw Rectangle", command=toggle_drawing)
draw_button.pack(side=tk.LEFT, pady=10)

#button to diable rectangle drawing mode
disable_button = tk.Button(button_frame, text="Reset Rectangles", command=reset_rectangles)
disable_button.pack(side=tk.RIGHT, pady=10)

#start the Tkinter main event loop
root.mainloop()