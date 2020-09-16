import os
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image

from .track import Point


class Chrome:
    def __init__(self, filename: str, map_id: str):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")  # needs in docker
        options.add_argument("--disable-dev-shm-usage")  # needs in docker
        driver = webdriver.Chrome(options=options)
        driver.set_window_size(600, 600)

        driver.get(f"file:///{os.getcwd()}/{filename}")

        self._driver = driver
        self._map_id = map_id

    def _image_loaded(self, img) -> bool:
        colors = [
            img.getpixel((0, 0)),
            img.getpixel((224, 0)),
            img.getpixel((0, 224)),
            img.getpixel((224, 224))]

        return all(map(lambda _: _ != (221, 221, 221, 255), colors))

    def crop_center(self, img, crop_width, crop_height):
        img_width, img_height = img.size
        return img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))

    def save_koma(self, filename: str, point: Point):
        self._driver.execute_script(
            f"map_{self._map_id}.panTo(new L.LatLng({point.latitude}, {point.longitude}), {{'animate': false}});")

        for _ in range(15):
            time.sleep(0.5)
            self._driver.save_screenshot("_map.png")
            img = Image.open('_map.png')
            img = img.rotate(point.direction)
            img = self.crop_center(img, 225, 225)

            if self._image_loaded(img):
                break

        img.save(filename)
        print(filename)
