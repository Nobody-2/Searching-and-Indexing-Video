import sys
import vlc
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QSlider,
    QPushButton,
)
from PySide6.QtCore import Qt, QTimer


class VLCPlayer(QMainWindow):
    def __init__(self, windowTitle):
        super().__init__()

        # Create a basic window
        self.setWindowTitle(windowTitle)
        self.setGeometry(100, 100, 352, 288)

        # Create a central widget and layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Create a VLC instance and media player
        self.vlc_instance = vlc.Instance()
        self.media_player = self.vlc_instance.media_player_new()

        # Create a frame (as a video panel) and add it to the layout
        self.video_frame = QWidget()
        self.video_frame.setMinimumSize(352, 288)
        main_layout.addWidget(self.video_frame)

        # Create and add a slider
        self.slider = QSlider(Qt.Horizontal)
        main_layout.addWidget(self.slider)
        self.slider.sliderMoved.connect(self.set_position)

        # Timer to update slider
        self.timer = QTimer(self)
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_slider)

        # Button layout
        button_layout = QHBoxLayout()

        # Buttons
        self.reset_button = QPushButton("Reset")
        self.play_button = QPushButton("Play")
        self.pause_button = QPushButton("Pause")
        button_layout.addWidget(self.reset_button)
        button_layout.addWidget(self.play_button)
        button_layout.addWidget(self.pause_button)

        # Add button layout to main layout
        main_layout.addLayout(button_layout)

        # Connect buttons to functions
        self.reset_button.clicked.connect(self.reset_media)
        self.play_button.clicked.connect(self.play_media)
        self.pause_button.clicked.connect(self.pause_media)

    def play(self, media_path):
        # Set the media for the player
        media = self.vlc_instance.media_new(media_path)
        self.media_player.set_media(media)

        # Set the window ID where to render the video
        win_id = int(self.video_frame.winId())
        if sys.platform.startswith("darwin"):  # for MacOS
            self.media_player.set_nsobject(win_id)
        else:  # for Windows/Linux
            self.media_player.set_xwindow(win_id)

        # Start playing
        self.media_player.play()
        self.timer.start()

        # Wait for the media to be parsed to get its duration
        media.parse()
        duration = media.get_duration()  # Duration in milliseconds
        self.slider.setMaximum(duration)

    def set_position(self, position):
        # Set the position of the media
        self.media_player.set_position(position / self.slider.maximum())

    def update_slider(self):
        # Update the position of the slider
        media_pos = self.media_player.get_position() * self.slider.maximum()
        self.slider.setValue(int(media_pos))

    def reset_media(self):
        self.media_player.set_position(0)
        self.media_player.play()

    def play_media(self):
        self.media_player.play()

    def pause_media(self):
        self.media_player.pause()


def playVideo(vid: "Videos/video1.mp4", start_time: 60):
    app = QApplication(sys.argv)
    player = VLCPlayer(vid)
    player.show()

    # Convert start and end times from seconds to milliseconds
    start_time_ms = start_time * 1000

    player.play(vid)  # Update this path

    player.media_player.set_time(start_time_ms)

    sys.exit(app.exec())
