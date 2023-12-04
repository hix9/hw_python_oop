from dataclasses import dataclass
"""Программа Фитнес-трекер."""


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


@dataclass
class Training:
    """Базовый класс тренировки."""

    action: int
    duration: float
    weight: float

    M_IN_KM = 1000
    LEN_STEP = 0.65
    CM_IN_M = 100
    MIN_IN_H = 60

    def get_distance(self) -> float:
        """Получить дистанцию в км."""

        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
# У меня не получается сделать перенос без отрыва от скобок,
# переменные имеют длинные названия.
# С отрывом у меня тоже не получается,
# локально Flake8 не видит ошибок, но при тестах возникает
# множество ошибок, возможно мне нужен ещё линтер?

        return (((self.CALORIES_MEAN_SPEED_MULTIPLIER
                 * self.get_mean_speed()
                 + self.CALORIES_MEAN_SPEED_SHIFT)
                 * (self.weight / self.M_IN_KM))
                * self.duration * self.MIN_IN_H)


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    LEN_STEP = 0.65
    CALORIES_WEIGHT_MULTIPLIER = 0.035
    CALORIES_WEIGHT_MULTIPLIER_2 = 0.029
    KMH_IN_MSEC = 0.278
    CM_IN_M = 100

    action: int
    duration: float
    weight: float
    height: int

    def get_spent_calories(self) -> float:

        return ((self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                 + ((self.get_mean_speed() * self.KMH_IN_MSEC)
                    ** 2 / (self.height / self.CM_IN_M))
                * self.CALORIES_WEIGHT_MULTIPLIER_2 * self.weight)
                * self.duration * self.MIN_IN_H)


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38
    MEAN_SPEED_MULTIPLIER = 1.1
    SWIM_WEIGHT_MULTIPLIER = 2

    action: int
    duration: float
    weight: float
    length_pool: float
    count_pool: int

    def get_mean_speed(self) -> float:
        return ((self.length_pool * self.count_pool)
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.MEAN_SPEED_MULTIPLIER)
                * self.SWIM_WEIGHT_MULTIPLIER * self.weight * self.duration)


TRANING_TYPE = {}


def read_package(workout_type: str, data: list[int]) -> Training:
    """Прочитать данные полученные от датчиков."""

    TRANING_TYPE = {'SWM': Swimming,
                    'RUN': Running,
                    'WLK': SportsWalking
                    }

    if workout_type not in TRANING_TYPE:

        raise TypeError('Работает только со строковыми данными.')

    return TRANING_TYPE[workout_type](*data)


def main(training: Training) -> InfoMessage:
    """Главная функция."""

    info: InfoMessage = training.show_training_info()

    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training: Training = read_package(workout_type, data)
        main(training)
