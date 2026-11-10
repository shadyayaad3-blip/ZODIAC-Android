# -*- coding: utf-8 -*-
"""
ZODIAC - Premium Mobile-First UI Components & Animations
Designed for modern Android UX with luxury cosmic styling.
Eliminates all Windows desktop-style borders, boxes, and default appearances.
"""

import math
import random
from datetime import datetime, date

from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.clipboard import Clipboard
from kivy.core.window import Window
from kivy.graphics import (
    Color, Ellipse, Line, Rectangle, RoundedRectangle
)
from kivy.metrics import dp
from kivy.properties import (
    BooleanProperty, ListProperty, NumericProperty, ObjectProperty, StringProperty
)
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

from zodiac_data import ar, get_arabic_month_name

FONT_PATH = "assets/arial.ttf"
LOGO_PATH = "assets/zodiac_logo.png"
LOGO_FULL_PATH = "assets/zodiac_logo_full.png"
ICON_PATH = "assets/icon.png"

# ---------------------------------------------------------
# Theme Color Constants (Strictly matching specifications)
# ---------------------------------------------------------
COLOR_BG_MAIN = (0.031, 0.031, 0.090, 1.0)        # #080817
COLOR_BG_SEC = (0.067, 0.067, 0.165, 1.0)         # #11112A
COLOR_CARD = (0.098, 0.094, 0.196, 1.0)           # #191832
COLOR_CARD_SURFACE = (0.078, 0.075, 0.160, 1.0)   # #141328
COLOR_CARD_BORDER = (0.22, 0.19, 0.38, 0.40)      # Ultra-soft ambient border
COLOR_CARD_SHADOW = (0.02, 0.02, 0.06, 0.60)      # Ambient dark shadow
COLOR_ACCENT_PRIMARY = (0.655, 0.545, 0.980, 1.0)  # #A78BFA (Lavender)
COLOR_ACCENT_SEC = (0.486, 0.227, 0.929, 1.0)      # #7C3AED (Primary Purple)
COLOR_ACCENT_DEEP = (0.427, 0.157, 0.851, 1.0)     # #6D28D9
COLOR_TEXT = (1.0, 1.0, 1.0, 1.0)                  # #FFFFFF
COLOR_TEXT_MUTED = (0.647, 0.639, 0.722, 1.0)     # #A5A3B8


