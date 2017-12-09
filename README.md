Instrukcja
=============================

Program służy do interpretacji i wizualizacji danych z projektu Oxford RobotCar Dataset (http://robotcar-dataset.robots.ox.ac.uk/) oraz danych własnych. Przeznaczony jest na systemy operacyjne Linux i napisany jest w języku Python 2.7. Program testowano na dystrybucji Ubuntu 16.04 LTS.

Wymagania
------------
###Interpreter języka Python 2.7.
Większość dystrybcuji Linuxa posiada domyślnie zainstalowany interpreter Pythona. W przypadku gdy takiego nie posiada należy kierować się instrukcjami zawartymi na oficjalnej stronie (https://docs.python.org/2/using/unix.html#on-linux).
###Pakiety:
Program do prawidłowego działania wymaga następujących pakietów Pythona:
* numpy
* matplotlib
* pillow
* colour_demosaicing

Mogą być one zainstalowane poprzez program PIP. Jego instalacji dokonuje się wpisując w terminalu:

```
sudo apt-get install python-pip
```
Do instalacji wspomnianych pakietów wykorzystuje się polecenie:
```
pip install numpy matplotlib pillow colour_demosaicing
```

###PyQT4 i pyqtgraph
Aby zainstalwoać bibliotekę pyqtgraph należy wpisać w terminalu:
```
sudo apt-get install python-pyqtgraph
```
Automatycznie powinna również zostać zainstalowana biblioteka PyQt4. Gdyby tak się nie stało należy ją zainstalować:
```
sudo apt-get install python-qt4
```
Uruchomienie programu
------------------

Aby uruchomić program należy sciągnąć wszystkie pliki zawarte w rezpozytorium i rozpakować je w dowolnym folderze. Następnie należy przejść do tego folderu za pomocą terminala i komendy 'cd' oraz wpisać:
 ```
python main.py
```

Uwagi
------------------
W obecnej wersji wszystkie ścieżki podawane w programie nie powinny zawierać polskich znaków ani znaków specjalnych(w tym spacje)

