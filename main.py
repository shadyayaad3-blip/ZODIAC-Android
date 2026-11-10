# -*- coding: utf-8 -*-
"""
ZODIAC - Premium Astrology & Birthday Calculator
Modern Android Mobile UI Redesign.
Features:
- Official ZODIAC Branding (from supplied SVG logo)
- 100% Mobile-First Android Touch UI (No desktop window borders)
- Modern Rounded Purple Gradient Buttons (16-22dp radius)
- Living Animated Cosmic Background (Twinkling stars & Nebulae)
- Arabic RTL Text Reshaping
- Animated Count-Up for Total Days Lived
- Live Ticking Countdown for Next Birthday
- Full 12 Signs Directory with Android Bottom-Sheet Modals
- Settings Screen & Clipboard Share
"""

from datetime import date, datetime
import calendar
import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from kivy.app import App
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.clipboard import Clipboard
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.properties import BooleanProperty, NumericProperty, ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition, FadeTransition
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle, Line, Rectangle, Ellipse

import zodiac_data
from zodiac_data import (
    ar,
    calculate_age,
    get_zodiac,
    get_zodiac_full,
    next_month,
    ALL_ZODIAC_SIGNS,
    format_arabic_date,
    get_arabic_month_name,
    SIGNS
)
from ui_components import (
    COLOR_BG_MAIN,
    COLOR_BG_SEC,
    COLOR_CARD,
    COLOR_CARD_SURFACE,
    COLOR_ACCENT_PRIMARY,
    COLOR_ACCENT_SEC,
    COLOR_TEXT,
    COLOR_TEXT_MUTED,
    CosmicBackground,
    ModernMobileCard,
    ModernMobileButton,
    MobileSecondaryButton,
    MobileIconButton,
    MobileDateStepper,
    MobileFilterChip,
    AnimatedCountLabel,
    LiveCountdownWidget,
    ElementPillBadge,
    CosmicToast,
    ZodiacDetailModal,
    FONT_PATH,
    LOGO_PATH,
    LOGO_FULL_PATH,
    ICON_PATH
)

# Standard mobile phone aspect ratio for desktop preview
Window.size = (420, 780)
Window.clearcolor = COLOR_BG_MAIN


