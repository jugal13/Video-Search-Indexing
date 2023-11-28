import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QLabel, QFileDialog
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import QUrl


class VideoPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Video Player")
        self.setGeometry(100, 100, 800, 600)

        self.file_name = ""

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.video_widget = QVideoWidget()

        self.select_video_button = QPushButton("Select Video")
        self.play_button = QPushButton("Play")
        self.pause_button = QPushButton("Pause")
        self.stop_button = QPushButton("Stop")
        self.resume_button = QPushButton("Resume")

        self.file_label = QLabel("No file selected")

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.video_widget)
        self.layout.addWidget(self.file_label)
        self.layout.addWidget(self.select_video_button)
        self.layout.addWidget(self.play_button)
        self.layout.addWidget(self.pause_button)
        self.layout.addWidget(self.resume_button)
        self.layout.addWidget(self.stop_button)

        self.central_widget.setLayout(self.layout)

        self.media_player.setVideoOutput(self.video_widget)

        self.select_video_button.clicked.connect(self.select_video)
        self.play_button.clicked.connect(self.play_video)
        self.pause_button.clicked.connect(self.pause_video)
        self.resume_button.clicked.connect(self.resume_video)
        self.stop_button.clicked.connect(self.stop_video)
        self.media_player.mediaStatusChanged.connect(self.statusChanged)

    def select_video(self):
        self.file_name, _ = QFileDialog.getOpenFileName(self, "Open Video")
        self.media_player.setMedia(
            QMediaContent(
                QUrl.fromLocalFile(self.file_name)
            )
        )
        self.file_label.setText(f"Selected: {self.file_name}")

    def play_video(self):
        if self.file_name != '':
            self.media_player.play()

    def pause_video(self):
        self.media_player.pause()

    def resume_video(self):
        self.media_player.play()

    def stop_video(self):
        self.media_player.stop()

    def statusChanged(self, status):
        if status == QMediaPlayer.LoadedMedia:
            self.media_player.setPosition(5000)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VideoPlayer()
    window.show()
    sys.exit(app.exec())