# ---------------------------------------------------------
# Cosmic Animated Star Particles Background
# ---------------------------------------------------------
class CosmicBackground(FloatLayout):
    """
    Living cosmic space background with deep nebula gradients and
    animated twinkling star particles.
    """
    enable_particles = BooleanProperty(True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.stars = []
        self._clock_ev = None
        self._time = 0.0

        with self.canvas.before:
            # Main dark space background #080817
            Color(rgba=COLOR_BG_MAIN)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)

            # Top cosmic nebula glow (#7C3AED with low alpha)
            Color(0.486, 0.227, 0.929, 0.12)
            self.nebula_top = Ellipse(pos=(0, 0), size=(0, 0))

            # Bottom cosmic nebula glow (#4C1D95 with low alpha)
            Color(0.30, 0.11, 0.58, 0.10)
            self.nebula_bottom = Ellipse(pos=(0, 0), size=(0, 0))

            # Canvas group for star particles
            self._stars_group = []
            for _ in range(50):
                color_inst = Color(0.92, 0.90, 1.0, 0.5)
                ellipse_inst = Ellipse(pos=(-50, -50), size=(2, 2))
                self._stars_group.append((color_inst, ellipse_inst))

        self.bind(pos=self._update_geometry, size=self._update_geometry)
        self._init_stars()

        # Start star animation clock at 30 FPS
        self._clock_ev = Clock.schedule_interval(self._update_stars, 1.0 / 30.0)

    def _init_stars(self):
        self.stars = []
        for i in range(50):
            star = {
                "nx": random.uniform(0.02, 0.98),
                "ny": random.uniform(0.02, 0.98),
                "size": random.uniform(1.2, 3.0),
                "base_alpha": random.uniform(0.20, 0.80),
                "twinkle_speed": random.uniform(1.2, 3.2),
                "phase": random.uniform(0, math.pi * 2),
                "vy": random.uniform(0.004, 0.015),
                "color_inst": self._stars_group[i][0],
                "ellipse_inst": self._stars_group[i][1],
            }
            self.stars.append(star)

    def _update_geometry(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

        top_w = self.width * 1.15
        top_h = self.height * 0.45
        self.nebula_top.pos = (self.x + (self.width - top_w) / 2, self.y + self.height - top_h * 0.7)
        self.nebula_top.size = (top_w, top_h)

        bot_w = self.width * 0.95
        bot_h = self.height * 0.38
        self.nebula_bottom.pos = (self.x + (self.width - bot_w) / 2, self.y - bot_h * 0.35)
        self.nebula_bottom.size = (bot_w, bot_h)

    def _update_stars(self, dt):
        if not self.enable_particles:
            return

        self._time += dt
        w = max(self.width, 1)
        h = max(self.height, 1)
        base_x = self.x
        base_y = self.y

        for star in self.stars:
            alpha = star["base_alpha"] + 0.35 * math.sin(self._time * star["twinkle_speed"] + star["phase"])
            alpha = max(0.08, min(0.95, alpha))
            star["color_inst"].rgba = (0.94, 0.92, 1.0, alpha)

            star["ny"] += star["vy"] * dt
            if star["ny"] > 1.02:
                star["ny"] = -0.02
                star["nx"] = random.uniform(0.02, 0.98)

            px = base_x + star["nx"] * w
            py = base_y + star["ny"] * h
            s = dp(star["size"])
            star["ellipse_inst"].pos = (px - s / 2, py - s / 2)
            star["ellipse_inst"].size = (s, s)

    def on_enable_particles(self, instance, value):
        if not value:
            for color_inst, _ in self._stars_group:
                color_inst.rgba = (0, 0, 0, 0)
        else:
            self._update_stars(0.01)


# ---------------------------------------------------------
# Modern Mobile Card (Organic Rounded #191832 Surface)
# ---------------------------------------------------------
class ModernMobileCard(BoxLayout):
    """
    Modern Android card with 20dp rounded corners, ambient dark shadow,
    and no harsh desktop-style outlines.
    """
    radius = ListProperty([dp(20)])
    bg_color = ListProperty(list(COLOR_CARD))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = kwargs.get("orientation", "vertical")
        self.padding = kwargs.get("padding", dp(18))
        self.spacing = kwargs.get("spacing", dp(12))

        with self.canvas.before:
            # Ambient drop shadow
            Color(rgba=COLOR_CARD_SHADOW)
            self._shadow = RoundedRectangle(
                pos=(self.x, self.y - dp(3)),
                size=(self.width, self.height),
                radius=self.radius
            )

            # Card surface
            self._bg_col = Color(rgba=self.bg_color)
            self._bg_rect = RoundedRectangle(
                pos=self.pos, size=self.size, radius=self.radius
            )

            # Ultra-subtle sheen border
            self._border_col = Color(rgba=COLOR_CARD_BORDER)
            self._border_line = Line(
                rounded_rectangle=(self.x, self.y, self.width, self.height, self.radius[0]),
                width=dp(0.9)
            )

        self.bind(pos=self._update_canvas, size=self._update_canvas)

    def _update_canvas(self, *args):
        r = self.radius[0] if self.radius else dp(20)
        self._shadow.pos = (self.x, self.y - dp(3))
        self._shadow.size = self.size
        self._shadow.radius = self.radius

        self._bg_rect.pos = self.pos
        self._bg_rect.size = self.size
        self._bg_rect.radius = self.radius

        self._border_line.rounded_rectangle = (self.x, self.y, self.width, self.height, r)

    def on_bg_color(self, instance, val):
        self._bg_col.rgba = val


# ---------------------------------------------------------
# Premium Android Mobile Button (Gradient, Rounded, Touch Feedback)
# ---------------------------------------------------------
class ModernMobileButton(ButtonBehavior, BoxLayout):
    """
    Modern Android mobile button with 18-20dp rounded corners,
    vibrant purple gradient background, ambient purple glow, and
    interactive touch scale animation. Zero Windows dialog box look.
    """
    text = StringProperty("")
    font_size = NumericProperty(dp(16))
    icon = StringProperty("")
    radius = ListProperty([dp(20)])
    is_pressed = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.size_hint_y = None
        self.height = kwargs.get("height", dp(54))
        self.padding = [dp(16), dp(6)]
        self.spacing = dp(8)

        with self.canvas.before:
            # Ambient purple glow / drop shadow
            self._glow_col = Color(0.486, 0.227, 0.929, 0.28)
            self._glow_rect = RoundedRectangle(
                pos=(self.x, self.y - dp(3)),
                size=(self.width, self.height),
                radius=self.radius
            )

            # Vibrant purple gradient background (#7C3AED to #6D28D9)
            self._bg_col = Color(0.486, 0.227, 0.929, 1.0)
            self._bg_rect = RoundedRectangle(
                pos=self.pos, size=self.size, radius=self.radius
            )

            # Subtle top sheen highlight
            self._sheen_col = Color(0.655, 0.545, 0.980, 0.35)
            self._sheen_line = Line(
                rounded_rectangle=(self.x + dp(1), self.y + dp(1), self.width - dp(2), self.height - dp(2), self.radius[0]),
                width=dp(1.0)
            )

        self.lbl_text = Label(
            text=ar(self.text),
            font_name=FONT_PATH,
            font_size=self.font_size,
            bold=True,
            color=COLOR_TEXT,
            halign="center",
            valign="middle"
        )
        self.lbl_text.bind(size=self.lbl_text.setter("text_size"))
        self.add_widget(self.lbl_text)

        self.bind(pos=self._update_canvas, size=self._update_canvas, text=self._update_text)

    def _update_text(self, *args):
        self.lbl_text.text = ar(self.text)

    def _update_canvas(self, *args):
        r = self.radius[0] if self.radius else dp(20)
        self._glow_rect.pos = (self.x, self.y - dp(3))
        self._glow_rect.size = self.size
        self._glow_rect.radius = self.radius

        self._bg_rect.pos = self.pos
        self._bg_rect.size = self.size
        self._bg_rect.radius = self.radius

        self._sheen_line.rounded_rectangle = (
            self.x + dp(1), self.y + dp(1), max(1, self.width - dp(2)), max(1, self.height - dp(2)), r
        )

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.is_pressed = True
            # Touch feedback: subtle scale bounce and deeper purple
            self._bg_col.rgba = (0.38, 0.16, 0.74, 1.0)
            self._glow_col.rgba = (0.486, 0.227, 0.929, 0.45)
            anim = Animation(height=self.height - dp(3), d=0.08, t="out_quad")
            anim.start(self)
            return super().on_touch_down(touch)
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        if self.is_pressed:
            self.is_pressed = False
            self._bg_col.rgba = (0.486, 0.227, 0.929, 1.0)
            self._glow_col.rgba = (0.486, 0.227, 0.929, 0.28)
            anim = Animation(height=dp(54), d=0.12, t="out_back")
            anim.start(self)
        return super().on_touch_up(touch)


# ---------------------------------------------------------
# Mobile Secondary Button (Dark Cosmic Surface with Lavender Accent)
# ---------------------------------------------------------
class MobileSecondaryButton(ButtonBehavior, BoxLayout):
    """
    Secondary action button with dark cosmic surface, rounded corners (20dp),
    lavender accent text, and smooth touch feedback.
    """
    text = StringProperty("")
    font_size = NumericProperty(dp(15))
    radius = ListProperty([dp(20)])
    is_pressed = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.size_hint_y = None
        self.height = kwargs.get("height", dp(48))
        self.padding = [dp(16), dp(6)]
        self.spacing = dp(8)

        with self.canvas.before:
            # Dark cosmic surface (#1A1835)
            self._bg_col = Color(0.10, 0.09, 0.21, 1.0)
            self._bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=self.radius)

            # Lavender sheen
            self._sheen_col = Color(0.655, 0.545, 0.980, 0.35)
            self._sheen_line = Line(
                rounded_rectangle=(self.x, self.y, self.width, self.height, self.radius[0]),
                width=dp(1.0)
            )

        self.lbl_text = Label(
            text=ar(self.text),
            font_name=FONT_PATH,
            font_size=self.font_size,
            bold=True,
            color=COLOR_ACCENT_PRIMARY,
            halign="center",
            valign="middle"
        )
        self.lbl_text.bind(size=self.lbl_text.setter("text_size"))
        self.add_widget(self.lbl_text)

        self.bind(pos=self._update_canvas, size=self._update_canvas, text=lambda *a: setattr(self.lbl_text, 'text', ar(self.text)))

    def _update_canvas(self, *args):
        r = self.radius[0] if self.radius else dp(20)
        self._bg_rect.pos = self.pos
        self._bg_rect.size = self.size
        self._bg_rect.radius = self.radius
        self._sheen_line.rounded_rectangle = (self.x, self.y, self.width, self.height, r)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.is_pressed = True
            self._bg_col.rgba = (0.16, 0.14, 0.32, 1.0)
            anim = Animation(height=self.height - dp(2), d=0.08)
            anim.start(self)
            return super().on_touch_down(touch)
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        if self.is_pressed:
            self.is_pressed = False
            self._bg_col.rgba = (0.10, 0.09, 0.21, 1.0)
            anim = Animation(height=dp(48), d=0.10)
            anim.start(self)
        return super().on_touch_up(touch)


