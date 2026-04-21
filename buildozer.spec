[app]
# (str) Title of your application
title = Rosario de Emaús

# (str) Package name
package.name = rosarioemaus

# (str) Package domain (needed for android/ios packaging)
package.domain = org.emaus

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,jpeg,html,js,css,json

# (str) Application versioning
version = 1.0

# (list) Application requirements
# Flask and its dependencies
requirements = python3,flask,jinja2,werkzeug,itsdangerous,click,markupsafe,setuptools,hostpython3

# (str) Supported orientations
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (str) Android logcat filters to use
android.logcat_filters = *:S python:D

# (list) Permissions
android.permissions = INTERNET, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE

# (str) The Android arch to build for
android.archs = arm64-v8a, armeabi-v7a

# (str) Bootstrap to use for android
# Para apps Flask/Web usamos webview
p4a.bootstrap = webview

# (int) Port for the webview to point at
android.port = 5000

[buildozer]
# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = off, 1 = on)
warn_on_root = 1