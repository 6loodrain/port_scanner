# Сканер портов

Web-приложение для сканирования открытых TCP портов удаленного хоста.
Приложение реализует следующее REST API:

    * GET /scan/<ip>/<begin_port>/<end_port>

    Параметры:
        # ip - хост, который необходимо просканировать
        # begin_port - начала диапозона портов для сканирования
        # end_port - конец диапозона портов для сканирования

    Формат ответа:  [{"port": "integer", "state": "(open|close)"}]


Обработчик запускает сканирование указанного хоста, и отдает информацию клиенту в формате JSON.
    


## Запуск программы
Загрузите репозиторий и перейдите в папку. В командной строке выполните следующую инструкцию.

        python port_scanner.py
Откройте браузер и сделайте запрос на указанный ниже адрес.
    
        https:://localhost:8080/scan/127.0.0.1/1/1000

Таким образом вы просканируете удалённый хост по адресу 127.0.0.1 в диапазоне портов от 1 до 1000 включительно.
## Пример запроса и вывода на примере сайта github.com
### 1.  Запускаем программу
![Image alt](https://sun9-east.userapi.com/sun9-23/s/v1/ig2/hZ8Uix6tbp2hWEjqVoVKeOm3RUf1ggtWoW_TlNguSwqah7Qs77vHpJ7kw45QxGSssNB8LaAPeTV5AEzavtkxK0JX.jpg?size=533x71&quality=96&type=album)
### 1.5  Узнаём IP
![Image alt](https://sun9-west.userapi.com/sun9-38/s/v1/ig2/4Qa9bkang5qFIsYMtOZEJPhOywspoq_R8rH9iVh0MuIZea8ta4Rl5IScEfWyYJcZ2j-lko5ndE0xN7XuHfckY7WJ.jpg?size=1006x726&quality=96&type=album)
### 2.  Вводим необходимые параметры в консоль
![Image Alt](https://sun9-north.userapi.com/sun9-81/s/v1/ig2/zRjjY9iOJewoWm15Bv7P4TF8d7AD3ItdDVmUINt2pGY06BoyC6asJekUcBBEHcoXtePAQm4_PxYr2C7-PKEaRkH1.jpg?size=557x102&quality=96&type=album)

#### !!!Допустимый формат IP - от 0.0.0.0 до 255.255.255.255!!!
#### !!!Допустимый формат start_port и end_port 0 < start_port <= end_port!!!
### 3.  Получаем результат
![Image Alt](https://sun9-west.userapi.com/sun9-48/s/v1/ig2/qslPIDdoAeVniHME31tFSXtkliipDIJhFi8Kzc8fO3tYTMj8axF1MfupFVRE04Oce7KN0DamPi5a4AQoZLD-A3vj.jpg?size=1920x1033&quality=96&type=album)
## Структура проекта
1. port_scanner.py - исполняемый файл
2. README.md - у вас перед глазами
3. specifications.txt - версии используемых библиотек и python
4. test_port_scanner.py - набор тестов

## Важно
Если вы работаете с большим диапазоном портов, от 5000, рекомендуется увеличить время жизни соединения. По умолчанию стоит 5 секунд.

        awaited_time = 5  # in sec, duration of connection