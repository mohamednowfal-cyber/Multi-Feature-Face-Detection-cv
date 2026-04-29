# 🚀 8-Step Master Algorithm

Use this structured 8-step algorithm for your project report and "Algorithm" slide in your presentation.

---

### Step 1: System Initialization
Initialize the Tkinter-based Graphical User Interface (GUI). Set up the modern dark-themed layout, including a **scrollable sidebar** for controls and a central preview panel for image visualization.

### Step 2: Image Acquisition
Use the `filedialog` module to browse and select an input image, or initiate a **Live Camera Stream** via `cv2.VideoCapture(0)`. Real-time frames are captured and treated as individual processing units.

### Step 3: Color Space Pre-processing
Convert the input image from the default **BGR** (Blue, Green, Red) color space to **Grayscale** using `cvtColor`. This reduces computational complexity for detection tasks while maintaining original color data for filtering.

### Step 4: Facial Feature Extraction
Apply the **Haar Cascade Classifier** (`haarcascade_frontalface_default.xml`) on the grayscale image to extract the $(x, y, w, h)$ coordinates of all human faces present in the frame.

### Step 5: Mode-Specific Processing (Branching)
Select and execute the specific image processing algorithm based on user interaction:
*   **Privacy Mode**: Apply Gaussian Blur to the extracted face ROIs (Region of Interest).
*   **Counting Mode**: Draw bounding boxes and overlay numerical labels using `putText`.
*   **Eye Classification Mode**: Detect ocular regions within facial ROIs to determine if eyes are "Visible" or "Not Visible".
*   **Focus Mode**: Blur the entire background layer while masking and preserving the original facial regions.

### Step 6: Artistic Filter Transformation
Execute advanced stylistic transformations:
*   **Cartoonify**: Use a **Bilateral Filter** for smoothing and **Adaptive Thresholding** for edge extraction, then combine them using bitwise operations.
*   **Vintage/Sepia**: Apply a $3 \times 3$ color transformation matrix to shift the color balance.

### Step 7: GUI State Synchronization
Update the status bar to reflect the current operation. Convert the processed NumPy array into a **PhotoImage** object using the Pillow library and refresh the main display label to show the live result.

### Step 8: Export and Persistence
Allow the user to save the processed image to the `output/` folder. Use `imwrite()` to finalize the file on disk, ensuring the high-quality result is preserved for external use.