# ---------------------------------------------------------
# Modern Android App Bar (TopBar)
# ---------------------------------------------------------
class TopBar(BoxLayout):
    """
    Modern Android App Bar with official logo mark, borderless circular
    touch targets, and clean centered title. No Windows dialog borders.
    """
    title = StringProperty("")
    show_back = BooleanProperty(False)
    show_settings = BooleanProperty(False)
    show_signs = BooleanProperty(False)
    show_share = BooleanProperty(False)
    show_logo = BooleanProperty(True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.size_hint_y = None
        self.height = dp(58)
        self.padding = [dp(14), dp(8)]
        self.spacing = dp(8)

        # Subtle dark translucent bar background (no harsh borders)
        with self.canvas.before:
            Color(0.04, 0.04, 0.10, 0.88)
            self.rect = Rectangle(pos=self.pos, size=self.size)

        self.bind(pos=self._update_canvas, size=self._update_canvas)

        self.on_nav_back = None
        self.on_nav_settings = None
        self.on_nav_signs = None
        self.on_nav_share = None

        self._build_bar()

    def _update_canvas(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def _build_bar(self):
        self.clear_widgets()

        # Left action target (Back or Settings)
        if self.show_back:
            btn_back = MobileIconButton(icon_text="←", font_size=dp(20))
            btn_back.on_release = self._handle_back
            self.add_widget(btn_back)
        elif self.show_settings:
            btn_set = MobileIconButton(icon_text="⚙", font_size=dp(18))
            btn_set.on_release = self._handle_settings
            self.add_widget(btn_set)
        else:
            self.add_widget(Widget(size_hint=(None, None), size=(dp(42), dp(42))))

        # Center Title & Branding
        center_box = BoxLayout(orientation="horizontal", spacing=dp(6), pos_hint={"center_y": 0.5})
        center_box.add_widget(Widget())  # Spacer

        if self.show_logo and os.path.exists(LOGO_PATH):
            logo_img = Image(
                source=LOGO_PATH,
                size_hint=(None, None),
                size=(dp(28), dp(28)),
                allow_stretch=True,
                keep_ratio=True
            )
            center_box.add_widget(logo_img)

        self.lbl_title = Label(
            text=ar(self.title),
            font_name=FONT_PATH,
            font_size=dp(17),
            bold=True,
            color=COLOR_TEXT,
            size_hint_x=None
        )
        self.lbl_title.bind(texture_size=lambda _, s: setattr(self.lbl_title, 'width', s[0]))
        self.bind(title=lambda *a: setattr(self.lbl_title, 'text', ar(self.title)))
        center_box.add_widget(self.lbl_title)

        center_box.add_widget(Widget())  # Spacer
        self.add_widget(center_box)

        # Right action target (Share, Signs chip, or Spacer)
        if self.show_share:
            btn_share = MobileIconButton(icon_text="✦", font_size=dp(18))
            btn_share.on_release = self._handle_share
            self.add_widget(btn_share)
        elif self.show_signs:
            btn_signs = MobileFilterChip(text="الأبراج", height=dp(34), is_active=True)
            btn_signs.on_release = self._handle_signs
            self.add_widget(btn_signs)
        else:
            self.add_widget(Widget(size_hint=(None, None), size=(dp(42), dp(42))))

    def _handle_back(self):
        if self.on_nav_back:
            self.on_nav_back()

    def _handle_settings(self):
        if self.on_nav_settings:
            self.on_nav_settings()

    def _handle_signs(self):
        if self.on_nav_signs:
            self.on_nav_signs()

    def _handle_share(self):
        if self.on_nav_share:
            self.on_nav_share()


# ---------------------------------------------------------
# 1. Welcome / Splash Screen with Official Logo
# ---------------------------------------------------------
class SplashScreen(Screen):
    """
    Cosmic welcome splash screen proudly displaying the user's official
    ZODIAC logo, pulsing ambient glow, and smooth progress transition.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bg = CosmicBackground()
        self.add_widget(self.bg)

        center_box = BoxLayout(
            orientation="vertical",
            size_hint=(0.88, None),
            spacing=dp(16),
            pos_hint={"center_x": 0.5, "center_y": 0.52}
        )
        center_box.bind(minimum_height=center_box.setter("height"))

        # Official Logo Image (Zero crop, zero distortion)
        self.logo_widget = Image(
            source=LOGO_PATH if os.path.exists(LOGO_PATH) else "",
            size_hint=(None, None),
            size=(dp(250), dp(225)),
            pos_hint={"center_x": 0.5},
            allow_stretch=True,
            keep_ratio=True
        )
        center_box.add_widget(self.logo_widget)

        # Arabic Subtitle
        lbl_sub = Label(
            text=ar("اكتشف أسرار الكون وتاريخك الفلكي"),
            font_name=FONT_PATH,
            font_size=dp(15),
            color=COLOR_TEXT_MUTED,
            size_hint_y=None,
            height=dp(26),
            halign="center"
        )
        center_box.add_widget(lbl_sub)

        # Ambient Progress Capsule
        self.prog_container = BoxLayout(size_hint_y=None, height=dp(5), size_hint_x=0.65, pos_hint={"center_x": 0.5})
        with self.prog_container.canvas.before:
            Color(0.12, 0.10, 0.22, 1.0)
            self.prog_bg = RoundedRectangle(pos=self.prog_container.pos, size=self.prog_container.size, radius=[dp(3)])
            Color(0.655, 0.545, 0.980, 1.0)
            self.prog_bar = RoundedRectangle(pos=self.prog_container.pos, size=(0, dp(5)), radius=[dp(3)])

        self.prog_container.bind(
            pos=lambda *a: setattr(self.prog_bg, 'pos', self.prog_container.pos),
            size=lambda *a: setattr(self.prog_bg, 'size', self.prog_container.size)
        )
        center_box.add_widget(self.prog_container)

        self.add_widget(center_box)

        # Skip indicator at bottom
        lbl_skip = Label(
            text=ar("انقر للمتابعة"),
            font_name=FONT_PATH,
            font_size=dp(12),
            color=(0.55, 0.52, 0.72, 0.75),
            size_hint=(None, None),
            size=(dp(200), dp(28)),
            pos_hint={"center_x": 0.5, "y": 0.04}
        )
        self.add_widget(lbl_skip)

        self._progress = 0.0
        self._anim_ev = None

    def on_enter(self):
        self._progress = 0.0
        self._anim_ev = Clock.schedule_interval(self._tick_progress, 1.0 / 40.0)

        # Gentle breathing animation on logo
        anim_pulse = (
            Animation(size=(dp(258), dp(232)), d=0.9, t="in_out_quad")
            + Animation(size=(dp(250), dp(225)), d=0.9, t="in_out_quad")
        )
        anim_pulse.repeat = True
        anim_pulse.start(self.logo_widget)

    def _tick_progress(self, dt):
        self._progress += dt / 1.5
        w = min(1.0, self._progress) * self.prog_container.width
        self.prog_bar.pos = self.prog_container.pos
        self.prog_bar.size = (w, dp(5))

        if self._progress >= 1.0:
            if self._anim_ev:
                self._anim_ev.cancel()
                self._anim_ev = None
            self.go_main()

    def go_main(self):
        if self._anim_ev:
            self._anim_ev.cancel()
            self._anim_ev = None
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = "main"

    def on_touch_down(self, touch):
        self.go_main()
        return True


# ---------------------------------------------------------
# 2. Main Screen (Mobile-First Birthday Input)
# ---------------------------------------------------------
class MainScreen(Screen):
    """
    Main mobile screen with official ZODIAC branding, modern Android
    capsule date steppers, and large rounded purple gradient button.
    Zero Windows desktop appearance.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bg = CosmicBackground()
        self.add_widget(self.bg)

        root = BoxLayout(orientation="vertical")

        # Top Bar
        self.top_bar = TopBar(
            title="ZODIAC",
            show_settings=True,
            show_signs=True,
            show_logo=True
        )
        self.top_bar.on_nav_settings = self.go_settings
        self.top_bar.on_nav_signs = self.go_all_signs
        root.add_widget(self.top_bar)

        # Scrollable Body
        scroll = ScrollView(do_scroll_x=False, bar_width=dp(2))
        content = BoxLayout(
            orientation="vertical",
            spacing=dp(16),
            padding=[dp(16), dp(12), dp(16), dp(24)],
            size_hint_y=None
        )
        content.bind(minimum_height=content.setter("height"))

        # Official Logo Brand Banner
        brand_box = BoxLayout(orientation="vertical", spacing=dp(4), size_hint_y=None)
        brand_box.bind(minimum_height=brand_box.setter("height"))

        if os.path.exists(LOGO_PATH):
            logo_hero = Image(
                source=LOGO_PATH,
                size_hint=(None, None),
                size=(dp(160), dp(144)),
                pos_hint={"center_x": 0.5},
                allow_stretch=True,
                keep_ratio=True
            )
            brand_box.add_widget(logo_hero)

        lbl_hero = Label(
            text=ar("اكتشف عالمك الفلكي"),
            font_name=FONT_PATH,
            font_size=dp(23),
            bold=True,
            color=COLOR_TEXT,
            size_hint_y=None,
            height=dp(34),
            halign="center"
        )
        lbl_hero.bind(size=lbl_hero.setter("text_size"))

        lbl_sub = Label(
            text=ar("أدخل تاريخ ميلادك لتكشف تفاصيل عمرك الدقيقة، برجك الفلكي، وصفاتك الكونية"),
            font_name=FONT_PATH,
            font_size=dp(13),
            color=COLOR_TEXT_MUTED,
            size_hint_y=None,
            halign="center"
        )
        lbl_sub.bind(width=lambda *a: setattr(lbl_sub, 'text_size', (lbl_sub.width, None)),
                     texture_size=lambda *a: setattr(lbl_sub, 'height', lbl_sub.texture_size[1]))

        brand_box.add_widget(lbl_hero)
        brand_box.add_widget(lbl_sub)
        content.add_widget(brand_box)

        # Modern Mobile Birthday Input Card
        input_card = ModernMobileCard(orientation="vertical", padding=dp(18), spacing=dp(14), size_hint_y=None)
        input_card.bind(minimum_height=input_card.setter("height"))

        # Card Header
        header_row = BoxLayout(orientation="horizontal", size_hint_y=None, height=dp(26), spacing=dp(8))
        lbl_card_title = Label(
            text=ar("تاريخ الميلاد"),
            font_name=FONT_PATH,
            font_size=dp(15),
            bold=True,
            color=COLOR_ACCENT_PRIMARY,
            halign="right"
        )
        lbl_card_title.bind(size=lbl_card_title.setter("text_size"))
        lbl_icon = Label(text="📅", font_size=dp(16), size_hint_x=None, width=dp(24))
        header_row.add_widget(lbl_card_title)
        header_row.add_widget(lbl_icon)
        input_card.add_widget(header_row)

        # 3 Mobile Capsule Steppers (RTL: Right = Day, Center = Month, Left = Year)
        steppers_row = BoxLayout(orientation="horizontal", spacing=dp(8), size_hint_y=None, height=dp(144))

        today = date.today()
        # Left: Year
        self.step_year = MobileDateStepper(
            title="السنة",
            value=2000,
            min_val=1920,
            max_val=today.year
        )
        # Center: Month
        self.step_month = MobileDateStepper(
            title="الشهر",
            value=today.month,
            min_val=1,
            max_val=12,
            is_month=True
        )
        # Right: Day
        self.step_day = MobileDateStepper(
            title="اليوم",
            value=today.day,
            min_val=1,
            max_val=31
        )

        steppers_row.add_widget(self.step_year)
        steppers_row.add_widget(self.step_month)
        steppers_row.add_widget(self.step_day)
        input_card.add_widget(steppers_row)

        # Quick "Today" Pill Helper
        helpers_row = BoxLayout(orientation="horizontal", size_hint_y=None, height=dp(32))
        helpers_row.add_widget(Widget())  # Spacer
        btn_today = MobileFilterChip(text="اليوم الحالي ↺", height=dp(30))
        btn_today.on_release = self._set_today
        helpers_row.add_widget(btn_today)
        input_card.add_widget(helpers_row)

        # Error Alert Banner
        self.lbl_error = Label(
            text="",
            font_name=FONT_PATH,
            font_size=dp(12),
            color=(0.95, 0.40, 0.40, 1.0),
            size_hint_y=None,
            height=0,
            halign="center"
        )
        self.lbl_error.bind(size=self.lbl_error.setter("text_size"))
        input_card.add_widget(self.lbl_error)

        # Large Rounded Purple Gradient Button (20dp radius, ambient purple glow)
        self.btn_submit = ModernMobileButton(
            text="اكتشف عالمك",
            height=dp(54),
            radius=[dp(20)]
        )
        self.btn_submit.on_release = self.calculate_and_navigate
        input_card.add_widget(self.btn_submit)

        content.add_widget(input_card)

        # Explore All 12 Signs Card
        explore_card = ModernMobileCard(orientation="vertical", padding=dp(16), spacing=dp(10), size_hint_y=None)
        explore_card.bind(minimum_height=explore_card.setter("height"))

        exp_header = BoxLayout(orientation="horizontal", size_hint_y=None, height=dp(24), spacing=dp(8))
        lbl_exp_title = Label(
            text=ar("دليل الأبراج الفلكية الـ 12"),
            font_name=FONT_PATH,
            font_size=dp(14),
            bold=True,
            color=COLOR_TEXT,
            halign="right"
        )
        lbl_exp_title.bind(size=lbl_exp_title.setter("text_size"))
        lbl_exp_icon = Label(text="✨", font_size=dp(14), size_hint_x=None, width=dp(20))
        exp_header.add_widget(lbl_exp_title)
        exp_header.add_widget(lbl_exp_icon)
        explore_card.add_widget(exp_header)

        lbl_exp_desc = Label(
            text=ar("تعرف على تفاصيل وصفات وتوافق جميع الأبراج: النارية والترابية والهوائية والمائية"),
            font_name=FONT_PATH,
            font_size=dp(12),
            color=COLOR_TEXT_MUTED,
            size_hint_y=None,
            halign="right"
        )
        lbl_exp_desc.bind(width=lambda *a: setattr(lbl_exp_desc, 'text_size', (lbl_exp_desc.width, None)),
                          texture_size=lambda *a: setattr(lbl_exp_desc, 'height', lbl_exp_desc.texture_size[1]))
        explore_card.add_widget(lbl_exp_desc)

        btn_view_signs = MobileSecondaryButton(text="تصفح جميع الأبراج", height=dp(44), radius=[dp(18)])
        btn_view_signs.on_release = self.go_all_signs
        explore_card.add_widget(btn_view_signs)

        content.add_widget(explore_card)

        # Footer branding
        lbl_footer = Label(
            text="ZODIAC  •  PREMIUM COSMIC ASTROLOGY",
            font_size=dp(10),
            color=(0.50, 0.45, 0.70, 0.70),
            size_hint_y=None,
            height=dp(26)
        )
        content.add_widget(lbl_footer)

        scroll.add_widget(content)
        root.add_widget(scroll)
        self.add_widget(root)

    def _set_today(self):
        t = date.today()
        self.step_day.value = t.day
        self.step_month.value = t.month
        self.step_year.value = t.year
        self._clear_error()

    def _show_error(self, message):
        self.lbl_error.text = ar(message)
        self.lbl_error.height = dp(24)

    def _clear_error(self):
        self.lbl_error.text = ""
        self.lbl_error.height = 0

    def calculate_and_navigate(self):
        day = self.step_day.value
        month = self.step_month.value
        year = self.step_year.value

        try:
            birthday = date(year, month, day)
        except ValueError:
            self._show_error("تاريخ الميلاد غير صحيح، راجع اليوم والشهر")
            return

        today = date.today()
        if birthday > today:
            self._show_error("تاريخ الميلاد لا يمكن أن يكون في المستقبل!")
            return

        self._clear_error()

        years, months, days = calculate_age(birthday, today)
        total_days = (today - birthday).days
        sign_info = get_zodiac_full(day, month)

        results_screen = self.manager.get_screen("results")
        results_screen.load_data(birthday, years, months, days, total_days, sign_info)

        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = "results"

    def go_settings(self):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = "settings"

    def go_all_signs(self):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = "all_signs"


# ---------------------------------------------------------
# 3. Results Dashboard Screen
# ---------------------------------------------------------
class ResultsScreen(Screen):
    """
    Modern mobile results dashboard with official branding, large zodiac symbol,
    animated count-up for total days, live countdown timer, and action buttons.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bg = CosmicBackground()
        self.add_widget(self.bg)

        self.selected_birthday = None
        self.sign_info = None
        self.years = 0
        self.months = 0
        self.days = 0
        self.total_days = 0
        self._countdown_timer = None

        root = BoxLayout(orientation="vertical")

        # Top Bar
        self.top_bar = TopBar(
            title="تحليلك الفلكي",
            show_back=True,
            show_share=True,
            show_logo=True
        )
        self.top_bar.on_nav_back = self.reset_and_back
        self.top_bar.on_nav_share = self.share_results
        root.add_widget(self.top_bar)

        self.scroll = ScrollView(do_scroll_x=False, bar_width=dp(2))
        self.content = BoxLayout(
            orientation="vertical",
            spacing=dp(14),
            padding=[dp(16), dp(12), dp(16), dp(24)],
            size_hint_y=None
        )
        self.content.bind(minimum_height=self.content.setter("height"))

        # 1. Zodiac Hero Card
        self.hero_card = ModernMobileCard(orientation="vertical", padding=dp(18), spacing=dp(10), size_hint_y=None)
        self.hero_card.bind(minimum_height=self.hero_card.setter("height"))

        # Glowing circular badge for Zodiac Symbol
        badge_container = FloatLayout(size_hint=(None, None), size=(dp(82), dp(82)), pos_hint={"center_x": 0.5})
        with badge_container.canvas.before:
            Color(0.486, 0.227, 0.929, 0.28)
            self.hero_halo = Ellipse(pos=(0, 0), size=(dp(82), dp(82)))
            Color(0.12, 0.10, 0.26, 0.95)
            self.hero_inner = Ellipse(pos=(dp(5), dp(5)), size=(dp(72), dp(72)))

        badge_container.bind(
            pos=lambda *a: [
                setattr(self.hero_halo, 'pos', badge_container.pos),
                setattr(self.hero_inner, 'pos', (badge_container.x + dp(5), badge_container.y + dp(5)))
            ]
        )

        self.lbl_hero_symbol = Label(
            text="♈",
            font_size=dp(40),
            bold=True,
            color=COLOR_TEXT,
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        badge_container.add_widget(self.lbl_hero_symbol)
        self.hero_card.add_widget(badge_container)

        self.lbl_sign_name = Label(
            text=ar("برج الحمل"),
            font_name=FONT_PATH,
            font_size=dp(22),
            bold=True,
            color=COLOR_TEXT,
            size_hint_y=None,
            height=dp(32),
            halign="center"
        )
        self.hero_card.add_widget(self.lbl_sign_name)

        self.lbl_date_range = Label(
            text=ar("21 مارس - 19 أبريل"),
            font_name=FONT_PATH,
            font_size=dp(13),
            color=COLOR_TEXT_MUTED,
            size_hint_y=None,
            height=dp(20),
            halign="center"
        )
        self.hero_card.add_widget(self.lbl_date_range)

        # Element & Planet Pills
        self.pills_row = BoxLayout(orientation="horizontal", size_hint_y=None, height=dp(30), spacing=dp(8))
        self.pill_element = ElementPillBadge(text="🔥 ناري", badge_color=(0.97, 0.44, 0.44, 1.0))
        self.pill_planet = ElementPillBadge(text="كوكب: المريخ", badge_color=COLOR_ACCENT_PRIMARY)
        self.pills_row.add_widget(Widget())
        self.pills_row.add_widget(self.pill_planet)
        self.pills_row.add_widget(self.pill_element)
        self.hero_card.add_widget(self.pills_row)

        self.content.add_widget(self.hero_card)

        # 2. Birthday & Age Breakdown Card
        self.age_card = ModernMobileCard(orientation="vertical", padding=dp(18), spacing=dp(10), size_hint_y=None)
        self.age_card.bind(minimum_height=self.age_card.setter("height"))

        lbl_age_sec_title = Label(
            text=ar("عمرك الحالي بالتفصيل"),
            font_name=FONT_PATH,
            font_size=dp(14),
            bold=True,
            color=COLOR_ACCENT_PRIMARY,
            size_hint_y=None,
            height=dp(20),
            halign="center"
        )
        self.age_card.add_widget(lbl_age_sec_title)

        self.lbl_big_age = Label(
            text="28 سنة",
            font_name=FONT_PATH,
            font_size=dp(26),
            bold=True,
            color=COLOR_TEXT,
            size_hint_y=None,
            height=dp(36),
            halign="center"
        )
        self.age_card.add_widget(self.lbl_big_age)

        # 3 Mobile Sub-cards (Years, Months, Days)
        age_metrics_row = BoxLayout(orientation="horizontal", spacing=dp(8), size_hint_y=None, height=dp(54))
        self.box_y_val, self.lbl_y_val = self._create_metric_box("سنوات")
        self.box_m_val, self.lbl_m_val = self._create_metric_box("أشهر")
        self.box_d_val, self.lbl_d_val = self._create_metric_box("أيام")

        # In RTL display: Years on right
        age_metrics_row.add_widget(self.box_d_val)
        age_metrics_row.add_widget(self.box_m_val)
        age_metrics_row.add_widget(self.box_y_val)
        self.age_card.add_widget(age_metrics_row)

        self.lbl_birth_date = Label(
            text=ar("تاريخ الميلاد: 15 مايو 1996"),
            font_name=FONT_PATH,
            font_size=dp(13),
            color=COLOR_TEXT_MUTED,
            size_hint_y=None,
            height=dp(22),
            halign="center"
        )
        self.age_card.add_widget(self.lbl_birth_date)

        self.content.add_widget(self.age_card)

        # 3. Total Days Lived Card with Count-up Animation
        self.days_card = ModernMobileCard(orientation="vertical", padding=dp(18), spacing=dp(8), size_hint_y=None)
        self.days_card.bind(minimum_height=self.days_card.setter("height"))

        lbl_days_title = Label(
            text=ar("إجمالي الأيام التي عشتها"),
            font_name=FONT_PATH,
            font_size=dp(14),
            bold=True,
            color=COLOR_ACCENT_PRIMARY,
            size_hint_y=None,
            height=dp(20),
            halign="center"
        )
        self.days_card.add_widget(lbl_days_title)

        self.lbl_animated_days = AnimatedCountLabel(font_size=dp(34))
        self.days_card.add_widget(self.lbl_animated_days)

        self.lbl_days_sub = Label(
            text=ar("آلاف الساعات من الذكريات واللحظات الفريدة"),
            font_name=FONT_PATH,
            font_size=dp(12),
            color=COLOR_TEXT_MUTED,
            size_hint_y=None,
            height=dp(20),
            halign="center"
        )
        self.days_card.add_widget(self.lbl_days_sub)

        self.content.add_widget(self.days_card)

        # 4. Next Birthday Live Countdown Timer Card
        self.countdown_card = ModernMobileCard(orientation="vertical", padding=dp(18), spacing=dp(10), size_hint_y=None)
        self.countdown_card.bind(minimum_height=self.countdown_card.setter("height"))

        lbl_cd_title = Label(
            text=ar("العد التنازلي لعيد ميلادك القادم"),
            font_name=FONT_PATH,
            font_size=dp(14),
            bold=True,
            color=COLOR_ACCENT_PRIMARY,
            size_hint_y=None,
            height=dp(20),
            halign="center"
        )
        self.countdown_card.add_widget(lbl_cd_title)

        self.countdown_widget = LiveCountdownWidget()
        self.countdown_card.add_widget(self.countdown_widget)

        self.content.add_widget(self.countdown_card)

        # 5. Zodiac In-depth Description & Traits
        self.desc_card = ModernMobileCard(orientation="vertical", padding=dp(18), spacing=dp(8), size_hint_y=None)
        self.desc_card.bind(minimum_height=self.desc_card.setter("height"))

        lbl_desc_title = Label(
            text=ar("صفات وشخصية البرج"),
            font_name=FONT_PATH,
            font_size=dp(14),
            bold=True,
            color=COLOR_ACCENT_PRIMARY,
            size_hint_y=None,
            height=dp(20),
            halign="right"
        )
        lbl_desc_title.bind(size=lbl_desc_title.setter("text_size"))
        self.desc_card.add_widget(lbl_desc_title)

        self.lbl_description = Label(
            text="",
            font_name=FONT_PATH,
            font_size=dp(13),
            color=COLOR_TEXT,
            size_hint_y=None,
            halign="right"
        )
        self.lbl_description.bind(
            width=lambda *a: setattr(self.lbl_description, 'text_size', (self.lbl_description.width, None)),
            texture_size=lambda *a: setattr(self.lbl_description, 'height', self.lbl_description.texture_size[1])
        )
        self.desc_card.add_widget(self.lbl_description)

        self.lbl_traits = Label(
            text="",
            font_name=FONT_PATH,
            font_size=dp(12),
            color=COLOR_TEXT_MUTED,
            size_hint_y=None,
            halign="right"
        )
        self.lbl_traits.bind(
            width=lambda *a: setattr(self.lbl_traits, 'text_size', (self.lbl_traits.width, None)),
            texture_size=lambda *a: setattr(self.lbl_traits, 'height', self.lbl_traits.texture_size[1])
        )
        self.desc_card.add_widget(self.lbl_traits)

        self.lbl_comp = Label(
            text="",
            font_name=FONT_PATH,
            font_size=dp(12),
            color=COLOR_ACCENT_PRIMARY,
            size_hint_y=None,
            halign="right"
        )
        self.lbl_comp.bind(
            width=lambda *a: setattr(self.lbl_comp, 'text_size', (self.lbl_comp.width, None)),
            texture_size=lambda *a: setattr(self.lbl_comp, 'height', self.lbl_comp.texture_size[1])
        )
        self.desc_card.add_widget(self.lbl_comp)

        self.content.add_widget(self.desc_card)

        # 6. Action Buttons (Modern Mobile Style)
        actions_box = BoxLayout(orientation="vertical", spacing=dp(10), size_hint_y=None)
        actions_box.bind(minimum_height=actions_box.setter("height"))

        btn_share = ModernMobileButton(text="مشاركة النتيجة ✦", height=dp(52), radius=[dp(20)])
        btn_share.on_release = self.share_results
        actions_box.add_widget(btn_share)

        btn_reset = MobileSecondaryButton(text="حساب تاريخ آخر ↺", height=dp(48), radius=[dp(20)])
        btn_reset.on_release = self.reset_and_back
        actions_box.add_widget(btn_reset)

        self.content.add_widget(actions_box)

        # Disclaimer
        lbl_disc = Label(
            text=ar("الأبراج للتسلية والثقافة العامة وليست علماً مثبتاً"),
            font_name=FONT_PATH,
            font_size=dp(11),
            color=(0.55, 0.52, 0.70, 0.70),
            size_hint_y=None,
            height=dp(26),
            halign="center"
        )
        self.content.add_widget(lbl_disc)

        self.scroll.add_widget(self.content)
        root.add_widget(self.scroll)
        self.add_widget(root)

    def _create_metric_box(self, label_text):
        box = BoxLayout(orientation="vertical", spacing=dp(1), padding=[dp(4), dp(4)])
        with box.canvas.before:
            Color(0.08, 0.075, 0.17, 1.0)
            r = RoundedRectangle(pos=box.pos, size=box.size, radius=[dp(12)])
        box.bind(pos=lambda *a: setattr(r, 'pos', box.pos),
                 size=lambda *a: setattr(r, 'size', box.size))

        lbl_v = Label(text="0", font_size=dp(18), bold=True, color=COLOR_TEXT)
        lbl_u = Label(text=ar(label_text), font_name=FONT_PATH, font_size=dp(11), color=COLOR_TEXT_MUTED)
        box.add_widget(lbl_v)
        box.add_widget(lbl_u)
        return box, lbl_v

    def load_data(self, birthday, years, months, days, total_days, sign_info):
        self.selected_birthday = birthday
        self.years = years
        self.months = months
        self.days = days
        self.total_days = total_days
        self.sign_info = sign_info

        self.lbl_hero_symbol.text = sign_info["symbol"]
        self.lbl_sign_name.text = ar(f"برج {sign_info['name']}")
        self.lbl_date_range.text = ar(sign_info["date_range"])

        self.pill_element.text = f"{sign_info['element_icon']} {sign_info['element']}"
        self.pill_element.badge_color = sign_info["element_color"]
        self.pill_planet.text = f"كوكب: {sign_info['planet']}"

        self.lbl_big_age.text = ar(f"{years} سنة")
        self.lbl_y_val.text = str(years)
        self.lbl_m_val.text = str(months)
        self.lbl_d_val.text = str(days)

        b_text = format_arabic_date(birthday.day, birthday.month, birthday.year)
        self.lbl_birth_date.text = ar(f"تاريخ الميلاد: {b_text}")

        self.lbl_animated_days.count_to(total_days, duration=1.2)
        approx_hours = total_days * 24
        self.lbl_days_sub.text = ar(f"ما يعادل تقريباً {approx_hours:,} ساعة من الذكريات والتجارب")

        self.lbl_description.text = ar(sign_info["description"])
        traits_str = " • ".join(sign_info["traits"])
        self.lbl_traits.text = ar(f"أبرز الصفات: {traits_str}")
        comp_str = " ، ".join(sign_info["compatibility"])
        self.lbl_comp.text = ar(f"الأبراج الأكثر توافقاً: {comp_str}")

        if self._countdown_timer:
            self._countdown_timer.cancel()

        self._update_countdown(0)
        self._countdown_timer = Clock.schedule_interval(self._update_countdown, 1.0)

        self.scroll.scroll_y = 1.0
        self.content.opacity = 0
        anim = Animation(opacity=1, d=0.40, t="out_quad")
        anim.start(self.content)

    def _update_countdown(self, dt):
        if not self.selected_birthday:
            return

        now = datetime.now()
        b = self.selected_birthday
        next_year = now.year

        while True:
            try:
                next_b = datetime(next_year, b.month, b.day, 0, 0, 0)
            except ValueError:
                next_b = datetime(next_year, 2, 28, 0, 0, 0)

            if next_b > now:
                break
            next_year += 1

        diff = next_b - now
        total_sec = max(0, int(diff.total_seconds()))

        cd_days = total_sec // 86400
        cd_hours = (total_sec % 86400) // 3600
        cd_mins = (total_sec % 3600) // 60
        cd_secs = total_sec % 60

        self.countdown_widget.set_time(cd_days, cd_hours, cd_mins, cd_secs)

    def share_results(self):
        if not self.sign_info or not self.selected_birthday:
            return

        b = self.selected_birthday
        b_str = f"{b.day}/{b.month}/{b.year}"
        share_text = (
            f"✦ تطبيق ZODIAC ✦\n"
            f"برج {self.sign_info['name']} {self.sign_info['symbol']} ({self.sign_info['element_icon']} {self.sign_info['element']})\n"
            f"تاريخ الميلاد: {b_str}\n"
            f"العمر: {self.years} سنة و {self.months} شهر و {self.days} يوم\n"
            f"إجمالي الأيام: {self.total_days:,} يوم\n"
            f"الكوكب الحاكم: {self.sign_info['planet']}\n"
            f"أبرز الصفات: {', '.join(self.sign_info['traits'])}\n"
            f"اكتشف برجك وعمرك بدقة مع تطبيق ZODIAC!"
        )

        Clipboard.copy(share_text)
        CosmicToast.show(self, "تم نسخ النتيجة إلى الحافظة بنجاح! ✨")

    def reset_and_back(self):
        if self._countdown_timer:
            self._countdown_timer.cancel()
            self._countdown_timer = None
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = "main"


# ---------------------------------------------------------
# 4. All 12 Zodiac Signs Screen
# ---------------------------------------------------------
class AllSignsScreen(Screen):
    """
    12 Zodiac Signs Directory with modern Android pill chips and
    smooth bottom-sheet modal dialogues.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bg = CosmicBackground()
        self.add_widget(self.bg)

        self.current_filter = None

        root = BoxLayout(orientation="vertical")

        self.top_bar = TopBar(
            title="الأبراج الفلكية الـ 12",
            show_back=True,
            show_logo=True
        )
        self.top_bar.on_nav_back = self.go_back
        root.add_widget(self.top_bar)

        # Filter Chips Bar (الكل | ناري | ترابي | هوائي | مائي)
        filter_bar = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(42),
            padding=[dp(12), dp(4)],
            spacing=dp(6)
        )

        filters = [
            ("الكل", None),
            ("ناري 🔥", "ناري"),
            ("ترابي 🌿", "ترابي"),
            ("هوائي 💨", "هوائي"),
            ("مائي 💧", "مائي"),
        ]

        self.filter_chips = []
        for label_text, filter_val in filters:
            chip = MobileFilterChip(text=label_text, is_active=(filter_val is None))
            chip.bind(on_release=lambda inst, f=filter_val: self._apply_filter(f, inst))
            self.filter_chips.append((chip, filter_val))
            filter_bar.add_widget(chip)

        root.add_widget(filter_bar)

        self.scroll = ScrollView(do_scroll_x=False, bar_width=dp(2))
        self.signs_layout = BoxLayout(
            orientation="vertical",
            spacing=dp(10),
            padding=[dp(16), dp(8), dp(16), dp(24)],
            size_hint_y=None
        )
        self.signs_layout.bind(minimum_height=self.signs_layout.setter("height"))

        self._render_signs()

        self.scroll.add_widget(self.signs_layout)
        root.add_widget(self.scroll)
        self.add_widget(root)

    def _apply_filter(self, filter_val, active_chip=None):
        self.current_filter = filter_val
        for chip, f_val in self.filter_chips:
            chip.is_active = (f_val == filter_val)
        self._render_signs()

    def _render_signs(self):
        self.signs_layout.clear_widgets()

        for sign in ALL_ZODIAC_SIGNS:
            if self.current_filter and sign["element"] != self.current_filter:
                continue

            card = self._create_sign_card(sign)
            self.signs_layout.add_widget(card)

    def _create_sign_card(self, sign):
        card = ModernMobileCard(orientation="horizontal", padding=dp(12), spacing=dp(10), size_hint_y=None, height=dp(86))

        # Right Symbol Badge (RTL First item)
        sym_box = BoxLayout(size_hint=(None, None), size=(dp(58), dp(58)))
        with sym_box.canvas.before:
            Color(0.18, 0.15, 0.35, 0.90)
            r = RoundedRectangle(pos=sym_box.pos, size=sym_box.size, radius=[dp(29)])
        sym_box.bind(pos=lambda *a: setattr(r, 'pos', sym_box.pos),
                     size=lambda *a: setattr(r, 'size', sym_box.size))

        lbl_s = Label(text=sign["symbol"], font_size=dp(28), bold=True, color=COLOR_TEXT)
        sym_box.add_widget(lbl_s)

        # Center info
        info_col = BoxLayout(orientation="vertical", spacing=dp(2))
        lbl_n = Label(
            text=ar(f"برج {sign['name']}  ({sign['name_en']})"),
            font_name=FONT_PATH,
            font_size=dp(15),
            bold=True,
            color=COLOR_TEXT,
            halign="right"
        )
        lbl_n.bind(size=lbl_n.setter("text_size"))

        lbl_d = Label(
            text=ar(sign["date_range"]),
            font_name=FONT_PATH,
            font_size=dp(12),
            color=COLOR_TEXT_MUTED,
            halign="right"
        )
        lbl_d.bind(size=lbl_d.setter("text_size"))

        elem_pill = ElementPillBadge(
            text=f"{sign['element_icon']} {sign['element']}",
            badge_color=sign["element_color"]
        )

        info_col.add_widget(lbl_n)
        info_col.add_widget(lbl_d)
        info_col.add_widget(elem_pill)

        # Left action arrow
        lbl_arrow = Label(text="‹", font_size=dp(22), color=COLOR_ACCENT_PRIMARY, size_hint_x=None, width=dp(20))

        card.add_widget(lbl_arrow)
        card.add_widget(info_col)
        card.add_widget(sym_box)

        def _open_detail(touch):
            if card.collide_point(*touch.pos):
                modal = ZodiacDetailModal(sign)
                modal.open()
                return True
            return False

        card.on_touch_down = _open_detail
        return card

    def go_back(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = "main"


# ---------------------------------------------------------
# 5. Settings Screen
# ---------------------------------------------------------
class SettingsScreen(Screen):
    """
    Settings screen offering star particles toggle,
    app information, disclaimer, and sharing.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bg = CosmicBackground()
        self.add_widget(self.bg)

        root = BoxLayout(orientation="vertical")

        self.top_bar = TopBar(
            title="الإعدادات والمعلومات",
            show_back=True,
            show_logo=True
        )
        self.top_bar.on_nav_back = self.go_back
        root.add_widget(self.top_bar)

        scroll = ScrollView(do_scroll_x=False, bar_width=dp(2))
        content = BoxLayout(
            orientation="vertical",
            spacing=dp(14),
            padding=[dp(16), dp(12), dp(16), dp(24)],
            size_hint_y=None
        )
        content.bind(minimum_height=content.setter("height"))

        # Section 1: Appearance & Effects
        card_fx = ModernMobileCard(orientation="vertical", padding=dp(16), spacing=dp(10), size_hint_y=None)
        card_fx.bind(minimum_height=card_fx.setter("height"))

        lbl_s1 = Label(
            text=ar("المظهر والمؤثرات"),
            font_name=FONT_PATH,
            font_size=dp(15),
            bold=True,
            color=COLOR_ACCENT_PRIMARY,
            size_hint_y=None,
            height=dp(22),
            halign="right"
        )
        lbl_s1.bind(size=lbl_s1.setter("text_size"))
        card_fx.add_widget(lbl_s1)

        row_fx = BoxLayout(orientation="horizontal", size_hint_y=None, height=dp(36), spacing=dp(10))
        self.btn_toggle_fx = ModernMobileButton(text="مفعل ✓", height=dp(34), size_hint_x=None, width=dp(90), radius=[dp(17)])
        self.btn_toggle_fx.on_release = self._toggle_particles

        lbl_fx_name = Label(
            text=ar("مؤثرات النجوم والكون المتحركة"),
            font_name=FONT_PATH,
            font_size=dp(13),
            color=COLOR_TEXT,
            halign="right"
        )
        lbl_fx_name.bind(size=lbl_fx_name.setter("text_size"))
        row_fx.add_widget(self.btn_toggle_fx)
        row_fx.add_widget(lbl_fx_name)
        card_fx.add_widget(row_fx)

        lbl_theme_desc = Label(
            text=ar("السمة: الفضاء الكوني الفاخر (Dark Cosmic Purple)"),
            font_name=FONT_PATH,
            font_size=dp(12),
            color=COLOR_TEXT_MUTED,
            size_hint_y=None,
            height=dp(20),
            halign="right"
        )
        lbl_theme_desc.bind(size=lbl_theme_desc.setter("text_size"))
        card_fx.add_widget(lbl_theme_desc)

        content.add_widget(card_fx)

        # Section 2: About App with Logo
        card_about = ModernMobileCard(orientation="vertical", padding=dp(16), spacing=dp(8), size_hint_y=None)
        card_about.bind(minimum_height=card_about.setter("height"))

        lbl_s2 = Label(
            text=ar("عن التطبيق"),
            font_name=FONT_PATH,
            font_size=dp(15),
            bold=True,
            color=COLOR_ACCENT_PRIMARY,
            size_hint_y=None,
            height=dp(22),
            halign="right"
        )
        lbl_s2.bind(size=lbl_s2.setter("text_size"))
        card_about.add_widget(lbl_s2)

        about_text = (
            "ZODIAC v2.0 - Premium Edition\n"
            "تطبيق فلكي فاخر لحساب العمر الدقيق وتحليل الأبراج الفلكية.\n"
            "مبني بالكامل بلغة Python وتقنية Kivy مع دعم كامل للغة العربية."
        )
        lbl_about = Label(
            text=ar(about_text),
            font_name=FONT_PATH,
            font_size=dp(13),
            color=COLOR_TEXT,
            size_hint_y=None,
            halign="right"
        )
        lbl_about.bind(width=lambda *a: setattr(lbl_about, 'text_size', (lbl_about.width, None)),
                       texture_size=lambda *a: setattr(lbl_about, 'height', lbl_about.texture_size[1]))
        card_about.add_widget(lbl_about)

        content.add_widget(card_about)

        # Section 3: Disclaimer
        card_disc = ModernMobileCard(orientation="vertical", padding=dp(16), spacing=dp(8), size_hint_y=None)
        card_disc.bind(minimum_height=card_disc.setter("height"))

        lbl_s3 = Label(
            text=ar("إخلاء مسؤولية وتنويه"),
            font_name=FONT_PATH,
            font_size=dp(15),
            bold=True,
            color=COLOR_ACCENT_PRIMARY,
            size_hint_y=None,
            height=dp(22),
            halign="right"
        )
        lbl_s3.bind(size=lbl_s3.setter("text_size"))
        card_disc.add_widget(lbl_s3)

        disc_text = (
            "الأبراج والصفات الفلكية الواردة في التطبيق مقدمة لأغراض التسلية "
            "والثقافة العامة والتأمل، وليست حقائق علمية مؤكدة أو تنبؤات بالمستقبل."
        )
        lbl_disc_body = Label(
            text=ar(disc_text),
            font_name=FONT_PATH,
            font_size=dp(12),
            color=COLOR_TEXT_MUTED,
            size_hint_y=None,
            halign="right"
        )
        lbl_disc_body.bind(width=lambda *a: setattr(lbl_disc_body, 'text_size', (lbl_disc_body.width, None)),
                           texture_size=lambda *a: setattr(lbl_disc_body, 'height', lbl_disc_body.texture_size[1]))
        card_disc.add_widget(lbl_disc_body)

        content.add_widget(card_disc)

        btn_share_app = ModernMobileButton(text="مشاركة تطبيق ZODIAC ✦", height=dp(50), radius=[dp(20)])
        btn_share_app.on_release = self._share_app
        content.add_widget(btn_share_app)

        scroll.add_widget(content)
        root.add_widget(scroll)
        self.add_widget(root)

    def _toggle_particles(self):
        app = App.get_running_app()
        new_val = not app.particles_enabled
        app.particles_enabled = new_val

        if new_val:
            self.btn_toggle_fx.text = "مفعل ✓"
            self.btn_toggle_fx._bg_col.rgba = (0.486, 0.227, 0.929, 1.0)
        else:
            self.btn_toggle_fx.text = "معطل ✕"
            self.btn_toggle_fx._bg_col.rgba = (0.24, 0.20, 0.38, 1.0)

        for screen in self.manager.screens:
            if hasattr(screen, "bg") and hasattr(screen.bg, "enable_particles"):
                screen.bg.enable_particles = new_val

    def _share_app(self):
        msg = "اكتشف برجك وعمرك الدقيق وتفاصيلك الفلكية مع تطبيق ZODIAC الرائع! ♈✨"
        Clipboard.copy(msg)
        CosmicToast.show(self, "تم نسخ رابط التطبيق إلى الحافظة! ✨")

    def go_back(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = "main"


# ---------------------------------------------------------
# Main Application Class
# ---------------------------------------------------------
class ZodiacApp(App):
    """
    ZODIAC Application instance managing screens, theme, and official branding.
    """
    font = FONT_PATH
    icon = ICON_PATH
    particles_enabled = BooleanProperty(True)

    def build(self):
        self.title = "ZODIAC"
        self.icon = ICON_PATH if os.path.exists(ICON_PATH) else ""

        sm = ScreenManager(transition=FadeTransition(duration=0.3))
        sm.add_widget(SplashScreen(name="splash"))
        sm.add_widget(MainScreen(name="main"))
        sm.add_widget(ResultsScreen(name="results"))
        sm.add_widget(AllSignsScreen(name="all_signs"))
        sm.add_widget(SettingsScreen(name="settings"))

        return sm

    def ar(self, text):
        return ar(text)


if __name__ == "__main__":
    ZodiacApp().run()
