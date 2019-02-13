# PyGame_proj
Этот проект был создан в рамках обучающей программы Яндекс.Лицей

# Суть проекта
Проект должен представлять из себя игру, которая имеет законченный игровой цикл, написанная на Python3 при помощи библиотеки PyGame

# Реализованные механики
- Сделана генерация поля из текстового файла
- Созданы классы Танка Игрока, Танка Противника, Пули, Стен, Листьев, Спаунов
- перемещения по полю
- выстрела танков
- главного меню, из которого можно выбрать уровень, начать игру и выйти
- автоматической смены уроня
- спауна противников
- коллизий танков со стенами
- коллизий вражеских танков с танком игрока(прим. было принято решение не добавлять коллизию между танками противников)
- проигрыша при повреждении флага или уничтожении танка
- ИИ, управляющий движением танков
- разрушение стен в соответсвии со стороной, в которую попали
- маштабирование всего игрового поля

# Справка по игре:
- управление танком производится с помощью стрелочек
- выстрел производится при помощи клавиши пробел
- уровень считается пройденным, если все появившиеся противники будут уничтожены
- проигрыш засчитывается после уничтожения флага или танка игрока, после этого вас выкинет в главное меню
- в главном меню можно выбрать начальный уровень, далее уровни будут циклично меняться по порядку
