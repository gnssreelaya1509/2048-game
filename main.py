import flet as ft
from core.engine_2048 import Engine2048


def main(page: ft.Page):
    page.title = "2048 Flet Edition"
    page.window.width = 450
    page.window.height = 650
    page.window.resizable = False
    page.theme_mode = ft.ThemeMode.DARK
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.bgcolor = "#faf8ef"

    engine = Engine2048()

    TILE_COLORS = {
        0: "#cdc1b4", 2: "#eee4da", 4: "#ede0c8", 8: "#f2b179",
        16: "#f59563", 32: "#f67c5f", 64: "#f65e3b", 128: "#edcf72",
        256: "#edcc61", 512: "#edc850", 1024: "#edc53f", 2048: "#edc22e"
    }

    score_label = ft.Text("SCORE: 0", size=24, weight=ft.FontWeight.BOLD, color="#776e65")
    status_label = ft.Text("Join the numbers to get 2048!", size=16, color="#776e65")

    grid_cells = [[ft.Container(
        width=80, height=80,
        bgcolor="#cdc1b4",
        border_radius=5,
        alignment=ft.Alignment(0, 0),
        content=ft.Text("", size=32, weight=ft.FontWeight.BOLD, color="#776e65")
    ) for _ in range(4)] for _ in range(4)]

    board_container = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(controls=grid_cells[r], spacing=10, alignment=ft.MainAxisAlignment.CENTER)
                for r in range(4)
            ],
            spacing=10
        ),
        bgcolor="#bbada0",
        padding=10,
        border_radius=8
    )

    def update_ui():
        for r in range(4):
            for c in range(4):
                val = engine.board[r][c]
                cell = grid_cells[r][c]
                text_ctrl = cell.content

                text_ctrl.value = str(val) if val > 0 else ""
                text_ctrl.color = "#f9f6f2" if val >= 8 else "#776e65"
                cell.bgcolor = TILE_COLORS.get(val, "#3c3a32")

        score_label.value = f"SCORE: {engine.score}"

        if engine.game_over:
            status_label.value = "Game Over! Press 'R' to Restart."
            status_label.color = "#f65e3b"
        else:
            status_label.value = "Join the numbers to get 2048!"
            status_label.color = "#776e65"

        page.update()

    # FIX: Extracted the reset logic into a safe, independent function
    def trigger_reset(e=None):
        engine.reset_game()
        update_ui()

    def handle_keyboard(e: ft.KeyboardEvent):
        key = e.key.upper().replace(" ", "")

        if key == "R" or key == "ESCAPE":
            trigger_reset()  # Pointing the keyboard 'R' to the new function
            return

        if engine.game_over:
            return

        direction_map = {
            "ARROWUP": "UP", "W": "UP",
            "ARROWDOWN": "DOWN", "S": "DOWN",
            "ARROWLEFT": "LEFT", "A": "LEFT",
            "ARROWRIGHT": "RIGHT", "D": "RIGHT"
        }

        if key in direction_map:
            if engine.move(direction_map[key]):
                update_ui()

    page.on_keyboard_event = handle_keyboard

    page.add(
        ft.Column(
            controls=[
                ft.Row([ft.Text("2048", size=48, weight=ft.FontWeight.BOLD, color="#776e65"), score_label],
                       alignment=ft.MainAxisAlignment.SPACE_BETWEEN, width=370),
                status_label,
                ft.Divider(height=10, color="transparent"),
                board_container,
                ft.Divider(height=20, color="transparent"),
                ft.ElevatedButton(
                    "New Game",
                    color="white", bgcolor="#8f7a66",
                    # FIX: Pointing the button directly to the new function without faking a key press!
                    on_click=trigger_reset,
                    width=370, height=45
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

    update_ui()


if __name__ == "__main__":
    ft.run(main)