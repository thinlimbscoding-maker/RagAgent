from logger_config import logger


class Car:
    def __init__(self, model, price, cartype):
        self.model = model
        self.price = price
        self.type = cartype

    def carModel(self):
        logger.info(f"my model is {self.model}")

    def carPrice(self):
        logger.info(f"my Price is {self.price}")


carObj = Car("zy00", "1Million", "auto")
carObj.carModel()
carObj.carPrice()

# above is normal class
