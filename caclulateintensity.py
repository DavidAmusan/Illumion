import numpy as np

class calculateintensity:
    def __init__(self, movie, start_x, start_y):
        self.movie = movie
        self.start_x = start_x
        self.start_y = start_y


    def calculate(self, event): 
        x0, y0 = int(self.start_x), int(self.start_y)
        x1, y1 = int(event.xdata), int(event.ydata)
        mean_intensities = []
        for frame in self.movie:
            mean_intensity = np.mean(frame[y0:y1, x0:x1])
            mean_intensities.append(mean_intensity)

        mean_intensities = np.array(mean_intensities)
        relative_intensities = (mean_intensities / mean_intensities[0]) * 100
        
        return relative_intensities