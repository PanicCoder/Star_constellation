import urllib.request

from PIL import Image

file_name = "grosser-baer.png"
urllib.request.urlretrieve("https://astrokramkiste.de/images/sternbilder/grosser-baer-a.png",file_name)
Image.open(file_name).save(".\\Images\\"+file_name+".png")

