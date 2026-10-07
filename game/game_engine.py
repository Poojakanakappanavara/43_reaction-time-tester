import pygame
from .round import Round

# Game Engine

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (90, 90, 90)
GREEN = (40, 180, 90)
BLUE = (50, 90, 170)


class GameEngine:
    def __init__(self, width, height, rounds_total=5):
        self.width = width
        self.height = height
        self.rounds_total = rounds_total

        # Difficulty settings
        self.difficulties = {
            "easy": (1500, 3500),
            "medium": (1000, 3000),
            "hard": (500, 2000)
        }

        self.difficulty = None
        self.min_wait_ms = 1000
        self.max_wait_ms = 3000

        # difficulty -> playing -> game over
        self.state = "difficulty"

        self.round = None
        self.reaction_times = []

        self.result_shown_at = None
        self.result_pause_ms = 800

        self.font = pygame.font.SysFont("Arial", 30)
        self.big_font = pygame.font.SysFont("Arial", 46)
        self.small_font = pygame.font.SysFont("Arial", 24)

        self.game_over = False
        self._game_over_logged = False

    def start_game(self, difficulty):
        """Start or restart the game."""

        self.difficulty = difficulty

        self.min_wait_ms, self.max_wait_ms = (
            self.difficulties[difficulty]
        )

        self.reaction_times = []

        self.round = Round(
            self.min_wait_ms,
            self.max_wait_ms
        )

        self.result_shown_at = None
        self.game_over = False
        self._game_over_logged = False
        self.state = "playing"

    def handle_event(self, event):

        # -------------------------
        # DIFFICULTY SELECTION
        # -------------------------
        if self.state == "difficulty":

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_1:
                    self.start_game("easy")

                elif event.key == pygame.K_2:
                    self.start_game("medium")

                elif event.key == pygame.K_3:
                    self.start_game("hard")

            return

        # -------------------------
        # GAME OVER
        # -------------------------
        if self.game_over:

            if event.type == pygame.KEYDOWN:

                # R = Replay with same difficulty
                if event.key == pygame.K_r:
                    self.start_game(self.difficulty)

                # D = Change difficulty
                elif event.key == pygame.K_d:
                    self.state = "difficulty"
                    self.game_over = False

            return

        # -------------------------
        # NORMAL GAME INPUT
        # -------------------------
        is_click = event.type == pygame.MOUSEBUTTONDOWN

        is_space = (
            event.type == pygame.KEYDOWN
            and event.key == pygame.K_SPACE
        )

        if is_click or is_space:

            reaction_ms = self.round.register_input()

            if reaction_ms is not None:
                self.reaction_times.append(reaction_ms)

            self.result_shown_at = pygame.time.get_ticks()

    def handle_input(self):
        # Reserved for continuously-held-key input.
        pass

    def update(self):

        if self.state != "playing":
            return

        if self.game_over:
            return

        self.round.update()

        if self.round.state in ("result", "false_start"):

            now = pygame.time.get_ticks()

            if now - self.result_shown_at >= self.result_pause_ms:
                self._start_next_round()

    def _start_next_round(self):

        if len(self.reaction_times) >= self.rounds_total:
            self.game_over = True
            return

        self.round = Round(
            self.min_wait_ms,
            self.max_wait_ms
        )

    def average_reaction_ms(self):

        if not self.reaction_times:
            return 0

        return round(
            sum(self.reaction_times)
            / len(self.reaction_times)
        )

    def render(self, screen):

        # ==================================================
        # DIFFICULTY SELECTION SCREEN
        # ==================================================

        if self.state == "difficulty":

            screen.fill(BLACK)

            title = self.big_font.render(
                "REACTION TIME TESTER",
                True,
                WHITE
            )

            screen.blit(
                title,
                title.get_rect(
                    center=(self.width // 2, 70)
                )
            )

            choose_text = self.font.render(
                "Choose Difficulty",
                True,
                WHITE
            )

            screen.blit(
                choose_text,
                choose_text.get_rect(
                    center=(self.width // 2, 125)
                )
            )

            easy_text = self.small_font.render(
                "1 - EASY   (1500-3500 ms)",
                True,
                WHITE
            )

            medium_text = self.small_font.render(
                "2 - MEDIUM (1000-3000 ms)",
                True,
                WHITE
            )

            hard_text = self.small_font.render(
                "3 - HARD   (500-2000 ms)",
                True,
                WHITE
            )

            screen.blit(
                easy_text,
                easy_text.get_rect(
                    center=(self.width // 2, 190)
                )
            )

            screen.blit(
                medium_text,
                medium_text.get_rect(
                    center=(self.width // 2, 230)
                )
            )

            screen.blit(
                hard_text,
                hard_text.get_rect(
                    center=(self.width // 2, 270)
                )
            )

            instruction = self.small_font.render(
                "Press 1, 2, or 3 to start",
                True,
                WHITE
            )

            screen.blit(
                instruction,
                instruction.get_rect(
                    center=(self.width // 2, 330)
                )
            )

            return

        # ==================================================
        # GAME OVER SCREEN
        # ==================================================

        if self.game_over:

            screen.fill(BLACK)

            title = self.big_font.render(
                "GAME OVER",
                True,
                WHITE
            )

            screen.blit(
                title,
                title.get_rect(
                    center=(self.width // 2, 40)
                )
            )

            difficulty_text = self.small_font.render(
                f"Difficulty: {self.difficulty.upper()}",
                True,
                WHITE
            )

            screen.blit(
                difficulty_text,
                difficulty_text.get_rect(
                    center=(self.width // 2, 80)
                )
            )

            results_title = self.font.render(
                "Your Results",
                True,
                WHITE
            )

            screen.blit(
                results_title,
                results_title.get_rect(
                    center=(self.width // 2, 115)
                )
            )

            y = 150

            for index, reaction_time in enumerate(
                self.reaction_times,
                start=1
            ):

                result_text = self.small_font.render(
                    f"Round {index}: {reaction_time} ms",
                    True,
                    WHITE
                )

                screen.blit(
                    result_text,
                    result_text.get_rect(
                        center=(self.width // 2, y)
                    )
                )

                y += 30

            average_text = self.font.render(
                f"Average: {self.average_reaction_ms()} ms",
                True,
                WHITE
            )

            screen.blit(
                average_text,
                average_text.get_rect(
                    center=(self.width // 2, y + 5)
                )
            )

            replay_text = self.small_font.render(
                "Press R to Replay",
                True,
                WHITE
            )

            screen.blit(
                replay_text,
                replay_text.get_rect(
                    center=(self.width // 2, 345)
                )
            )

            change_text = self.small_font.render(
                "Press D to Change Difficulty",
                True,
                WHITE
            )

            screen.blit(
                change_text,
                change_text.get_rect(
                    center=(self.width // 2, 375)
                )
            )

            if not self._game_over_logged:

                print(
                    "Session complete! Reaction times (ms):",
                    self.reaction_times
                )

                print(
                    "Difficulty:",
                    self.difficulty
                )

                print(
                    "Average:",
                    self.average_reaction_ms(),
                    "ms"
                )

                self._game_over_logged = True

            return

        # ==================================================
        # NORMAL GAME SCREEN
        # ==================================================

        if self.round.state == "waiting":

            bg = GRAY
            message = "Wait for green..."

        elif self.round.state == "go":

            bg = GREEN
            message = "Click now!"

        elif self.round.state == "false_start":

            bg = BLUE
            message = "False Start!"

        else:

            bg = BLUE
            message = f"{self.round.reaction_ms} ms"

        screen.fill(bg)

        text_surf = self.big_font.render(
            message,
            True,
            WHITE
        )

        screen.blit(
            text_surf,
            text_surf.get_rect(
                center=(
                    self.width // 2,
                    self.height // 2
                )
            )
        )

        round_num = min(
            len(self.reaction_times) + 1,
            self.rounds_total
        )

        round_text = self.font.render(
            f"Round {round_num}/{self.rounds_total}",
            True,
            WHITE
        )

        screen.blit(
            round_text,
            (10, 10)
        )

        avg_text = self.font.render(
            f"Avg: {self.average_reaction_ms()} ms",
            True,
            WHITE
        )

        screen.blit(
            avg_text,
            (self.width - 190, 10)
        )