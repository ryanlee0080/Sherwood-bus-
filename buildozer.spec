[app]
# (str) Title of your application
title = 豫豐居民巴士

# (str) Package name (英文小寫，無空格)
package.name = sherwoodbus

# (str) Package domain (你的網域或識別碼)
package.domain = org.sherwood

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include (包含的檔案類型)
source.include_exts = py,png,jpg,ttf

# (str) Application versioning
version = 1.0

# (list) Application requirements
# 注意：必須包含 python3 和 kivy，如使用其他套件也可加在此處
requirements = python3,kivy

# (str) Supported orientation (portrait/landscape/all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions (預設基本權限即可)
android.permissions = INTERNET

# (int) Target Android API
android.api = 33

# (int) Minimum API required
android.minapi = 21

# (str) Android NDK version
android.ndk = 25b

[buildozer]
# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# (int) Display warning if buildozer is run as root (0 = disable, 1 = enable)
warn_on_root = 1
