# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ['KIVY_NO_ARGS'] = '1'

import main
from kivy.clock import Clock
from datetime import date

def run_tests(app):
    print("Testing Mobile UI redesign and official logo...")
    sm = app.root
    
    # 1. Test Splash screen
    splash = sm.get_screen("splash")
    print("Splash screen logo source:", splash.logo_widget.source)
    assert os.path.exists(splash.logo_widget.source), "Logo file must exist!"
    
    # 2. Test Main screen
    sm.current = "main"
    main_scr = sm.get_screen("main")
    print("Main screen topbar title:", repr(main_scr.top_bar.lbl_title.text))
    
    # Test date stepper
    main_scr.step_day.value = 15
    main_scr.step_month.value = 8
    main_scr.step_year.value = 1998
    print("Date selected: 15 / 8 / 1998")
    
    # Calculate
    main_scr.calculate_and_navigate()
    assert sm.current == "results"
    
    # 3. Test Results screen
    res = sm.get_screen("results")
    print("Results Hero Symbol:", res.lbl_hero_symbol.text)
    print("Sign Name:", repr(res.lbl_sign_name.text))
    print(f"Age: {res.years}y {res.months}m {res.days}d")
    print("Total days:", res.total_days)
    assert res.sign_info["name"] == "الأسد", "Expected Leo sign!"
    
    # Test share
    res.share_results()
    print("Share results executed successfully!")
    
    # 4. Test All Signs
    sm.current = "all_signs"
    all_signs = sm.get_screen("all_signs")
    print("Signs count:", len(all_signs.signs_layout.children))
    assert len(all_signs.signs_layout.children) == 12
    
    # Test filter
    all_signs._apply_filter("هوائي")
    print("Air signs count:", len(all_signs.signs_layout.children))
    assert len(all_signs.signs_layout.children) == 3
    
    all_signs._apply_filter(None)
    assert len(all_signs.signs_layout.children) == 12
    
    # 5. Test Settings
    sm.current = "settings"
    settings = sm.get_screen("settings")
    settings._toggle_particles()
    settings._toggle_particles()
    print("Settings tested.")
    
    print(">>> ALL MOBILE UI REDESIGN TESTS PASSED SUCCESSFULLY! <<<")
    app.stop()

class TestApp(main.ZodiacApp):
    def on_start(self):
        Clock.schedule_once(lambda dt: run_tests(self), 0.5)

if __name__ == "__main__":
    TestApp().run()
