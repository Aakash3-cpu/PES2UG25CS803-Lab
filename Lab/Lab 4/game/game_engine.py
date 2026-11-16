import random
import pygame
from game.text_box import TextBox


class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.secret_number = random.randint(1, 100)

        self.attempts = 0

        # Task 4: Maximum attempts
        self.max_attempts = 5
        self.game_over = False

        # Task 2: Dynamic search range
        self.min_range = 1
        self.max_range = 100

        # Task 3: Recent guess history
        self.guess_history = []

        self.feedback_msg = "Enter a number between 1 and 100"
        self.feedback_color = (220, 220, 220)

        self.game_won = False

        self.input_box = TextBox(
            width // 2 - 110,
            150,
            120,
            48
        )

        self.submit_btn = pygame.Rect(
            width // 2 + 25,
            150,
            100,
            48
        )

        self.font_title = pygame.font.SysFont(None, 42)
        self.font_medium = pygame.font.SysFont(None, 28)
        self.font_small = pygame.font.SysFont(None, 24)
        self.font_btn = pygame.font.SysFont(None, 26)

    def submit_guess(self):

        # Do not accept guesses after game ends
        if self.game_won or self.game_over:
            return

        # Task 1: Prevent empty input crash
        if not self.input_box.text.strip():
            self.feedback_msg = "Please enter a number!"
            self.feedback_color = (240, 200, 80)
            return

        guess = int(self.input_box.text)

        self.attempts += 1
        self.input_box.clear()

        # Guess is too low
        if guess < self.secret_number:

            self.min_range = guess + 1

            self.feedback_msg = f"TOO LOW! (Guess was {guess})"
            self.feedback_color = (80, 160, 240)

            # Task 3: Add to history
            self.guess_history.append(
                (guess, "TOO LOW", self.feedback_color)
            )

        # Guess is too high
        elif guess > self.secret_number:

            self.max_range = guess - 1

            self.feedback_msg = f"TOO HIGH! (Guess was {guess})"
            self.feedback_color = (240, 100, 80)

            # Task 3: Add to history
            self.guess_history.append(
                (guess, "TOO HIGH", self.feedback_color)
            )

        # Correct guess
        else:

            self.feedback_msg = (
                f"CORRECT! Found in {self.attempts} attempts."
            )

            self.feedback_color = (80, 220, 90)

            self.game_won = True

            # Task 3: Add correct guess to history
            self.guess_history.append(
                (guess, "CORRECT", self.feedback_color)
            )

            return

        # Task 4: Check maximum attempts
        if self.attempts >= self.max_attempts:

            self.game_over = True

            self.feedback_msg = (
                f"GAME OVER! The number was {self.secret_number}."
            )

            self.feedback_color = (240, 80, 80)

    def reset(self):

        self.secret_number = random.randint(1, 100)

        self.attempts = 0

        # Task 4
        self.game_over = False

        # Task 2
        self.min_range = 1
        self.max_range = 100

        # Task 3
        self.guess_history = []

        self.feedback_msg = "Enter a number between 1 and 100"
        self.feedback_color = (220, 220, 220)

        self.game_won = False

        self.input_box.clear()

    def handle_event(self, event):

        self.input_box.handle_event(event)

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_RETURN:
                self.submit_guess()

            elif event.key == pygame.K_r and (
                self.game_won or self.game_over
            ):
                self.reset()

        elif event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:

                if self.submit_btn.collidepoint(event.pos):
                    self.submit_guess()

    def update(self):
        pass

    def render(self, screen):

        screen.fill((30, 34, 42))

        # -------------------------
        # TITLE
        # -------------------------

        title_surf = self.font_title.render(
            "Number Guessing Arena",
            True,
            (245, 245, 245)
        )

        screen.blit(
            title_surf,
            (
                self.width // 2
                - title_surf.get_width() // 2,
                35
            )
        )

        # -------------------------
        # ATTEMPTS
        # -------------------------

        attempts_surf = self.font_medium.render(
            f"Attempts: {self.attempts}/{self.max_attempts}",
            True,
            (180, 185, 195)
        )

        screen.blit(
            attempts_surf,
            (
                self.width // 2
                - attempts_surf.get_width() // 2,
                95
            )
        )

        # -------------------------
        # VALID RANGE
        # -------------------------

        range_surf = self.font_medium.render(
            f"Valid Range: {self.min_range} - {self.max_range}",
            True,
            (180, 185, 195)
        )

        screen.blit(
            range_surf,
            (
                self.width // 2
                - range_surf.get_width() // 2,
                125
            )
        )

        # -------------------------
        # INPUT
        # -------------------------

        self.input_box.render(screen)

        # -------------------------
        # SUBMIT BUTTON
        # -------------------------

        pygame.draw.rect(
            screen,
            (50, 150, 80),
            self.submit_btn,
            border_radius=6
        )

        pygame.draw.rect(
            screen,
            (220, 220, 220),
            self.submit_btn,
            width=2,
            border_radius=6
        )

        btn_text = self.font_btn.render(
            "SUBMIT",
            True,
            (255, 255, 255)
        )

        screen.blit(
            btn_text,
            (
                self.submit_btn.centerx
                - btn_text.get_width() // 2,
                self.submit_btn.centery
                - btn_text.get_height() // 2
            )
        )

        # -------------------------
        # FEEDBACK
        # -------------------------

        feedback_surf = self.font_medium.render(
            self.feedback_msg,
            True,
            self.feedback_color
        )

        screen.blit(
            feedback_surf,
            (
                self.width // 2
                - feedback_surf.get_width() // 2,
                235
            )
        )

        # -------------------------
        # TASK 3: RECENT GUESSES
        # -------------------------

        history_title = self.font_small.render(
            "Recent Guesses:",
            True,
            (245, 245, 245)
        )

        screen.blit(
            history_title,
            (
                self.width // 2
                - history_title.get_width() // 2,
                300
            )
        )

        recent_guesses = self.guess_history[-5:]

        for i, (guess, result, color) in enumerate(recent_guesses):

            history_text = self.font_small.render(
                f"{guess} - {result}",
                True,
                color
            )

            screen.blit(
                history_text,
                (
                    self.width // 2
                    - history_text.get_width() // 2,
                    330 + (i * 25)
                )
            )

        # -------------------------
        # GAME OVER / WIN
        # -------------------------

        if self.game_over:

            game_over_text = self.font_medium.render(
                "GAME OVER - Press [R] to Restart",
                True,
                (240, 80, 80)
            )

            screen.blit(
                game_over_text,
                (
                    self.width // 2
                    - game_over_text.get_width() // 2,
                    455
                )
            )

        elif self.game_won:

            restart_surf = self.font_medium.render(
                "Press [R] to Start a New Game",
                True,
                (255, 220, 80)
            )

            screen.blit(
                restart_surf,
                (
                    self.width // 2
                    - restart_surf.get_width() // 2,
                    455
                )
            )