# ---------------------------------------------------------
# Circular Mobile Touch Button (Borderless Icon Target)
# ---------------------------------------------------------
class MobileIconButton(ButtonBehavior, BoxLayout):
    """
    Modern Android borderless circular touch button (e.g. for AppBar navigation).
    Completely eliminates Windows dialog box frames.
    """
    icon_text = StringProperty("")
    font_size = NumericProperty(dp(18))
    is_pressed = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (dp(42), dp(42))
        self.padding = dp(2)

        with self.canvas.before:
            # Soft circular background
            self._bg_col = Color(0.655, 0.545, 0.980, 0.10)
            self._circle = Ellipse(pos=self.pos, size=self.size)

        self.lbl = Label(
            text=self.icon_text,
            font_size=self.font_size,
            bold=True,
            color=COLOR_TEXT
        )
        self.add_widget(self.lbl)

        self.bind(pos=self._update_canvas, size=self._update_canvas, icon_text=lambda *a: setattr(self.lbl, 'text', self.icon_text))

    def _update_canvas(self, *args):
        self._circle.pos = self.pos
        self._circle.size = self.size

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.is_pressed = True
            self._bg_col.rgba = (0.486, 0.227, 0.929, 0.35)
            anim = Animation(size=(dp(38), dp(38)), d=0.06)
            anim.start(self)
            return super().on_touch_down(touch)
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        if self.is_pressed:
            self.is_pressed = False
            self._bg_col.rgba = (0.655, 0.545, 0.980, 0.10)
            anim = Animation(size=(dp(42), dp(42)), d=0.10, t="out_back")
            anim.start(self)
        return super().on_touch_up(touch)


