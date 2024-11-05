Movie Time Graph Analysis


Overview


This application visualizes movie data relative to the time it was captured using Python's Matplotlib and Tkinter libraries. The application displays movie frames, allows users to draw rectangles on the frames, and calculates the relative intensity of those regions over time.

Features


Visualizes movie data captured with a 12-bit camera (value range: 0-4095).


Users can draw rectangles to select regions of interest on movie frames.

Relative intensity calculations are displayed on a separate plot.

Up to 9 rectangles can be plotted simultaneously, with color differentiation.

The option to reset all drawn rectangles and their corresponding intensity plots.

Requirements

Python 3.x
Libraries: numpy, matplotlib, tkinter

To install required libraries, use:

bash

Copy code


pip install numpy matplotlib


Getting Started

Prepare the Environment


Ensure movie.npy and time.npy are in the same directory as illumiongui.py.
Run the Application

Open a terminal and navigate to the directory containing the files.


Run the application:


bash
Copy code


python illumiongui.py


Using the Application

Upon opening, you will see the movie image on the left and the unplotted intensity graph on the right.


Use the slider at the bottom to navigate through the movie frames.


Click on the Draw Rectangle button to enable drawing mode (cursor will change to a crosshair).


Click and drag on the movie image to create a rectangle. The relative intensity for that region will be plotted to the right.


To reset the rectangles and the intensity graph, click the Reset Rectangles button.



Testing
Functional Tests

Verify that rectangles can be drawn and that the correct relative intensity is calculated for the selected area.


Ensure the reset functionality works correctly and that all rectangles and graphs are cleared.


Edge Cases


Test with frames that have no intensity (e.g., all zero values) to ensure that the application handles these gracefully. Passed


Test the maximum rectangle limit (9) and attempt to exceed it by drawing additional rectangles. Passed


Design Choices


The application is designed for ease of use, with intuitive controls for drawing and resetting rectangles.


Rectangles are color-coded to differentiate intensity plots, improving visual clarity.


Future extensibility can include:
Exporting intensity data to a file.


Adding more advanced analysis features, such as statistical summaries of selected regions.


Support for more file formats and data visualization types.


Limitations


The current implementation assumes that the input data is correctly formatted and does not include error handling for incorrect data formats.


The application currently supports only one movie at a time.



License
This project is open-source and available under the MIT License.