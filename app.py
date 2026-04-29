import cv2
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os

from modules.face_detection import detect_faces
from modules.face_blur import blur_faces
from modules.cartoonify import cartoonify
from modules.background_blur import blur_background
from modules.face_count import count_and_label_faces
from modules.filters import apply_grayscale, apply_sepia
from modules.eye_classification import classify_eyes

class FaceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Visionary Face Processor")
        self.root.geometry("1000x700")
        self.root.configure(bg="#1e1e2e")  # Dark theme background

        # State variables
        self.original_img = None
        self.processed_img = None
        self.display_img = None
        self.camera_active = False
        self.cap = None

        self.setup_ui()

    def setup_ui(self):
        # Sidebar with Scrollbar
        sidebar_container = tk.Frame(self.root, bg="#181825", width=280)
        sidebar_container.pack(side="left", fill="y")
        sidebar_container.pack_propagate(False)

        canvas = tk.Canvas(sidebar_container, bg="#181825", highlightthickness=0, width=260)
        scrollbar = tk.Scrollbar(sidebar_container, orient="vertical", command=canvas.yview)
        
        self.scrollable_frame = tk.Frame(canvas, bg="#181825")
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True, padx=(10, 0))
        scrollbar.pack(side="right", fill="y")

        # Bind mousewheel to scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Header
        title_label = tk.Label(self.scrollable_frame, text="VISIONARY", fg="#cba6f7", bg="#181825", font=("Helvetica", 18, "bold"))
        title_label.pack(pady=(20, 5))
        subtitle_label = tk.Label(self.scrollable_frame, text="Face Processor", fg="#a6adc8", bg="#181825", font=("Helvetica", 10))
        subtitle_label.pack(pady=(0, 20))

        # Button Style
        btn_style = {
            "bg": "#313244",
            "fg": "#cdd6f4",
            "activebackground": "#45475a",
            "activeforeground": "#f5e0dc",
            "font": ("Helvetica", 10, "bold"),
            "bd": 0,
            "cursor": "hand2",
            "width": 24,
            "pady": 10
        }

        def create_section_label(text):
            lbl = tk.Label(self.scrollable_frame, text=text, fg="#585b70", bg="#181825", font=("Helvetica", 9, "bold"))
            lbl.pack(pady=(15, 5), anchor="w", padx=20)
            return lbl

        # SECTION: Actions
        create_section_label("PRIMARY ACTIONS")
        self.btn_upload = tk.Button(self.scrollable_frame, text="📁 Upload Image", command=self.upload_image, **btn_style)
        self.btn_upload.config(bg="#cba6f7", fg="#11111b")
        self.btn_upload.pack(pady=5)

        self.btn_camera = tk.Button(self.scrollable_frame, text="📷 Live Camera", command=self.toggle_camera, **btn_style)
        self.btn_camera.config(bg="#a6e3a1", fg="#11111b")
        self.btn_camera.pack(pady=5)

        # SECTION: Face Tools
        create_section_label("FACE TOOLS")
        self.btn_detect = tk.Button(self.scrollable_frame, text="👤 Face Detection", command=self.apply_detection, state="disabled", **btn_style)
        self.btn_detect.pack(pady=5)

        self.btn_blur = tk.Button(self.scrollable_frame, text="🔒 Face Blur", command=self.apply_blur, state="disabled", **btn_style)
        self.btn_blur.pack(pady=5)

        self.btn_count = tk.Button(self.scrollable_frame, text="👥 Face Count", command=self.apply_face_count, state="disabled", **btn_style)
        self.btn_count.pack(pady=5)

        self.btn_bg_blur = tk.Button(self.scrollable_frame, text="✨ Background Blur", command=self.apply_background_blur, state="disabled", **btn_style)
        self.btn_bg_blur.pack(pady=5)

        self.btn_eye = tk.Button(self.scrollable_frame, text="👁️ Eye Classification", command=self.apply_eye_classification, state="disabled", **btn_style)
        self.btn_eye.pack(pady=5)

        # SECTION: Artistic Filters
        create_section_label("ARTISTIC FILTERS")
        self.btn_cartoon = tk.Button(self.scrollable_frame, text="🎨 Cartoonify", command=self.apply_cartoon, state="disabled", **btn_style)
        self.btn_cartoon.pack(pady=5)

        self.btn_gray = tk.Button(self.scrollable_frame, text="🏁 Grayscale", command=self.apply_grayscale_filter, state="disabled", **btn_style)
        self.btn_gray.pack(pady=5)

        self.btn_sepia = tk.Button(self.scrollable_frame, text="🎞️ Sepia Filter", command=self.apply_sepia_filter, state="disabled", **btn_style)
        self.btn_sepia.pack(pady=5)

        # SECTION: Export
        create_section_label("EXPORT & RESET")
        self.btn_reset = tk.Button(self.scrollable_frame, text="🔄 Reset Image", command=self.reset_image, state="disabled", **btn_style)
        self.btn_reset.pack(pady=5)

        self.btn_save = tk.Button(self.scrollable_frame, text="💾 Save Result", command=self.save_image, state="disabled", **btn_style)
        self.btn_save.pack(pady=(5, 30))

        # Main Display Area
        self.main_area = tk.Frame(self.root, bg="#1e1e2e")
        self.main_area.pack(side="right", expand=True, fill="both")

        # Container for image to add border effect
        self.img_container = tk.Frame(self.main_area, bg="#11111b", bd=2)
        self.img_container.place(relx=0.5, rely=0.5, anchor="center")

        self.image_label = tk.Label(self.img_container, text="No Image Uploaded", fg="#585b70", bg="#1e1e2e", font=("Helvetica", 14), padx=20, pady=20)
        self.image_label.pack()

        # Footer Status
        self.status_var = tk.StringVar(value="Ready")
        self.status_bar = tk.Label(self.root, textvariable=self.status_var, bd=1, relief="sunken", anchor="w", bg="#11111b", fg="#a6adc8")
        self.status_bar.pack(side="bottom", fill="x")

    def upload_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp")])
        if path:
            self.original_img = cv2.imread(path)
            if self.original_img is None:
                messagebox.showerror("Error", "Could not read the image file.")
                return
            
            self.processed_img = self.original_img.copy()
            self.show_image(self.processed_img)
            self.enable_buttons()
            self.status_var.set(f"Loaded: {os.path.basename(path)}")

    def enable_buttons(self):
        # Using a dark foreground color (#11111b) for better contrast on vibrant backgrounds
        self.btn_detect.config(state="normal", bg="#89b4fa", fg="#11111b")
        self.btn_blur.config(state="normal", bg="#f9e2af", fg="#11111b")
        self.btn_cartoon.config(state="normal", bg="#a6e3a1", fg="#11111b")
        self.btn_bg_blur.config(state="normal", bg="#cba6f7", fg="#11111b")
        self.btn_eye.config(state="normal", bg="#f5c2e7", fg="#11111b")
        self.btn_count.config(state="normal", bg="#74c7ec", fg="#11111b")
        self.btn_camera.config(state="normal", bg="#a6e3a1", fg="#11111b")
        self.btn_gray.config(state="normal", bg="#94e2d5", fg="#11111b")
        self.btn_sepia.config(state="normal", bg="#eba0ac", fg="#11111b")
        self.btn_reset.config(state="normal", bg="#fab387", fg="#11111b")
        self.btn_save.config(state="normal", bg="#f38ba8", fg="#11111b")

    def show_image(self, image):
        # Convert BGR to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Resize for display while maintaining aspect ratio
        h, w = image_rgb.shape[:2]
        max_h, max_w = 600, 700
        ratio = min(max_w/w, max_h/h)
        new_w, new_h = int(w * ratio), int(h * ratio)
        
        image_resized = cv2.resize(image_rgb, (new_w, new_h))
        
        img_pil = Image.fromarray(image_resized)
        self.display_img = ImageTk.PhotoImage(img_pil)

        self.image_label.config(image=self.display_img, text="")
        self.image_label.image = self.display_img

    def apply_detection(self):
        if self.original_img is not None:
            self.status_var.set("Detecting faces...")
            self.processed_img = detect_faces(self.original_img.copy())
            self.show_image(self.processed_img)
            self.status_var.set("Faces detected.")

    def apply_blur(self):
        if self.original_img is not None:
            self.status_var.set("Blurring faces...")
            self.processed_img = blur_faces(self.original_img.copy())
            self.show_image(self.processed_img)
            self.status_var.set("Faces blurred.")

    def apply_cartoon(self):
        if self.original_img is not None:
            self.status_var.set("Applying cartoon effect...")
            self.processed_img = cartoonify(self.original_img.copy())
            self.show_image(self.processed_img)
            self.status_var.set("Cartoon effect applied.")

    def apply_background_blur(self):
        if self.original_img is not None:
            self.status_var.set("Applying background blur...")
            self.processed_img = blur_background(self.original_img.copy())
            self.show_image(self.processed_img)
            self.status_var.set("Background blur applied.")

    def apply_eye_classification(self):
        if self.original_img is not None:
            self.status_var.set("Classifying eyes...")
            self.processed_img = classify_eyes(self.original_img.copy())
            self.show_image(self.processed_img)
            self.status_var.set("Eyes classified.")

    def apply_face_count(self):
        if self.original_img is not None:
            self.status_var.set("Counting faces...")
            self.processed_img = count_and_label_faces(self.original_img.copy())
            self.show_image(self.processed_img)
            self.status_var.set("Faces counted and labeled.")

    def apply_grayscale_filter(self):
        if self.original_img is not None:
            self.status_var.set("Applying grayscale filter...")
            self.processed_img = apply_grayscale(self.original_img.copy())
            self.show_image(self.processed_img)
            self.status_var.set("Grayscale filter applied.")

    def apply_sepia_filter(self):
        if self.original_img is not None:
            self.status_var.set("Applying sepia filter...")
            self.processed_img = apply_sepia(self.original_img.copy())
            self.show_image(self.processed_img)
            self.status_var.set("Sepia filter applied.")

    def toggle_camera(self):
        if not self.camera_active:
            self.start_camera()
        else:
            self.stop_camera()

    def start_camera(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            messagebox.showerror("Error", "Could not open camera.")
            return
        
        self.camera_active = True
        self.btn_camera.config(text="🛑 Stop Camera", bg="#f38ba8")
        self.btn_upload.config(state="disabled")
        self.status_var.set("Camera Active")
        self.update_camera_frame()

    def stop_camera(self):
        self.camera_active = False
        if self.cap:
            self.cap.release()
            self.cap = None
        self.btn_camera.config(text="📷 Live Camera", bg="#a6e3a1")
        self.btn_upload.config(state="normal")
        self.status_var.set("Camera stopped.")

    def update_camera_frame(self):
        if self.camera_active:
            ret, frame = self.cap.read()
            if ret:
                # Mirror the frame for more natural feel
                frame = cv2.flip(frame, 1)
                self.original_img = frame
                self.processed_img = frame.copy()
                self.show_image(self.processed_img)
                self.enable_buttons()
                self.root.after(10, self.update_camera_frame)
            else:
                self.stop_camera()

    def reset_image(self):
        if self.original_img is not None:
            self.processed_img = self.original_img.copy()
            self.show_image(self.processed_img)
            self.status_var.set("Image reset.")

    def save_image(self):
        if self.processed_img is not None:
            path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png")])
            if path:
                cv2.imwrite(path, self.processed_img)
                messagebox.showinfo("Success", f"Image saved to {path}")
                self.status_var.set(f"Saved to {os.path.basename(path)}")

def main():
    root = tk.Tk()
    app = FaceApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