# ---------------------------------------------------------
# Modern Android Mobile Date Selector (Capsule Stepper)
# ---------------------------------------------------------
class MobileDateStepper(BoxLayout):
    """
    Modern mobile date stepper capsule.
    Replaces Windows-style NumericUpDown / desktop spin buttons with
    a cohesive mobile touch capsule:
    - Soft rounded capsule card
    - Sleek circular '+' and '-' touch targets
    - Prominent bold centered value
    - Integrated Arabic label
    """
    title = StringProperty("")
    value = NumericProperty(1)
    min_val = NumericProperty(1)
    max_val = NumericProperty(31)
    is_month = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.spacing = dp(6)
        self.padding = [dp(6), dp(10)]
        self.size_hint_x = 1.0

        # Background capsule canvas (soft #141328 card with 18dp radius)
        with self.canvas.before:
            Color(rgba=COLOR_CARD_SURFACE)
            self._bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(18)])
            Color(0.24, 0.20, 0.42, 0.40)
            self._border = Line(rounded_rectangle=(self.x, self.y, self.width, self.height, dp(18)), width=dp(1.0))

        self.bind(pos=self._update_canvas, size=self._update_canvas)

        # 1. Top Touch Button: PLUS (+)
        self.btn_plus = BoxLayout(size_hint_y=None, height=dp(34))
        with self.btn_plus.canvas.before:
            Color(0.486, 0.227, 0.929, 0.20)
            self._r_plus = RoundedRectangle(pos=self.btn_plus.pos, size=self.btn_plus.size, radius=[dp(12)])
        self.btn_plus.bind(pos=lambda *a: setattr(self._r_plus, 'pos', self.btn_plus.pos),
                           size=lambda *a: setattr(self._r_plus, 'size', self.btn_plus.size))
        lbl_p = Label(text="+", font_size=dp(20), bold=True, color=COLOR_ACCENT_PRIMARY)
        self.btn_plus.add_widget(lbl_p)
        self.btn_plus.on_touch_down = self._wrap_touch(self.btn_plus, self._increment)
        self.add_widget(self.btn_plus)

        # 2. Middle Value Display & Input
        self.val_box = BoxLayout(orientation="vertical", size_hint_y=None, height=dp(52), spacing=dp(1))
        
        self.lbl_value = Label(
            text=f"{self.value:02d}" if self.value < 100 else str(self.value),
            font_size=dp(22),
            bold=True,
            color=COLOR_TEXT
        )
        self.val_box.add_widget(self.lbl_value)

        # Subtitle (Month Arabic name or unit label)
        self.lbl_sub = Label(
            text=ar(get_arabic_month_name(self.value)) if self.is_month else ar(self.title),
            font_name=FONT_PATH,
            font_size=dp(11),
            color=COLOR_ACCENT_PRIMARY if self.is_month else COLOR_TEXT_MUTED
        )
        self.val_box.add_widget(self.lbl_sub)
        self.add_widget(self.val_box)

        # 3. Bottom Touch Button: MINUS (-)
        self.btn_minus = BoxLayout(size_hint_y=None, height=dp(34))
        with self.btn_minus.canvas.before:
            Color(0.486, 0.227, 0.929, 0.20)
            self._r_minus = RoundedRectangle(pos=self.btn_minus.pos, size=self.btn_minus.size, radius=[dp(12)])
        self.btn_minus.bind(pos=lambda *a: setattr(self._r_minus, 'pos', self.btn_minus.pos),
                            size=lambda *a: setattr(self._r_minus, 'size', self.btn_minus.size))
        lbl_m = Label(text="–", font_size=dp(20), bold=True, color=COLOR_ACCENT_PRIMARY)
        self.btn_minus.add_widget(lbl_m)
        self.btn_minus.on_touch_down = self._wrap_touch(self.btn_minus, self._decrement)
        self.add_widget(self.btn_minus)

        self.bind(value=self._on_value_change)

    def _update_canvas(self, *args):
        self._bg_rect.pos = self.pos
        self._bg_rect.size = self.size
        self._border.rounded_rectangle = (self.x, self.y, self.width, self.height, dp(18))

    def _wrap_touch(self, widget, callback):
        def handler(touch):
            if widget.collide_point(*touch.pos):
                callback()
                return True
            return False
        return handler

    def _increment(self):
        new_val = self.value + 1
        if new_val > self.max_val:
            new_val = self.min_val
        self.value = new_val

    def _decrement(self):
        new_val = self.value - 1
        if new_val < self.min_val:
            new_val = self.max_val
        self.value = new_val

    def _on_value_change(self, instance, val):
        self.lbl_value.text = f"{val:02d}" if val < 100 else str(val)
        if self.is_month:
            self.lbl_sub.text = ar(get_arabic_month_name(val))


