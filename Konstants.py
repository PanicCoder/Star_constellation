import platform
from Interface import In_common
in_common = In_common()
sep = "\\" if platform.system() == 'Windows' else "/"
icon = "."+sep+"Images"+sep+"icon.png"
galaxy = "."+sep+"Images"+sep+"galaxy.jpg"
exit = "."+sep+"Images"+sep+"Exit.png"
level = "."+sep+"Images"+sep+"level.png"
settings = "."+sep+"Images"+sep+"settings.png"
settings_json = "."+sep+"Settings"+sep+"settings.json"
level_json = "."+sep+"Starfiles"+sep
music = "."+sep+"Music"+sep
sound_effects = "."+sep+"Sound_effects"+sep
switch = ["."+sep+"Images"+sep+"offswitch.png","."+sep+"Images"+sep+"onswitch.png"]