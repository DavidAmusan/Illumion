import matplotlib.pyplot as plt

class Rois:
    def __init__(self, start_x, start_y, ax):
        self.start_x= start_x
        self.start_y= start_y
        self.ax= ax
        self.rectangle = []
        rect = None
        rect_color = ['red', 'green', 'blue', 'orange', 'purple', 'indigo', 'tan', 'grey', 'peach']
        color_index = 0 

    def start_draw(self, xdata, ydata):
        self.rect = plt.Rectangle((xdata, ydata), 0, 0, edgecolor=self.rect_color[self.color_index], fill=False)
        
        self.ax.add_patch(self.rect) 
        self.rectangles.append(self.rect) 

    def now_drawing(self, xdata, ydata,):
        width = xdata - self.start_x
        height = ydata - self.start_y
        self.rect.set_width(width)
        self.rect.set_height(height)

    def reset_rectangles(self):

        for rect in self.rectangles:
            self.ax.patches.remove(rect)  
            self.rectangles.clear() 
                    
            self.ax_intensity.cla()  
            self.ax_intensity.set_title("Relative Intensity")
            self.ax_intensity.set_xlabel("Time (s)")
            self.ax_intensity.set_ylabel("Relative Intensity (%)")
            self.canvas_intensity.draw() 
            self.canvas_plot.draw()
            self.config(cursor="")  # Reset the cursor when rectangles are reset        