# ---------------------------------------------------------
# Modern Android Pill Filter Chip
# ---------------------------------------------------------
class MobileFilterChip(ButtonBehavior, BoxLayout):
    """
    Modern Android pill filter chip with organic capsule shape (18dp),
    active gradient state, and zero desktop window frames.
    """
    text = StringProperty("")
    is_active = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.size_hint_y = None
        self.height = dp(34)
        self.padding = [dp(14), dp(4)]

        with self.canvas.before:
            self._bg_col = Color(0.12, 0.10, 0.24, 0.90)
            self._rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(17)])

        self.lbl = Label(
            text=ar(self.text),
            font_name=FONT_PATH,
            font_size=dp(12),
            bold=True,
            color=COLOR_TEXT_MUTED
        )
        self.lbl.bind(texture_size=lambda _, s: setattr(self, 'width', s[0] + dp(28)))
        self.add_widget(self.lbl)

        self.bind(pos=self._update_canvas, size=self._update_canvas, text=self._update_text, is_active=self._update_active)

    def _update_canvas(self, *args):
        self._rect.pos = self.pos
        self._rect.size = self.size

    def _update_text(self, *args):
        self.lbl.text = ar(self.text)

    def _update_active(self, *args):
        if self.is_active:
            self._bg_col.rgba = (0.486, 0.227, 0.929, 1.0)
            self.lbl.color = COLOR_TEXT
        else:
            self._bg_col.rgba = (0.12, 0.10, 0.24, 0.90)
            self.lbl.color = COLOR_TEXT_MUTED


