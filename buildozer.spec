
[app]

title = ZODIAC
package.name = zodiac
package.domain = org.cosmic.zodiac

source.dir = .
source.include_exts = py,png,jpg,jpeg,ttf,otf,kv,atlas,json,svg
source.include_patterns = assets/*

version = 2.0.0

requirements = python3==3.11.5,hostpython3==3.11.5,kivy==2.3.1,arabic-reshaper,python-bidi

android.api = 33
android.minapi = 23
android.ndk = 25c
android.archs = arm64-v8a
p4a.branch = v2024.01.21

android.skip_update = False
android.accept_sdk_license = True

android.allow_backup = True
android.debug_artifact = apk

[buildozer]

log_level = 2
warn_on_root = 1
