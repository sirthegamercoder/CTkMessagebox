"""
CustomTkinter Messagebox
Author: sirthegamercoder
Version: 2.7
"""

from __future__ import annotations

import os
import sys
from typing import Any, Literal, Optional, Sequence, Tuple, Union

import customtkinter
from PIL import Image, ImageTk


def _clamp(value: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, value))


def _is_color_string(value: Any) -> bool:
    return isinstance(value, str)


class CTkMessagebox(customtkinter.CTkToplevel):
    _ICON_CACHE: dict[tuple[str, tuple[int, int]], customtkinter.CTkImage] = {}

    def __init__(
        self,
        master: Any = None,
        width: int = 400,
        height: int = 200,
        title: str = "CTkMessagebox",
        message: str = "This is a CTkMessagebox!",
        option_1: str = "OK",
        option_2: Optional[str] = None,
        option_3: Optional[str] = None,
        options: Optional[Sequence[str]] = None,
        border_width: int = 1,
        border_color: str = "default",
        button_color: Union[str, Tuple[str, ...]] = "default",
        bg_color: str = "default",
        fg_color: str = "default",
        text_color: str = "default",
        title_color: str = "default",
        button_text_color: str = "default",
        button_width: Optional[int] = None,
        button_height: Optional[int] = None,
        cancel_button_color: Optional[str] = None,
        cancel_button: Optional[Literal["circle", "cross", "none"]] = None,
        button_hover_color: str = "default",
        icon: Optional[str] = "info",
        icon_size: Optional[Tuple[int, int]] = None,
        corner_radius: int = 15,
        justify: Literal["left", "center", "right"] = "right",
        font: Optional[tuple] = None,
        header: bool = False,
        topmost: bool = True,
        fade_in_duration: int = 0,
        sound: bool = False,
        wraplength: int = 0,
        option_focus: Optional[Literal[1, 2, 3]] = None,
    ) -> None:

        super().__init__()

        self.master_window = master
        self.event: Optional[str] = None
        self._closing = False
        self._fade_job: Optional[str] = None
        self._return_funcid: Optional[str] = None
        self.option_focus: Optional[int] = None
        self.selected_button: Optional[customtkinter.CTkButton] = None
        self.selected_option: Optional[str] = None

        self.width = max(250, int(width))
        self.height = max(150, int(height))

        if master is None:
            spawn_x = int((self.winfo_screenwidth() - self.width) / 2)
            spawn_y = int((self.winfo_screenheight() - self.height) / 2)
        else:
            spawn_x = int(
                master.winfo_width() * 0.5 + master.winfo_x() - 0.5 * self.width + 7
            )
            spawn_y = int(
                master.winfo_height() * 0.5 + master.winfo_y() - 0.5 * self.height + 20
            )

        self.geometry(f"{self.width}x{self.height}+{spawn_x}+{spawn_y}")
        self.title(title)
        self.resizable(False, False)

        self.fade = int(fade_in_duration) if fade_in_duration else 0
        if self.fade:
            self.fade = max(20, self.fade)
            self.attributes("-alpha", 0)

        self.oldx = 0
        self.oldy = 0

        if not header:
            self.overrideredirect(True)

        if topmost:
            self.attributes("-topmost", True)
        else:
            self.transient(master)

        if sys.platform.startswith("win"):
            self.transparent_color = self._resolve_transparent_color()
            default_cancel_button: Optional[str] = "cross"
        elif sys.platform.startswith("darwin"):
            self.transparent_color = "systemTransparent"
            self.attributes("-transparent", True)
            default_cancel_button = "circle"
        else:
            self.transparent_color = "#000001"
            corner_radius = 0
            default_cancel_button = "cross"

        self.lift()
        self.config(background=self.transparent_color)

        if sys.platform.startswith("win"):
            try:
                self.attributes("-transparentcolor", self.transparent_color)
            except Exception:
                self.transparent_color = "#000001"
                self.attributes("-transparentcolor", self.transparent_color)

        self.protocol("WM_DELETE_WINDOW", self.button_event)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        if options:
            opts = list(options)
            if len(opts) >= 1:
                option_1 = opts[-1]
            if len(opts) >= 2:
                option_2 = opts[-2]
            if len(opts) >= 3:
                option_3 = opts[-3]

        self.bg_color = (
            self._apply_appearance_mode(
                customtkinter.ThemeManager.theme["CTkFrame"]["fg_color"]
            )
            if bg_color == "default"
            else bg_color
        )
        self.fg_color = (
            self._apply_appearance_mode(
                customtkinter.ThemeManager.theme["CTkFrame"]["top_fg_color"]
            )
            if fg_color == "default"
            else fg_color
        )

        if sys.platform.startswith("win") and (
            self.bg_color == self.transparent_color
            or self.fg_color == self.transparent_color
        ):
            self.transparent_color = "#000001"
            self.attributes("-transparentcolor", self.transparent_color)
            self.config(background=self.transparent_color)

        default_button_color = self._apply_appearance_mode(
            customtkinter.ThemeManager.theme["CTkButton"]["fg_color"]
        )
        self.button_color = self._normalize_button_color(
            button_color, default_button_color
        )

        self.text_color = (
            self._apply_appearance_mode(
                customtkinter.ThemeManager.theme["CTkLabel"]["text_color"]
            )
            if text_color == "default"
            else text_color
        )
        self.title_color = (
            self._apply_appearance_mode(
                customtkinter.ThemeManager.theme["CTkLabel"]["text_color"]
            )
            if title_color == "default"
            else title_color
        )
        self.bt_text_color = (
            self._apply_appearance_mode(
                customtkinter.ThemeManager.theme["CTkButton"]["text_color"]
            )
            if button_text_color == "default"
            else button_text_color
        )
        self.bt_hv_color = (
            self._apply_appearance_mode(
                customtkinter.ThemeManager.theme["CTkButton"]["hover_color"]
            )
            if button_hover_color == "default"
            else button_hover_color
        )
        self.border_color = (
            self._apply_appearance_mode(
                customtkinter.ThemeManager.theme["CTkFrame"]["border_color"]
            )
            if border_color == "default"
            else border_color
        )

        self._title = title
        self.message = message
        self.font = font
        self.justify = justify if justify in ("left", "center", "right") else "right"
        self.sound = sound
        self.cancel_button = cancel_button if cancel_button else default_cancel_button
        self.round_corners = int(_clamp(corner_radius, 0, 30))
        self.button_width = int(button_width) if button_width else int(self.width / 4)
        self.button_height = int(button_height) if button_height else 28
        self.button_height = int(_clamp(self.button_height, 1, self.height / 4 - 20))
        self.border_width = int(_clamp(border_width, 0, 5))

        self.dot_color = cancel_button_color
        if self.dot_color == "transparent":
            self.dot_color = self.bg_color

        size = self._resolve_icon_size(icon_size)
        self.icon = self.load_icon(icon, size) if icon else None

        self.frame_top = customtkinter.CTkFrame(
            self,
            corner_radius=self.round_corners,
            width=self.width,
            border_width=self.border_width,
            bg_color=self.transparent_color,
            fg_color=self.bg_color,
            border_color=self.border_color,
        )
        self.frame_top.grid(sticky="nswe")
        for col in range(6):
            self.frame_top.grid_columnconfigure(col, weight=1)
        for row in range(3):
            self.frame_top.grid_rowconfigure(row, weight=1)

        self.frame_top.bind("<B1-Motion>", self.move_window)
        self.frame_top.bind("<ButtonPress-1>", self.oldxyset)

        self.button_close: Optional[customtkinter.CTkButton] = None
        if self.cancel_button == "cross":
            text_color = (
                self.dot_color if _is_color_string(self.dot_color) else self.title_color
            )
            self.button_close = customtkinter.CTkButton(
                self.frame_top,
                corner_radius=10,
                width=0,
                height=0,
                hover=False,
                border_width=0,
                text_color=text_color,
                text="✕",
                fg_color="transparent",
                command=self.button_event,
            )
            self.button_close.grid(
                row=0,
                column=5,
                sticky="ne",
                padx=5 + self.border_width,
                pady=5 + self.border_width,
            )
        elif self.cancel_button == "circle":
            self.button_close = customtkinter.CTkButton(
                self.frame_top,
                corner_radius=10,
                width=10,
                height=10,
                hover=False,
                border_width=0,
                text="",
                fg_color=(
                    self.dot_color if _is_color_string(self.dot_color) else "#c42b1c"
                ),
                command=self.button_event,
            )
            self.button_close.grid(row=0, column=5, sticky="ne", padx=10, pady=10)

        self.title_label = customtkinter.CTkLabel(
            self.frame_top,
            width=1,
            text=self._title,
            text_color=self.title_color,
            font=self.font,
        )
        self.title_label.grid(
            row=0, column=0, columnspan=6, sticky="nw", padx=(15, 30), pady=5
        )
        self.title_label.bind("<B1-Motion>", self.move_window)
        self.title_label.bind("<ButtonPress-1>", self.oldxyset)

        self.info = customtkinter.CTkButton(
            self.frame_top,
            width=1,
            height=self.height / 2,
            corner_radius=0,
            text=self.message,
            font=self.font,
            fg_color=self.fg_color,
            hover=False,
            text_color=self.text_color,
            image=self.icon,
        )
        self.info._text_label.configure(
            wraplength=int(wraplength) if wraplength > 0 else int(self.width / 2),
            justify="left",
        )
        self.info.grid(
            row=1, column=0, columnspan=6, sticky="nwes", padx=self.border_width
        )

        self.option_text_1: Optional[str] = option_1
        self.option_text_2: Optional[str] = option_2
        self.option_text_3: Optional[str] = option_3

        self.button_1: Optional[customtkinter.CTkButton] = None
        self.button_2: Optional[customtkinter.CTkButton] = None
        self.button_3: Optional[customtkinter.CTkButton] = None

        self.button_1 = self._make_option_button(self.option_text_1, 0)
        if self.option_text_2 is not None:
            self.button_2 = self._make_option_button(self.option_text_2, 1)
        if self.option_text_3 is not None:
            self.button_3 = self._make_option_button(self.option_text_3, 2)

        self._layout_buttons()

        if header:
            self.title_label.configure(text="")
            self.title_label.grid_configure(pady=0)
            if self.button_close is not None:
                self.button_close.configure(text_color=self.bg_color)
            self.frame_top.configure(corner_radius=0)

        self.after_idle(self._grab_and_bind_keys)

        if option_focus in (1, 2, 3):
            self.after_idle(lambda: self.focus_button(option_focus))
        elif (
            self.option_text_2 is None and self.option_text_3 is None and self.button_1
        ):
            self.after_idle(self._focus_default)

        if self.sound:
            self.after(50, self._safe_bell)

        if self.fade:
            self.after_idle(self.fade_in)

        self.after_idle(self._auto_resize_for_message)

    def _resolve_transparent_color(self) -> str:
        try:
            value = self._apply_appearance_mode(self.cget("fg_color"))
        except Exception:
            value = "#000001"
        return value if _is_color_string(value) else "#000001"

    @staticmethod
    def _normalize_button_color(
        button_color: Union[str, Tuple[str, ...]], default: str
    ) -> Tuple[str, str, str]:
        if button_color == "default":
            return (default, default, default)
        if isinstance(button_color, tuple):
            n = len(button_color)
            if n == 1:
                return (button_color[0], default, default)
            if n == 2:
                return (button_color[0], button_color[1], default)
            return (button_color[0], button_color[1], button_color[2])
        return (button_color, button_color, button_color)

    def _resolve_icon_size(
        self, icon_size: Optional[Tuple[int, int]]
    ) -> Tuple[int, int]:
        if icon_size:
            w = max(1, int(icon_size[0]))
            h = max(1, int(min(icon_size[1], self.height - 100)))
        else:
            w = h = max(1, int(self.height / 4))
        return (w, h)

    def _make_option_button(
        self, text: Optional[str], index: int
    ) -> customtkinter.CTkButton:
        return customtkinter.CTkButton(
            self.frame_top,
            text=text,
            fg_color=self.button_color[index],
            width=self.button_width,
            font=self.font,
            text_color=self.bt_text_color,
            hover_color=self.bt_hv_color,
            height=self.button_height,
            command=lambda t=text: self.button_event(t),
        )

    def _layout_buttons(self) -> None:
        has2 = self.button_2 is not None
        has3 = self.button_3 is not None
        span = 1 if self.button_width else 2

        if self.justify == "center":
            if has3:
                cols = [4, 2, 0]
            elif has2:
                cols = [2, 3, 0]
            else:
                cols = [2, 0, 0]
            if has3:
                self._grid(self.button_1, 2, cols[0], span, (0, 10))
                self._grid(self.button_2, 2, cols[1], span, (10, 10))
                self._grid(self.button_3, 2, cols[2], span, (10, 0))
            elif has2:
                self._grid(self.button_1, 2, 2, 2, (0, 5))
                self._grid(self.button_2, 2, 4, 2, (5, 0))
            else:
                self._grid(self.button_1, 2, 2, 2, (0, 10))

        elif self.justify == "left":
            if has3:
                self._grid(self.button_3, 2, 0, span, (10, 0))
                self._grid(
                    self.button_2, 2, 2 if not self.button_width else 1, span, (10, 10)
                )
                self._grid(
                    self.button_1, 2, 4 if not self.button_width else 2, span, (0, 10)
                )
            elif has2:
                self._grid(self.button_2, 2, 0, span, (10, 0))
                self._grid(
                    self.button_1, 2, 2 if not self.button_width else 1, span, (10, 10)
                )
            else:
                self._grid(self.button_1, 2, 0, span, (10, 0))

        else:
            if self.button_width:
                cols = [5, 4, 3]
            else:
                cols = [4, 2, 0]
            self._grid(self.button_1, 2, cols[0], span, (0, 10))
            if has2:
                self._grid(self.button_2, 2, cols[1], span, (10, 10))
            if has3:
                self._grid(self.button_3, 2, cols[2], span, (10, 0))

    def _grid(
        self,
        button: Optional[customtkinter.CTkButton],
        row: int,
        column: int,
        span: int,
        padx: Tuple[int, int],
    ) -> None:
        if button is None:
            return
        button.grid(
            row=row,
            column=column,
            columnspan=span,
            sticky="news",
            padx=padx,
            pady=10,
        )

    def _focus_default(self) -> None:
        if self.button_1 is None or not self.winfo_exists():
            return
        self.button_1.focus()
        self._bind_return(self.button_1, self.option_text_1)

    def _bind_return(
        self, button: customtkinter.CTkButton, option: Optional[str]
    ) -> None:
        self._unbind_return()
        self._return_funcid = button.bind(
            "<Return>", lambda event, opt=option: self.button_event(opt), add="+"
        )

    def _unbind_return(self) -> None:
        if self.selected_button is not None and self._return_funcid is not None:
            try:
                self.selected_button.unbind("<Return>", self._return_funcid)
            except Exception:
                pass
        self._return_funcid = None

    def _grab_and_bind_keys(self) -> None:
        if not self.winfo_exists():
            return
        try:
            self.grab_set()
        except Exception:
            pass
        self.bind("<Escape>", lambda e: self.button_event())
        self.bind("<Left>", lambda e: self.change_left())
        self.bind("<Right>", lambda e: self.change_right())

    def _safe_bell(self) -> None:
        if self.winfo_exists():
            try:
                self.bell()
            except Exception:
                pass

    def _auto_resize_for_message(self) -> None:
        if not self.winfo_exists():
            return
        try:
            needed = self.info._text_label.winfo_reqheight()
        except Exception:
            return
        if needed <= self.height / 2:
            return
        new_height = int(needed - self.height / 2 + self.height)
        self.height = new_height
        self.geometry(f"{self.width}x{new_height}+{self.winfo_x()}+{self.winfo_y()}")

    def place_widget(self, widget, x: int = 10, y: int = 10, **args):
        args.pop("master", None)
        new_widget = widget(master=self.frame_top, **args)
        new_widget.place(x=x, y=y)
        return new_widget

    def focus_button(self, option_focus: int) -> None:
        if option_focus not in (1, 2, 3):
            return
        button = getattr(self, f"button_{option_focus}", None)
        option = getattr(self, f"option_text_{option_focus}", None)
        if button is None or option is None or not self.winfo_exists():
            return

        if self.selected_button is not None:
            try:
                self.selected_button.configure(border_width=0)
            except Exception:
                pass
            self._unbind_return()

        self.option_focus = option_focus
        self.selected_button = button
        self.selected_option = option
        button.focus()
        try:
            button.configure(border_color=self.bt_hv_color, border_width=3)
        except Exception:
            pass
        self._bind_return(button, option)

    def change_left(self) -> None:
        if self.option_focus in (None, 3):
            return
        nxt = self.option_focus + 1
        while nxt <= 3 and getattr(self, f"button_{nxt}", None) is None:
            nxt += 1
        if nxt <= 3:
            self.focus_button(nxt)

    def change_right(self) -> None:
        if self.option_focus in (None, 1):
            return
        nxt = self.option_focus - 1
        while nxt >= 1 and getattr(self, f"button_{nxt}", None) is None:
            nxt -= 1
        if nxt >= 1:
            self.focus_button(nxt)

    def load_icon(
        self, icon: str, size: Tuple[int, int]
    ) -> Optional[customtkinter.CTkImage]:
        key = (icon, size)
        if key in self._ICON_CACHE:
            cached = self._ICON_CACHE[key]
            self._set_window_icon(icon)
            return cached

        if icon in ("check", "cancel", "info", "question", "warning"):
            image_path = os.path.join(
                os.path.dirname(os.path.realpath(__file__)), "icons", icon + ".png"
            )
        else:
            image_path = icon

        try:
            pil_image = Image.open(image_path)
        except Exception:
            return None

        ctk_image = customtkinter.CTkImage(pil_image, size=size)
        self._ICON_CACHE[key] = ctk_image
        self._window_bitmap = ImageTk.PhotoImage(file=image_path)
        self._set_window_icon(icon)
        return ctk_image

    def _set_window_icon(self, icon: str) -> None:
        if sys.platform.startswith("darwin"):
            return
        bitmap = getattr(self, "_window_bitmap", None)
        if bitmap is None:
            return

        def _apply() -> None:
            if not self.winfo_exists():
                return
            try:
                self.iconphoto(False, bitmap)
            except Exception:
                pass

        self.after(200, _apply)

    def fade_in(self) -> None:
        if not self.winfo_exists():
            return
        steps = max(1, int(self.fade))
        interval = max(1, int(1000 / steps))

        def _step(alpha: int = 0) -> None:
            if not self.winfo_exists():
                return
            try:
                self.attributes("-alpha", alpha / 100)
            except Exception:
                return
            if alpha >= 100:
                return
            self._fade_job = self.after(interval, _step, alpha + 10)

        _step(0)

    def fade_out(self, on_done=None) -> None:
        if not self.winfo_exists() or not self.fade:
            if on_done:
                on_done()
            return
        steps = max(1, int(self.fade))
        interval = max(1, int(1000 / steps))

        def _step(alpha: int = 100) -> None:
            if not self.winfo_exists():
                return
            try:
                self.attributes("-alpha", alpha / 100)
            except Exception:
                pass
            if alpha <= 0:
                if on_done:
                    on_done()
                return
            self._fade_job = self.after(interval, _step, alpha - 10)

        _step(100)

    def get(self) -> Optional[str]:
        if self.winfo_exists():
            try:
                self.master.wait_window(self)
            except Exception:
                pass
        return self.event

    def oldxyset(self, event) -> None:
        self.oldx = event.x
        self.oldy = event.y

    def move_window(self, event) -> None:
        if not self.winfo_exists():
            return
        self.x = event.x_root - self.oldx
        self.y = event.y_root - self.oldy
        self.geometry(f"+{self.x}+{self.y}")

    def button_event(self, event: Optional[str] = None) -> None:
        if self._closing:
            return
        self._closing = True

        if self._fade_job is not None:
            try:
                self.after_cancel(self._fade_job)
            except Exception:
                pass
            self._fade_job = None

        for name in ("button_1", "button_2", "button_3"):
            btn = getattr(self, name, None)
            if btn is not None:
                try:
                    btn.configure(state="disabled")
                except Exception:
                    pass

        self.event = event

        def _finish() -> None:
            if not self.winfo_exists():
                return
            try:
                self.grab_release()
            except Exception:
                pass
            try:
                self.destroy()
            except Exception:
                pass
            if self.master_window is not None:
                try:
                    if self.master_window.winfo_exists():
                        self.master_window.focus_force()
                except Exception:
                    pass

        if self.fade:
            self.fade_out(on_done=_finish)
        else:
            _finish()
