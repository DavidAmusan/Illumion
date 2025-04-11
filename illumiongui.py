#import libraries
import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from roi_class import Rois
import threading 
from caclulateintensity import calculateintensity
import concurrent.futures

#movie and time data
time = np.load('time.npy')
movie = np.load('movie.npy')

class Main(tk.tk):
    def __init__(self):
        super().__init__()

        self.title("Movie Time Graph Analysis")
        self.geometry("1400x450")  

        #Main Frame
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        #frame for the movie plot
        self.frame_plot = tk.Frame(self.main_frame)
        self.frame_plot.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        #frame for the intensity plot
        self.frame_intensity = tk.Frame(self.main_frame)
        self.frame_intensity.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        #plot for the movie
        self.fig, self.ax = plt.subplots()
        self.frames = movie[0]
        self.frame_plot_image = self.ax.imshow(self.frames, cmap='gray', vmin=0, vmax=4095)
        self.ax.set_title("12-bit Movie by the Second")

        #create a canvas for the movie plot
        self.canvas_plot = FigureCanvasTkAgg(self.fig, master=self.frame_plot)
        self.canvas_plot.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.start_x = None
        self.start_y = None
        self.drawing_mode = False  

        self.fig_intensity, self.ax_intensity = plt.subplots(figsize=(5, 4))
        self.ax_intensity.set_title("Relative Intensity")
        self.ax_intensity.set_xlabel("Time (s)")
        self.ax_intensity.set_ylabel("Relative Intensity")

        #canvas for the intensity plot
        self.canvas_intensity = FigureCanvasTkAgg(self.fig_intensity, master=self.frame_intensity)
        self.canvas_intensity.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.canvas_plot.mpl_connect("button_press_event", self.on_button_press)
        self.canvas_plot.mpl_connect("motion_notify_event", self.on_mouse_drag)
        self.canvas_plot.mpl_connect("button_release_event", self.on_button_release)

                #slider for movie frames
        self.slider = tk.Scale(self, from_=0, to=len(time) - 1, orient=tk.HORIZONTAL, command=self.frameByTime)
        self.slider.pack(side=tk.BOTTOM, fill=tk.X)

                #button frame 
        self.button_frame = tk.Frame(self)
        self.button_frame.pack(side=tk.BOTTOM, pady=(10, 0))

                #button to toggle rectangle drawing mode
        self.raw_button = tk.Button(self.button_frame, text="Draw Rectangle", command=self.toggle_drawing)
        self.draw_button.pack(side=tk.LEFT, pady=10)

                #button to diable rectangle drawing mode
        self.disable_button = tk.Button(self.button_frame, text="Reset Rectangles", command=self.reset_rectangles)
        self.disable_button.pack(side=tk.RIGHT, pady=10)
        
        self.rois = Rois(self.start_x, self.start_y, self.ax)
    
    def format_time(seconds):
        return f"{int(seconds // 3600):02}:{int((seconds % 3600) // 60):02}:{int(seconds % 60):02}"

#function to update movie frame based on slider
    def frameByTime(self, val):
        second = int(self.slider.get())
        self.frame_plot_image.set_data(movie[second])
        self.ax.set_title(f"12-bit Movie Analysis")
        self.canvas_plot.draw()

        #function to toggle drawing mode
    def toggle_drawing(self):
        if self.drawing_mode:
            self.config(cursor="crosshair")  
        else:
            self.config(cursor="")  
        
        self.drawing_mode = not self.drawing_mode  
    
    def now_drawing(self, event):
        self.rois.now_drawing(event.xdata, event.ydata)
        self.canvas_plot.draw()

    def on_button_press(self, event):
        self.roi_executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
        start_future = self.roi_executor.submit(self.rois.start_draw, event.xdata, event.ydata)

    def calculate_intensity_and_plot(self, event):
        self.calculateintensity = calculateintensity(self.start_x, self.start_y)
        
        self.mean_intensities.append(self.calculateintensity.calculate(event))

    def on_mouse_drag(self,event):
            if self.drawing_mode and event.xdata is not None and event.ydata is not None:
                now_drawing = self.roi_executor.submit(self.now_drawing, event)
                
    def on_button_release(self, event):
                    if  self.drawing_mode is not None:

                        calculatethread = threading.Thread(target=self.calculate_intensity_and_plot, args=(event))
                        calculatethread.start()

                        self.ax_intensity.set_title("Relative Intensity")
                        self.ax_intensity.set_xlabel("Time(s)")
                        self.ax_intensity.set_ylabel("Relative Intensity (%)")
                        
                        relative_intensities = (self.mean_intensities / self.mean_intensities[0]) * 100

                        self.ax_intensity.plot(time, relative_intensities, color=self.rect_color[self.color_index], label=f'Rectangle {self.color_index + 1}')

                        self.ax_intensity.legend()
                        self.canvas_intensity.draw()

                        self.color_index = (self.color_index + 1) % len(self.rect_color)

                        self.rect = None  

                #reset rectangles
    def reset_rectangles(self):
        self.rois.reset_rectangles()
        self.drawing_mode = False

                #start the Tkinter main event loop
if __name__ == "__main__":
    from analysis.experiment import load_experiment
    experiment = load_experiment(PATH)
    roi = Main()  # Create an instance of the MainApplication
    roi.mainloop()  # Start the Tkinter event loop to display the GUI