# ---------------------------------------------------------
# Animated Count-up Label for Total Days Lived
# ---------------------------------------------------------
class AnimatedCountLabel(Label):
    """
    Counts up smoothly from 0 to target value with cubic ease-out.
    """
    current_val = NumericProperty(0)
    target_val = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_size = kwargs.get("font_size", dp(36))
        self.bold = True
        self.color = COLOR_ACCENT_PRIMARY
        self._elapsed = 0.0
        self._duration = 1.2
        self._clock_ev = None
        self.text = "0"

    def count_to(self, target, duration=1.2):
        if self._clock_ev:
            self._clock_ev.cancel()

        self.target_val = int(target)
        self._duration = duration
        self._elapsed = 0.0
        self.current_val = 0
        self.text = "0"
        self._clock_ev = Clock.schedule_interval(self._tick, 1.0 / 60.0)

    def _tick(self, dt):
        self._elapsed += dt
        progress = min(1.0, self._elapsed / self._duration)
        ease = 1.0 - (1.0 - progress) ** 3
        val = int(ease * self.target_val)
        self.current_val = val
        self.text = f"{val:,}"

        if progress >= 1.0:
            self.text = f"{self.target_val:,}"
            if self._clock_ev:
                self._clock_ev.cancel()
                self._clock_ev = None


