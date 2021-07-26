# API-Testing-for-Fun-and-Profit_2

README.md - nie rób list of content a punktu zrób jako odpowiednie nagłówki (poczytaj jak się to w markdown robi). Będzie bardziej przejrzyste i zbliżone do tego jak wygąda to w innych repo. Możesz też zaznaczyć, do jakiego systemu odnosi się instrukcja (dobrze widzę, że to Windows?)

pliki z testami powinny być w oddzielnym folderze

używająs pytest.ini można wymusić, żeby pliki z testami nie zaczynały się od 'test_'

zamiast 2 folderów crud i helpers zrób jeden libs i tam wrzuć pliki z tych 2 folderów

crud_methods.py - zmienne URL, USER, PASSWORD wyrzucić do zmiennych środowiskowych, można się wspomóc biblioteką dotenv to obsługi zmiennych środowiskowych z pliku .env

ten sam plik - pozostań przy oryginalnych get/post itp. Tkod tych metod się mocno powiela i można tutaj wykorzystać metodę requests.request('GET') zamiast requests.get i stworzyć sobie dodatkową nadrzętną metodę (za dużo pisania żeby podać przykład i jest szansa, że wymyśłisz, jak nie pytaj)

client_data.py - zamiast tworzenia słownika, proponuję stworzyć klasę używając @dataclass, później można użyc na tym metody asdict() i otrzymasz ten sam słownik, który zwracasz (asdict używj podczas wysyłki klasy User)

w testach, najpierw sprawdź status code odpowiedzi, a poźniej dopiero dane z json(), warto używać biblioteki assertpy bo ma with soft_assert() i możesz sprawdzić wiele asserci na raz (tak jak masz teraz napisane, jeśli dev źle zakoduje i zwróci zły kod błędu, to nie sprawdzisz czy przyszły dane)

generalnie znów uwaga co do zmiennych URL, USER, PASSWORD (takie dane konfiguracyjne warto mieś w oddzielnej klasie np. Config().URL i zaczytywać ze zmiennych środowiskowych (opisałem to wyżej))

nie używaj globalsów, jak w setup class zrobisz cls.api_key to w testach możesz się do tego odnieść przez self.__class__.api_key

CLEANUP powinien być taką samą zmienną jak cm w ramach klasy ClientTests

odwołanie jak wyżej przez _class_ załatwi problem z ewentualnym brakiem dodawanych rzeczy