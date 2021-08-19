from PIL import Image, ImageDraw
from selenium import webdriver


class ScreenAnalysis:


    def __init__(self):
        self.screenshot_production()
        self.analyze()

    def screenshot_production(self):
        URL = 'your url'
        options = webdriver.ChromeOptions()
        options.headless = True
        driver = webdriver.Chrome(options=options)
        driver.get(URL) # открывает страницу
        S = lambda X: driver.execute_script('return document.body.parentNode.scroll' + X) # проскроливает страницу
        driver.set_window_size(1440, S('Height'))  # размер окна для скриншота
        driver.find_element_by_tag_name('body').screenshot('screen_production.png') # куда сохранять скриншот
        driver.quit() # выход из драйвера


    def analyze(self):
        screenshot_staging = Image.open("screen_staging.png")
        screenshot_production = Image.open("screen_production.png")
        columns = 60
        rows = 80
        screen_width, screen_height = screenshot_staging.size

        block_width = ((screen_width - 1) // columns) + 1 # разделитель
        block_height = ((screen_height - 1) // rows) + 1

        for y in range(0, screen_height, block_height+1):
            for x in range(0, screen_width, block_width+1):
                region_staging = self.process_region(screenshot_staging, x, y, block_width, block_height)
                region_production = self.process_region(screenshot_production, x, y, block_width, block_height)

                if region_staging is not None and region_production is not None and region_production != region_staging:
                    draw = ImageDraw.Draw(screenshot_staging)
                    draw.rectangle((x, y, x+block_width, y+block_height), outline = "red") # смена цвета линий

        screenshot_staging.save("result.png")

    def process_region(self, image, x, y, width, height):
        region_total = 0

        #
        factor = 120 #точность чем больше, тем хуже

        for coordinateY in range(y, y+height):
            for coordinateX in range(x, x+width):
                try:
                    pixel = image.getpixel((coordinateX, coordinateY))
                    region_total += sum(pixel)/4
                except:
                    return

        return region_total/factor

ScreenAnalysis()
