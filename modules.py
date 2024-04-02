import matplotlib.pyplot as plt
from datetime import datetime as dt
from time import sleep
import requests
import json

# for i in range(1440):
#     sleep(60)
#     r = requests.get('https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD')
#     bitcoin_value = float(json.loads(r.content)["USD"])
#     with open('btc cource.txt', 'r', encoding='utf-8') as f:
#             file = str(f.readline(-1))
#     with open('btc cource.txt', 'a', encoding='utf-8') as f:
#             f.write(f'{file}\n{str(bitcoin_value)}')

class TimeNow:
    # @staticmethod
    def get_current_time(self):
        """
        Получение текущего времени и даты в виде объекта datetime.
        :return: Объект datetime, представляющий текущее время и дату.
        """
        return self.current_time
    
    def get_today(self):
        """
        Получение текущей даты в формате 'DD.MM.YYYY'.
        :return: Строка с текущей датой.
        """
        return f"{dt.now().day:02d}.{dt.now().month:02d}.{dt.now().year:02d}"

    def get_time(self):
        """
        Получение текущего времени в формате 'HH:MM:SS'.
        :return: Строка с текущим временем.
        """
        return f"{dt.now().hour:02d}:{dt.now().minute:02d}:{dt.now().second:02d}"

class CreateStatistic:
    # def __init__(self, date, message):
    #     self.date = date

    def get_time(self, message):
        time_now_instance = TimeNow()  # Создаем экземпляр класса TimeNow
        if len(message) == 2 and len(message[1]) in [4, 5]:
            day = message[1]
            day_parts = day.split(".")
            if len(day_parts[0]) == 1:
                day_parts[0] = f"0{day_parts[0]}"
            day = ".".join(day_parts)
            

            time_now = f"{day}.{time_now_instance.get_today()[5 if len(day) == 2 else 6:]}"
            print(time_now)

        elif len(message) == 2 and len(message[1]) in [1, 2]:
            if len(message[1]) == 1:
                message[1] = f"0{message[1]}"
            time_now = f"{message[1]}.{time_now_instance.get_today()[3:]}"
            
        else:
            time_now = (time_now_instance.get_today())

        return time_now
    

    def theme(self, time_now=None):
        time_now_instance = TimeNow()
        time_now=int(time_now_instance.get_time()[:2])
        """Устанавливает темную/светлую тему"""
        if  time_now < 19 and time_now > 6:
            return "black", "white", "#423189"
        else:
            return "white", "black", "#383862"
    

    def create(self, message):
        """Создает статистику"""

        time_now = self.get_time(message)
        accuracy = self.accuracy(message)
        color_word, color_background, color_bar = self.theme()

        if type(time_now) == str:
            return get_stat_of_day(time_now, color_word, color_background, color_bar, high=accuracy)
        else:
            return get_stat_of_day(color_word=color_word, color_background=color_background, color_bar=color_bar, high=accuracy)
        
def smooth_zeros(data, repeat, window_size=3):
    smoothed_data = []
    smoothed_repeat = []
    for i in range(len(data)):
        start_index = max(0, i - window_size // 2)
        end_index = min(len(data), i + window_size // 2 + 1)

        # Усредняем значения в окне, игнорируя нули
        non_zero_values = [repeat[j] for j in range(start_index, end_index) if repeat[j] != 0]

        if non_zero_values:
            smoothed_repeat.append(np.mean(non_zero_values))
        else:
            smoothed_repeat.append(0)

        smoothed_data.append(data[i])

    return smoothed_data, smoothed_repeat

def get_stat_of_day(date: str = TimeNow().get_today(), color_word: str = "white", 
                                                       color_background: str = "black",
                                                       color_bar: str = "#D77D31",
                                                       high: int = 1):
    result = db.message_log().get_data(date)
    plt.figure(figsize=(10 if high < 3 else 15 if high < 4 else 30 if high < 6 else 5, 5 if high < 3 else 4 if high < 6 else 2), dpi=150, facecolor='black')  # Добавлен параметр facecolor
    data = []
    repeat = [1]
    for i in range(len(result)):
        data.append(f"{result[i][2][:high]}")
        if len(data) < len(result):
            if f"{result[i+1][2][:high]}" == f"{result[i][2][:high]}":
                repeat.append(repeat[i]+1)
            else:
                repeat.append(1)
    
    # Усреднение значений вокруг нулей
    smoothed_data, smoothed_repeat = smooth_zeros(data, repeat, window_size=1)

    average_value = np.mean(smoothed_repeat)
    

    plt.grid(True, alpha=0.7)
    if high < 6: 
        plt.bar(smoothed_data, smoothed_repeat, color=color_bar, alpha=1, edgecolor=color_bar, label=f'В среднем: {int(average_value)}')
        plt.xlabel("Часы", fontdict={"fontname": "Arial", "fontsize": 18, "color": color_word})  # Установлен цвет белым
        plt.ylabel("Количество сообщений", fontdict={"fontname": "Arial", "fontsize": 18, "color": color_word})  # Установлен цвет белым
        plt.xticks(rotation=0 if high < 3 else 45 if high < 4 else 90, color=color_word)  # Установлен цвет белым
    plt.yticks(rotation=0, color=color_word)  # Установлен цвет белым
    
    plt.legend(fontsize=14, loc="upper left", facecolor="gray", edgecolor=color_bar)  # Установлен цвет белым
    
    plt.title(f"Активность чата", fontdict={"fontname": "Arial", "fontsize": 35, "color": color_word})  # Установлен цвет белым
    
    plt.gca().set_facecolor(color_background)  # Задний фон всего графика
    plt.tight_layout()
    plt.savefig("stat_today.png", facecolor=color_background)  # Установлен цвет белым
    plt.close()

    return date
