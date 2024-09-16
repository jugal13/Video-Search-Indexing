import cv2
import tkinter as tk
from tkinter import filedialog

class VideoPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Video Player")
        self.video_path = ""

        self.canvas = tk.Canvas(root, width=640, height=480)
        self.canvas.pack()

        self.choose_file_button = tk.Button(root, text="Choose Video", command=self.choose_file)
        self.choose_file_button.pack(pady=10)

        self.play_button = tk.Button(root, text="Play", command=self.play_video)
        self.play_button.pack(pady=5)

        self.pause_button = tk.Button(root, text="Pause", command=self.pause_video)
        self.pause_button.pack(pady=5)
        self.pause_button.config(state=tk.DISABLED)

        self.stop_button = tk.Button(root, text="Stop", command=self.stop_video)
        self.stop_button.pack(pady=5)
        self.stop_button.config(state=tk.DISABLED)

    def choose_file(self):
        self.video_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4*.avi")])

    def play_video(self):
        if self.video_path:
            self.cap = cv2.VideoCapture(self.video_path)
            self.play_button.config(state=tk.DISABLED)
            self.pause_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.NORMAL)
            self.play()

    def play(self):
        ret, frame = self.cap.read()
        if ret:
            self.frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.photo = cv2.resize(self.frame, (640, 480))
            self.photo = tk.PhotoImage(data=self.photo.tobytes())
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
            self.root.after(30, self.play)
        else:
            self.cap.release()
            self.play_button.config(state=tk.NORMAL)
            self.pause_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.DISABLED)

    def pause_video(self):
        self.cap.release()
        self.play_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.DISABLED)

    def stop_video(self):
        self.cap.release()
        self.play_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.DISABLED)
        self.canvas.delete("all")

def main():
    root = tk.Tk()
    player = VideoPlayer(root)
    root.mainloop()

if __name__ == "__main__":
    main()
