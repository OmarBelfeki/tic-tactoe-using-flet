import flet as ft

x_turn: bool = True
board = [""] * 9


def main(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window.height = 750
    page.window.width = 390
    page.window.bgcolor = ft.Colors.BLACK
    page.bgcolor = ft.Colors.BLACK

    def check_winner():
        win_conditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        for condition in win_conditions:
            if (
                board[condition[0]] == board[condition[1]] == board[condition[2]]
                and board[condition[0]] != ""
            ):
                return board[condition[0]]
        return None

    def show_login_dialog(winner):
        def submit(e: ft.ControlEvent) -> None:
            winner_name = name_field.value
            e.page.dialog.open = False
            e.page.snack_bar = ft.SnackBar(ft.Text(f"{winner_name} is the winner!"))
            e.page.snack_bar.open = True
            e.page.update()

        name_field = ft.TextField(label="Enter your name")
        login_dialog = ft.AlertDialog(
            title=ft.Text(f"Congratulations, {winner}!"),
            content=name_field,
            actions=[
                ft.TextButton(text="Submit", on_click=submit),
                ft.TextButton(text="Cancel", on_click=lambda e: setattr(e.page.dialog, "open", False)),
            ]
        )
        page.dialog = login_dialog
        page.dialog.open = True
        page.update()

    def repeat(e: ft.ControlEvent) -> None:
        global board, x_turn
        board = [""] * 9
        x_turn = True
        for i in e.page.controls[3].controls:
            i.content.value = ""
        e.page.controls[1].value = "IT'S X TURN"
        e.page.controls[2].visible = False
        e.page.update()

    def clicked(e: ft.ControlEvent) -> None:
        global x_turn, board
        idx = e.control.data
        if board[idx] == "":
            board[idx] = "X" if x_turn else "O"
            e.control.content.value = board[idx]
            winner = check_winner()
            if winner:
                e.page.controls[2].value = f"The Winner is {winner}"
                e.page.controls[2].visible = True
                show_login_dialog(winner)
            else:
                x_turn = not x_turn
                e.page.controls[1].value = f"IT'S {'X' if x_turn else 'O'} TURN"
        e.page.update()

    page.add(
        ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Text(
                    value="Turn On/Off two\nplayer mode",
                    size=25,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Switch(),
            ],
        ),
        ft.Text(
            value="IT'S X TURN",
            size=25,
            width=300,
            text_align=ft.TextAlign.CENTER,
        ),
        ft.Text(
            value="The Winner is X",
            size=35,
            width=300,
            text_align=ft.TextAlign.CENTER,
            weight=ft.FontWeight.BOLD,
            visible=False,
        ),
        ft.Row(
            wrap=True,
            controls=[
                ft.Container(
                    alignment=ft.alignment.center,
                    content=ft.Text(value="", size=40),
                    bgcolor="#001354",
                    width=100,
                    height=100,
                    border_radius=ft.border_radius.all(value=15),
                    on_click=clicked,
                    data=i,
                )
                for i in range(9)
            ],
        ),
        ft.Divider(height=90, color=ft.Colors.TRANSPARENT),
        ft.TextButton(
            content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Icon(
                        name=ft.Icons.ROTATE_LEFT,
                        color=ft.Colors.RED_800,
                        size=28,
                    ),
                    ft.Text(
                        value="Repeat the game",
                        color=ft.Colors.RED_800,
                        size=20,
                    ),
                ],
            ),
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.with_opacity(opacity=0.4, color=ft.Colors.RED),
            ),
            on_click=repeat
        )
    )

    page.update()


ft.app(main, assets_dir="assets")