# ---------------------------------------------------------
# Live Birthday Countdown Widget (Days, Hours, Minutes, Seconds)
# ---------------------------------------------------------
class LiveCountdownWidget(BoxLayout):
    """
    Real-time ticking digital countdown timer with 4 modern mobile sub-cards.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.spacing = dp(8)
        self.size_hint_y = None
        self.height = dp(74)

        # 4 boxes for Days, Hours, Minutes, Seconds (in RTL order: Days on right)
        self.box_days, self.lbl_days = self._create_unit_box("أيام")
        self.box_hours, self.lbl_hours = self._create_unit_box("ساعات")
        self.box_mins, self.lbl_mins = self._create_unit_box("دقائق")
        self.box_secs, self.lbl_secs = self._create_unit_box("ثواني")

        self.add_widget(self.box_secs)
        self.add_widget(self.box_mins)
        self.add_widget(self.box_hours)
        self.add_widget(self.box_days)

    def _create_unit_box(self, label_text):
        box = BoxLayout(orientation="vertical", spacing=dp(2), padding=[dp(4), dp(8)])
        with box.canvas.before:
            Color(0.08, 0.075, 0.17, 1.0)
            rect = RoundedRectangle(pos=box.pos, size=box.size, radius=[dp(14)])
            Color(0.24, 0.20, 0.44, 0.40)
            line = Line(rounded_rectangle=(0, 0, 10, 10, dp(14)), width=dp(1.0))

        box.bind(pos=lambda *a: [setattr(rect, 'pos', box.pos),
                                 setattr(line, 'rounded_rectangle', (box.x, box.y, box.width, box.height, dp(14)))],
                 size=lambda *a: [setattr(rect, 'size', box.size),
                                  setattr(line, 'rounded_rectangle', (box.x, box.y, box.width, box.height, dp(14)))])

        lbl_val = Label(
            text="00",
            font_size=dp(21),
            bold=True,
            color=COLOR_TEXT
        )
        lbl_unit = Label(
            text=ar(label_text),
            font_name=FONT_PATH,
            font_size=dp(11),
            color=COLOR_TEXT_MUTED
        )
        box.add_widget(lbl_val)
        box.add_widget(lbl_unit)
        return box, lbl_val

    def set_time(self, days, hours, minutes, seconds):
        self.lbl_days.text = f"{days:03d}"
        self.lbl_hours.text = f"{hours:02d}"
        self.lbl_mins.text = f"{minutes:02d}"
        self.lbl_secs.text = f"{seconds:02d}"


# ---------------------------------------------------------
# Astrological Element Pill Badge
# ---------------------------------------------------------
class ElementPillBadge(BoxLayout):
    """
    Organic mobile pill badge for astrological element (ناري, ترابي, هوائي, مائي)
    with custom vibrant coloring and zero boxy desktop borders.
    """
    text = StringProperty("")
    badge_color = ListProperty([0.486, 0.227, 0.929, 1.0])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.size_hint = (None, None)
        self.height = dp(28)
        self.padding = [dp(12), dp(4)]

        with self.canvas.before:
            self._bg_col = Color(rgba=(self.badge_color[0], self.badge_color[1], self.badge_color[2], 0.24))
            self._rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(14)])

        self.lbl = Label(
            text=ar(self.text),
            font_name=FONT_PATH,
            font_size=dp(12),
            bold=True,
            color=COLOR_TEXT
        )
        self.lbl.bind(texture_size=self._update_width)
        self.add_widget(self.lbl)

        self.bind(pos=self._update_canvas, size=self._update_canvas, text=self._update_text, badge_color=self._update_color)

    def _update_width(self, instance, val):
        self.width = val[0] + dp(24)

    def _update_text(self, *args):
        self.lbl.text = ar(self.text)

    def _update_color(self, *args):
        c = self.badge_color
        self._bg_col.rgba = (c[0], c[1], c[2], 0.24)

    def _update_canvas(self, *args):
        self._rect.pos = self.pos
        self._rect.size = self.size


# ---------------------------------------------------------
# Floating Animated Toast Notification
# ---------------------------------------------------------
class CosmicToast(BoxLayout):
    """
    Floating animated toast capsule notification for clipboard share and actions.
    """
    @classmethod
    def show(cls, parent_widget, message):
        toast = CosmicToast(message)
        parent_widget.add_widget(toast)
        toast.pos_hint = {"center_x": 0.5, "y": 0.08}
        toast.opacity = 0

        anim = (
            Animation(opacity=1, d=0.22, t="out_quad")
            + Animation(d=2.0)
            + Animation(opacity=0, d=0.30, t="in_quad")
        )

        def _finish(*args):
            if toast.parent:
                toast.parent.remove_widget(toast)

        anim.bind(on_complete=_finish)
        anim.start(toast)

    def __init__(self, message, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.size_hint = (None, None)
        self.height = dp(44)
        self.padding = [dp(20), dp(8)]

        with self.canvas.before:
            Color(0.12, 0.10, 0.26, 0.95)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(22)])
            Color(0.655, 0.545, 0.980, 0.6)
            self.line = Line(rounded_rectangle=(0, 0, 10, 10, dp(22)), width=dp(1.0))

        self.bind(pos=lambda *a: [setattr(self.rect, 'pos', self.pos),
                                  setattr(self.line, 'rounded_rectangle', (self.x, self.y, self.width, self.height, dp(22)))],
                 size=lambda *a: [setattr(self.rect, 'size', self.size),
                                  setattr(self.line, 'rounded_rectangle', (self.x, self.y, self.width, self.height, dp(22)))])

        lbl = Label(
            text=ar(message),
            font_name=FONT_PATH,
            font_size=dp(13),
            bold=True,
            color=COLOR_TEXT
        )
        lbl.bind(texture_size=lambda _, s: setattr(self, 'width', s[0] + dp(40)))
        self.add_widget(lbl)


# ---------------------------------------------------------
# Modern Android Bottom-Sheet Modal (Zodiac Sign Profile)
# ---------------------------------------------------------
class ZodiacDetailModal(ModalView):
    """
    Modern Android bottom-sheet modal showing complete astrological profile.
    Replaces desktop-style popup windows.
    """
    def __init__(self, sign_dict, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (0.94, 0.84)
        self.auto_dismiss = True
        self.background_color = (0, 0, 0, 0.72)

        card = ModernMobileCard(orientation="vertical", padding=dp(18), spacing=dp(12))

        # Top Drag Handle Indicator
        handle_bar = BoxLayout(size_hint=(None, None), size=(dp(44), dp(5)), pos_hint={"center_x": 0.5})
        with handle_bar.canvas.before:
            Color(0.35, 0.32, 0.52, 0.8)
            r_h = RoundedRectangle(pos=handle_bar.pos, size=handle_bar.size, radius=[dp(3)])
        handle_bar.bind(pos=lambda *a: setattr(r_h, 'pos', handle_bar.pos),
                        size=lambda *a: setattr(r_h, 'size', handle_bar.size))
        card.add_widget(handle_bar)

        # Header Row
        header = BoxLayout(orientation="horizontal", size_hint_y=None, height=dp(58), spacing=dp(12))

        # Circular Close Button
        btn_close = MobileIconButton(icon_text="✕", font_size=dp(14))
        btn_close.on_release = self.dismiss
        header.add_widget(btn_close)

        # Title Info
        info_col = BoxLayout(orientation="vertical", spacing=dp(2))
        lbl_name = Label(
            text=ar(f"برج {sign_dict['name']}  ({sign_dict['name_en']})"),
            font_name=FONT_PATH,
            font_size=dp(19),
            bold=True,
            color=COLOR_TEXT,
            halign="right"
        )
        lbl_name.bind(size=lbl_name.setter("text_size"))

        lbl_dates = Label(
            text=ar(sign_dict["date_range"]),
            font_name=FONT_PATH,
            font_size=dp(12),
            color=COLOR_TEXT_MUTED,
            halign="right"
        )
        lbl_dates.bind(size=lbl_dates.setter("text_size"))
        info_col.add_widget(lbl_name)
        info_col.add_widget(lbl_dates)
        header.add_widget(info_col)

        # Symbol Badge
        sym_box = BoxLayout(size_hint=(None, None), size=(dp(54), dp(54)))
        with sym_box.canvas.before:
            Color(0.20, 0.16, 0.38, 0.9)
            r_s = RoundedRectangle(pos=sym_box.pos, size=sym_box.size, radius=[dp(27)])
        sym_box.bind(pos=lambda *a: setattr(r_s, 'pos', sym_box.pos),
                     size=lambda *a: setattr(r_s, 'size', sym_box.size))
        lbl_sym = Label(text=sign_dict["symbol"], font_size=dp(28), bold=True, color=COLOR_TEXT)
        sym_box.add_widget(lbl_sym)
        header.add_widget(sym_box)

        card.add_widget(header)

        # Scrollable content for details
        scroll = ScrollView(do_scroll_x=False, bar_width=dp(3))
        content = BoxLayout(orientation="vertical", spacing=dp(12), size_hint_y=None)
        content.bind(minimum_height=content.setter("height"))

        # Pills row (Element + Planet)
        pills_row = BoxLayout(orientation="horizontal", size_hint_y=None, height=dp(30), spacing=dp(8))
        pill_elem = ElementPillBadge(
            text=f"{sign_dict['element_icon']} {sign_dict['element']}",
            badge_color=sign_dict["element_color"]
        )
        pill_planet = ElementPillBadge(
            text=f"كوكب: {sign_dict['planet']}",
            badge_color=COLOR_ACCENT_PRIMARY
        )
        pills_row.add_widget(Widget())
        pills_row.add_widget(pill_planet)
        pills_row.add_widget(pill_elem)
        content.add_widget(pills_row)

        content.add_widget(self._create_section("الوصف والتحليل الفلكي", sign_dict["description"]))
        traits_text = " • ".join(sign_dict["traits"])
        content.add_widget(self._create_section("أبرز الصفات", traits_text))
        content.add_widget(self._create_section("نقاط القوة", sign_dict["strengths"]))
        content.add_widget(self._create_section("التحديات", sign_dict["challenges"]))
        comp_text = " ، ".join(sign_dict["compatibility"])
        content.add_widget(self._create_section("الأبراج الأكثر توافقاً", comp_text))
        lucky_text = f"الأرقام: {sign_dict['lucky_numbers']}  |  اللون المفضل: {sign_dict['lucky_color']}"
        content.add_widget(self._create_section("أسرار الحظ", lucky_text))

        scroll.add_widget(content)
        card.add_widget(scroll)

        # Modern close button at bottom
        btn_done = ModernMobileButton(text="إغلاق", height=dp(46), radius=[dp(18)])
        btn_done.on_release = self.dismiss
        card.add_widget(btn_done)

        self.add_widget(card)

    def _create_section(self, title, body):
        box = BoxLayout(orientation="vertical", size_hint_y=None, spacing=dp(4))
        lbl_t = Label(
            text=ar(title),
            font_name=FONT_PATH,
            font_size=dp(13),
            bold=True,
            color=COLOR_ACCENT_PRIMARY,
            size_hint_y=None,
            height=dp(20),
            halign="right"
        )
        lbl_t.bind(size=lbl_t.setter("text_size"))

        lbl_b = Label(
            text=ar(body),
            font_name=FONT_PATH,
            font_size=dp(13),
            color=COLOR_TEXT,
            size_hint_y=None,
            halign="right"
        )
        lbl_b.bind(width=lambda *a: setattr(lbl_b, 'text_size', (lbl_b.width, None)),
                   texture_size=lambda *a: setattr(lbl_b, 'height', lbl_b.texture_size[1]))

        box.add_widget(lbl_t)
        box.add_widget(lbl_b)
        box.bind(minimum_height=box.setter("height"))
        return box
