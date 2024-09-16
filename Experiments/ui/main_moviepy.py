import tkinter as tk
from tkinter import filedialog
from moviepy.editor import VideoFileClip

class VideoPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Video Player")
        self.video_path = ""
        self.video_clip = None

        self.canvas = tk.Canvas(root, width=640, height=480)
        self.canvas.pack()

        self.choose_file_button = tk.Button(root, text="Choose Video", command=self.choose_file)
        self.choose_file_button.pack(pady=10)

        self.play_button = tk.Button(root, text="Play", command=self.play_video)
        self.play_button.pack(pady=5)
        self.play_button.config(state=tk.DISABLED)

        self.pause_button = tk.Button(root, text="Pause", command=self.pause_video)
        self.pause_button.pack(pady=5)
        self.pause_button.config(state=tk.DISABLED)

        self.stop_button = tk.Button(root, text="Stop", command=self.stop_video)
        self.stop_button.pack(pady=5)
        self.stop_button.config(state=tk.DISABLED)

    def choose_file(self):
        self.video_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4 *.avi")])
        if self.video_path:
            self.play_button.config(state=tk.NORMAL)

    def play_video(self):
        if self.video_path:
            try:
                self.video_clip = VideoFileClip(self.video_path)
                self.play_button.config(state=tk.DISABLED)
                self.pause_button.config(state=tk.NORMAL)
                self.stop_button.config(state=tk.NORMAL)
                self.play()
            except Exception as e:
                print("Error:", e)

    def play(self):
        frame = self.video_clip.get_frame(self.video_clip.duration / 2)  # Get a frame from the video
        photo = tk.PhotoImage(data=frame.tobytes())
        self.canvas.create_image(0, 0, image=photo, anchor=tk.NW)
        self.root.after(30, self.play)

    def pause_video(self):
        self.play_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.DISABLED)

    def stop_video(self):
        self.video_clip.close()
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
