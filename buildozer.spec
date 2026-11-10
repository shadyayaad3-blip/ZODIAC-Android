
[app]

title = ZODIAC
package.name = zodiac
package.domain = org.cosmic.zodiac

source.dir = .
source.include_exts = py,png,jpg,jpeg,ttf,otf,kv,atlas,json,svg
source.include_patterns = assets/*

version = 2.0.0

p4a.branch = master

requirements = python3,kivy==2.3.1,arabic-reshaper,python-bidi

orientation = portrait
fullscreen = 0

p4a.branch = master

android.api = 35
android.minapi = 23
android.sdk = 35
android.ndk = 27b

android.skip_update = False
android.accept_sdk_license = True

android.archs = arm64-v8a,armeabi-v7a

android.allow_backup = True
android.debug_artifact = apk

[buildozer]

log_level = 2
warn_on_root = 1
