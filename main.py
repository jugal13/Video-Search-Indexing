from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QLabel, QFileDialog
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import QUrl, Qt, QTime

import time
import pickle
import sys

from query import query_frame_diff, convertFrameToMin, convertFrameToSec

statusMessage = {
    QMediaPlayer.PausedState: "Paused",
    QMediaPlayer.PlayingState: "Playing",
    QMediaPlayer.StoppedState: "Stopped",

    QMediaPlayer.LoadingMedia: "LoadingMedia",
    QMediaPlayer.LoadedMedia: "LoadedMedia",
    QMediaPlayer.BufferingMedia: "BufferingMedia",
    QMediaPlayer.BufferedMedia: "BufferedMedia",
    QMediaPlayer.EndOfMedia: "EndOfMedia",
}

diff_pickle_path = './hash-diff-videos/combined.pkl'
diff_hash_values = pickle.load(open(diff_pickle_path, 'rb'))  # 0.4s


class VideoPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Video Player")
        self.setGeometry(100, 100, 374, 504)

        self.file_name = ""
        self.first_load = False
        self.matched_first_frame = 0

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.video_widget = QVideoWidget()

        self.select_video_button = QPushButton("Select Video")
        self.play_button = QPushButton("Play")
        self.stop_button = QPushButton("Stop")
        self.reset_frame_button = QPushButton("Reset Frame")

        self.file_label = QLabel("No file selected")
        self.file_label.setMinimumHeight(10)
        self.file_label.setMaximumHeight(20)
        self.file_label.setAlignment(Qt.AlignCenter)

        self.timer_label = QLabel("00:00/00:00")
        self.timer_label.setMinimumHeight(10)
        self.timer_label.setMaximumHeight(20)
        self.timer_label.setAlignment(Qt.AlignCenter)

        self.layout = QVBoxLayout()

        self.layout.addWidget(self.video_widget)
        self.layout.addWidget(self.timer_label)
        self.layout.addWidget(self.file_label)
        self.layout.addWidget(self.select_video_button)
        self.layout.addWidget(self.play_button)
        self.layout.addWidget(self.stop_button)
        self.layout.addWidget(self.reset_frame_button)

        self.central_widget.setLayout(self.layout)

        self.media_player.setVideoOutput(self.video_widget)

        self.select_video_button.clicked.connect(self.select_video)
        self.play_button.clicked.connect(self.play_video)
        self.stop_button.clicked.connect(self.stop_video)
        self.reset_frame_button.clicked.connect(self.reset_video)

        self.media_player.mediaStatusChanged.connect(self.mediaStatusChanged)
        self.media_player.stateChanged.connect(self.playerStatusChanged)
        self.media_player.positionChanged.connect(self.postionStatusChanged)

    def select_video(self):
        self.file_name, _ = QFileDialog.getOpenFileName(self, "Open Video")

        if not self.file_name:
            return

        start_time = time.time()
        self.matched_first_frame, matched_video_path = query_frame_diff(
            self.file_name,
            diff_hash_values
        )  # 0.003s
        end_time = time.time()

        elapsed_time = end_time - start_time
        print(f"Time taken to query: {elapsed_time} seconds")

        video_name = matched_video_path.split("/")[-1].split(".")[0]
        # TODO fix this path as absolute path to folder
        video_path = "./dataset/videos/" + \
            video_name + ".mp4"

        time_in_min = convertFrameToMin(self.matched_first_frame)
        time_in_sec = convertFrameToSec(self.matched_first_frame)

        print("Matched Video: ", video_name)
        print("Matched Frame Number: ", self.matched_first_frame)
        print("Matched Time: ", time_in_min,
              " minutes ", time_in_sec, " seconds")

        self.media_player.setMedia(
            QMediaContent(
                QUrl.fromLocalFile(video_path)
            )
        )
        self.file_label.setText(f"Selected: {video_name}.mp4")
        self.first_load = True

    def play_video(self):
        if self.media_player.state() == QMediaPlayer.PausedState:
            self.media_player.play()
            self.play_button.setText("Pause")
        elif self.media_player.state() == QMediaPlayer.PlayingState:
            self.media_player.pause()
            self.play_button.setText("Play")
        elif self.media_player.state() == QMediaPlayer.StoppedState:
            self.media_player.play()
            self.play_button.setText("Pause")

    def stop_video(self):
        self.media_player.stop()
        self.play_button.setText("Play")
        if self.media_player.state() == QMediaPlayer.StoppedState:
            duration = self.media_player.duration()
            if duration >= 0:
                total_time = QTime(
                    0,
                    (duration // 60000) % 60,
                    (duration // 1000) % 60
                )
                current_time = QTime(
                    0,
                    (0 // 60000) % 60,
                    (0 // 1000) % 60
                )
                self.timer_label.setText(
                    f"{current_time.toString('mm:ss')} / {total_time.toString('mm:ss')}")

    def reset_video(self):
        if not self.first_load:
            time_in_ms = int(self.matched_first_frame / 30 * 1000)
            self.media_player.setPosition(time_in_ms)
            self.media_player.play()
            self.play_button.setText("Pause")

    def mediaStatusChanged(self, status):
        # print(statusMessage[status])
        if status == QMediaPlayer.LoadedMedia and self.first_load:
            time_in_ms = int(self.matched_first_frame / 30 * 1000)
            self.media_player.setPosition(time_in_ms)
            self.media_player.play()
            self.first_load = False
            self.play_button.setText("Pause")

    def playerStatusChanged(self, status):
        # print(statusMessage[status])
        pass

    def postionStatusChanged(self, position):
        duration = self.media_player.duration()
        if duration >= 0:
            total_time = QTime(
                0,
                (duration // 60000) % 60,
                (duration // 1000) % 60
            )
            current_time = QTime(
                0,
                (position // 60000) % 60,
                (position // 1000) % 60
            )
            self.timer_label.setText(
                f"{current_time.toString('mm:ss')} / {total_time.toString('mm:ss')}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VideoPlayer()
    window.show()
    sys.exit(app.exec_())
