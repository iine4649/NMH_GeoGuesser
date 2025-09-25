"""GUI for gui.py

This module contains the Qt-based user interface used by the NMH GeoGuesser
application.

Summary
- MainWindow: the main application window. Responsible for difficulty
    selection, showing the current photo, the clickable map widget, the timer
    and score display, and end-of-game summary.
- PhotoLabel: QLabel subclass that scales QPixmap while preserving aspect
    ratio and quality.

Data expectations
- The game relies on `initialize_game_state` and `get_processed_image_path`
    from `src/game.py`. Each image entry passed to the UI is expected to be a dict with at least these keys:
        - "imlocationx": int (x coordinate on the map)
        - "imlocationy": int (y coordinate on the map)
        - a filename/path that `get_processed_image_path` can turn into a local
            filesystem path usable by QPixmap.

Running
- Use the project entrypoint `src/main.py` to start the application. From
    the project root (using the project's venv):

        /path/to/project/.venv/bin/python src/main.py

"""

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QSizePolicy,
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QAction, QKeySequence, QPixmap

from clickable_map import ClickableMap
from score import get_scores
from game import save_final_score,get_rankings,initialize_game_state,get_processed_image_path



class PhotoLabel(QLabel):
    def __init__(self, text=""):
        super().__init__(text)
        self.isrunning = 0

    def setPixmap(self, pixmap):
        if pixmap and not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(
                self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            super().setPixmap(scaled_pixmap)
        else:
            super().setPixmap(pixmap)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NMH GeoGuesser")
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.timer_duration = 30
        self.time_remaining = self.timer_duration
        self.guess_made = False
        self.current_score = 0
        self.current_image_data = None
        self.images_list = []
        self.current_image_index = 0
        self.current_difficulty = None
        self.setup_menu_bar()
        self.show_difficulty_selection()
        #lets the difficulty loading function know what the difficulty is
        self.isrunning = 0

    def setup_menu_bar(self):
        view_menu = self.menuBar().addMenu("View")
        fullscreen_action = QAction("Toggle Full Screen", self)
        fullscreen_action.setShortcut(QKeySequence("F11"))
        fullscreen_action.triggered.connect(self.toggle_fullscreen)
        view_menu.addAction(fullscreen_action)

    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F11:
            self.toggle_fullscreen()
        elif event.key() == Qt.Key_Escape and self.isFullScreen():
            self.showNormal()
        else:
            super().keyPressEvent(event)

    def initialize_game(self, difficulty):
        game_state = initialize_game_state(difficulty)
        self.images_list = game_state["images_list"]
        self.current_image_index = game_state["current_image_index"]
        self.current_score = game_state["current_score"]
        self.current_difficulty = game_state["current_difficulty"]
        self.current_image_data = game_state["current_image_data"]

    def show_difficulty_selection(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        self.setCentralWidget(widget)

        title_label = QLabel("NMH GeoGuesser")
        title_label.setAlignment(Qt.AlignCenter| Qt.AlignVCenter)
        layout.addWidget(title_label)

        subtitle_label = QLabel("Select Difficulty:")
        subtitle_label.setAlignment(Qt.AlignCenter | Qt.AlignTop)
        layout.addWidget(subtitle_label)

        # Put Easy and Hard buttons side-by-side near the top
        btn_row = QWidget()
        btn_layout = QHBoxLayout(btn_row)
        btn_layout.setSpacing(20)
        btn_layout.setContentsMargins(0, 10, 0, 10)

        easy_button = QPushButton("Easy")
        easy_button.setFixedWidth(120)
        easy_button.clicked.connect(self.start_easy_game)
        btn_layout.addWidget(easy_button)
        
        hard_button = QPushButton("Hard")
        hard_button.setFixedWidth(120)
        hard_button.clicked.connect(self.start_hard_game)
        btn_layout.addWidget(hard_button)

        # center the button row
        btn_layout.setAlignment(Qt.AlignHCenter)
        layout.addWidget(btn_row)

    def start_easy_game(self):
        self.start_game("easy")
        self.isrunning = 1

    def start_hard_game(self):
        self.start_game("hard")
        self.isrunning = 2

    def start_game(self, difficulty):
        print(f"Starting game with difficulty: {difficulty}")
        self.initialize_game(difficulty)
        self.show_game_screen(difficulty)

    def show_game_screen(self, difficulty):
        widget = QWidget()
        self.setCentralWidget(widget)

        main_layout = QVBoxLayout()
        widget.setLayout(main_layout)

        self.photo_label = PhotoLabel("Photo will appear here")
        self.photo_label.setAlignment(Qt.AlignCenter)
        self.photo_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        main_layout.addWidget(self.photo_label, 1)

        middle_layout = QHBoxLayout()
        self.timer_label = QLabel(f"Timer: {self.timer_duration}")
        self.score_label = QLabel(f"Score: {self.current_score}")
        self.image_counter_label = QLabel()

        # Add labels to layout
        self.timer_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        middle_layout.addWidget(self.timer_label)

        self.score_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        middle_layout.addWidget(self.score_label)

        self.image_counter_label.setAlignment(Qt.AlignCenter)
        middle_layout.addWidget(self.image_counter_label)

        self.update_image_counter_display()
        main_layout.addLayout(middle_layout)

        self.load_current_image()

        self.start_round_timer()

        self.clickable_map = ClickableMap("assets/nmh_map.png")
        self.clickable_map.clicked.connect(self.on_map_clicked)
        self.clickable_map.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        main_layout.addWidget(self.clickable_map, 2)

    def on_map_clicked(self, x, y):
        print(f"Map clicked at coordinates: ({x}, {y})")
        self.stop_timer()
        self.guess_made = True

        if self.current_image_data:
            guess_point = (x, y)
            correct_x = self.current_image_data["imlocationx"]
            correct_y = self.current_image_data["imlocationy"]
            correct_point = (correct_x, correct_y)

            round_score = get_scores(guess_point, correct_point)
            self.current_score = self.current_score + round_score

            print(f"Round score: {round_score}, Total score: {self.current_score}")
            print(f"Correct location was: {correct_point}")
            self.update_score_display()

            self.advance_to_next_image()

    def update_score_display(self):
        self.score_label.setText(f"Score: {self.current_score}")

    def load_current_image(self):
        image_path = get_processed_image_path(self.current_image_data)

        if image_path:
            pixmap = QPixmap(image_path)
            if not pixmap.isNull():
                self.photo_label.setPixmap(pixmap)
                print(f"Loaded image: {image_path}")
            else:
                self.photo_label.setText(f"Failed to load image: {image_path}")
                print(f"Failed to load image: {image_path}")
        else:
            self.photo_label.setText("No image data available")
            print("No image data available")

    def update_image_counter_display(self):
        current_num = self.current_image_index + 1
        total_num = len(self.images_list)

        counter_text = f"Image: {current_num}/{total_num}"
        if current_num == total_num:
            counter_text = f"Image: {current_num}/{total_num} (Final Round)"

        self.image_counter_label.setText(counter_text)

    def start_round_timer(self):
        self.time_remaining = self.timer_duration
        self.guess_made = False
        self.update_timer_display()
        self.timer.start(1000)

    def stop_timer(self):
        self.timer.stop()

    def update_timer(self):
        if self.time_remaining > 0:
            self.time_remaining = self.time_remaining - 1
            self.update_timer_display()
        else:
            self.timer.stop()
            self.auto_advance_round()

    def update_timer_display(self):
        self.timer_label.setText(f"Timer: {self.time_remaining}")

    def auto_advance_round(self):
        guess_was_made = self.guess_made
        if not guess_was_made:
            print("Time's up! Auto-advancing to next round")
        print("Moving to next round")
        self.advance_to_next_image()

    def advance_to_next_image(self):
        self.current_image_index += 1

        game_complete = self.is_game_complete()
        if game_complete:
            print("Game complete!")
            self.show_end_screen()
        else:
            self.current_image_data = self.images_list[self.current_image_index]
            self.load_current_image()
            self.update_image_counter_display()
            self.start_round_timer()

            current_image_num = self.current_image_index + 1
            total_images = len(self.images_list)
            print(f"Advanced to image {current_image_num} of {total_images}")

    def is_game_complete(self):
        return self.current_image_index >= len(self.images_list)

    def show_end_screen(self):
        if self.current_difficulty:
            save_final_score(self.current_score, self.current_difficulty)

        widget = QWidget()
        self.setCentralWidget(widget)

        layout = QVBoxLayout()
        widget.setLayout(layout)

        score_label = QLabel("Game Complete!")
        score_label.setAlignment(Qt.AlignCenter)
        score_label.setStyleSheet("font-size: 24px; font-weight: bold; margin: 20px;")
        layout.addWidget(score_label)

        final_score_label = QLabel(f"Final Score: {self.current_score}")
        final_score_label.setAlignment(Qt.AlignCenter)
        final_score_label.setStyleSheet("font-size: 18px; margin: 10px;")
        layout.addWidget(final_score_label)

        rankings_label = QLabel("Leaderboard:")
        rankings_label.setAlignment(Qt.AlignCenter)
        rankings_label.setStyleSheet(
            "font-size: 16px; font-weight: bold; margin-top: 20px;"
        )
        layout.addWidget(rankings_label)

        if self.current_difficulty:
            rankings = get_rankings(self.current_difficulty)

            if rankings:
                max_rankings = 5
                if len(rankings) < max_rankings:
                    max_rankings = len(rankings)

                for i in range(max_rankings):
                    entry = rankings[i]
                    rank_number = i + 1
                    player_name = entry["player"]
                    player_score = entry["score"]
                    rank_text = f"{rank_number}. {player_name} - {player_score} points"

                    rank_label = QLabel(rank_text)
                    rank_label.setAlignment(Qt.AlignCenter)
                    rank_label.setStyleSheet("margin: 5px;")
                    layout.addWidget(rank_label)
            else:
                no_rankings_label = QLabel("No previous scores recorded")
                no_rankings_label.setAlignment(Qt.AlignCenter)
                no_rankings_label.setStyleSheet("margin: 10px; font-style: italic;")
                layout.addWidget(no_rankings_label)
