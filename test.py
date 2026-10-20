import customtkinter as ctk

import CTkMessagebox


class TestApp(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        self.title("CTkMessagebox Test")
        self.geometry("640x520")
        self.minsize(520, 420)

        self.status = ctk.CTkLabel(self, text="No dialog shown yet.", anchor="w")
        self.status.pack(side="bottom", fill="x", padx=12, pady=(4, 12))

        header = ctk.CTkLabel(
            self,
            text="Click a button to open a messagebox",
            font=ctk.CTkFont(size=16, weight="bold"),
        )
        header.pack(pady=(14, 8))

        grid = ctk.CTkFrame(self)
        grid.pack(fill="both", expand=True, padx=12, pady=8)

        tests = [
            ("Info (1 button)", self.t_info),
            ("Question (2 buttons)", self.t_question),
            ("Warning (3 buttons)", self.t_warning),
            ("Check", self.t_check),
            ("Cancel icon", self.t_cancel),
            ("No icon", self.t_no_icon),
            ("Custom icon size", self.t_icon_size),
            ("Options list", self.t_options_list),
            ("Left justify", self.t_left),
            ("Center justify", self.t_center),
            ("Custom colors", self.t_colors),
            ("Fade in", self.t_fade),
            ("Header mode", self.t_header),
            ("Long wrapped message", self.t_wrap),
            ("Focus option 2 + sound", self.t_focus_sound),
            ("Cancel button = circle", self.t_circle),
            ("Cancel button = none", self.t_none),
            ("No master (screen center)", self.t_no_master),
        ]

        for i, (label, cmd) in enumerate(tests):
            btn = ctk.CTkButton(grid, text=label, command=cmd, width=200)
            btn.grid(row=i // 3, column=i % 3, padx=6, pady=6, sticky="ew")

        for c in range(3):
            grid.grid_columnconfigure(c, weight=1)

    def _show(self, **kwargs) -> None:
        box = CTkMessagebox(master=self, **kwargs)
        answer = box.get()
        text = f"Answer: {answer!r}"
        print(text)
        self.status.configure(text=text)

    def t_info(self) -> None:
        self._show(
            title="Info",
            message="This is an informational message.",
            icon="info",
            option_1="OK",
        )

    def t_question(self) -> None:
        self._show(
            title="Question",
            message="Do you want to continue?",
            icon="question",
            option_1="Yes",
            option_2="No",
        )

    def t_warning(self) -> None:
        self._show(
            title="Warning",
            message="Unsaved changes will be lost.\nSave before quitting?",
            icon="warning",
            option_1="Save",
            option_2="Discard",
            option_3="Cancel",
            justify="center",
        )

    def t_check(self) -> None:
        self._show(
            title="Done",
            message="Operation completed successfully.",
            icon="check",
            option_1="Great",
            button_color="#2fa572",
        )

    def t_cancel(self) -> None:
        self._show(
            title="Error",
            message="Something went wrong.",
            icon="cancel",
            option_1="Close",
            button_color="#c42b1c",
        )

    def t_no_icon(self) -> None:
        self._show(
            title="Plain",
            message="No icon on this one.",
            icon=None,
            option_1="OK",
        )

    def t_icon_size(self) -> None:
        self._show(
            title="Big icon",
            message="The icon is rendered at 64x64.",
            icon="info",
            icon_size=(64, 64),
            width=420,
            height=220,
            option_1="OK",
        )

    def t_options_list(self) -> None:
        self._show(
            title="From options list",
            message="Order comes from the options list.",
            icon="question",
            options=["Cancel", "No", "Yes"],
        )

    def t_left(self) -> None:
        self._show(
            title="Left justified",
            message="Buttons are packed to the left.",
            icon="info",
            option_1="A",
            option_2="B",
            justify="left",
        )

    def t_center(self) -> None:
        self._show(
            title="Centered",
            message="Buttons are centered.",
            icon="info",
            option_1="A",
            option_2="B",
            option_3="C",
            justify="center",
        )

    def t_colors(self) -> None:
        self._show(
            title="Custom colors",
            message="Dark theme, custom accents.",
            icon="info",
            option_1="Primary",
            option_2="Secondary",
            bg_color="#1f1f1f",
            fg_color="#2b2b2b",
            border_color="#ff9f1c",
            text_color="#e0e0e0",
            title_color="#ff9f1c",
            button_color=("#ff9f1c", "#3a86ff"),
            button_text_color="#101010",
            button_hover_color="#ffbf69",
            cancel_button_color="#ff9f1c",
        )

    def t_fade(self) -> None:
        self._show(
            title="Fade in",
            message="This box fades in over ~40 steps.",
            icon="info",
            option_1="OK",
            fade_in_duration=40,
        )

    def t_header(self) -> None:
        self._show(
            title="Header mode",
            message="In header mode the title bar is hidden.",
            icon="info",
            option_1="OK",
            header=True,
            topmost=False,
        )

    def t_wrap(self) -> None:
        self._show(
            title="Long message",
            message=(
                "This is a much longer message that should wrap across "
                "several lines so you can verify that the dialog grows "
                "vertically to fit the content instead of clipping it. "
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit, "
                "sed do eiusmod tempor incididunt ut labore et dolore."
            ),
            icon="info",
            option_1="OK",
            wraplength=320,
            width=420,
        )

    def t_focus_sound(self) -> None:
        self._show(
            title="Focus + sound",
            message="Option 2 has focus. Use Left/Right arrows and Enter.",
            icon="question",
            option_1="One",
            option_2="Two",
            option_3="Three",
            option_focus=2,
            sound=True,
        )

    def t_circle(self) -> None:
        self._show(
            title="Circle close",
            message="Close button is a circle (red dot).",
            icon="info",
            option_1="OK",
            cancel_button="circle",
        )

    def t_none(self) -> None:
        self._show(
            title="No close button",
            message="Only the OK button can dismiss this one.",
            icon="info",
            option_1="OK",
            cancel_button="none",
        )

    def t_no_master(self) -> None:
        box = CTkMessagebox(
            title="Screen centered",
            message="This dialog has no master and centers on the screen.",
            icon="info",
            option_1="OK",
        )
        answer = box.get()
        self.status.configure(text=f"Answer: {answer!r}")


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    TestApp().mainloop()
