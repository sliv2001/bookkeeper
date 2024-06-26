# Программа для управления личными финансами
#### (учебный проект для курса по практике программирования на Python)

[Техническое задание](specification.md)

Для работы с данными было выбрано использование библиотеки ORM (PonyORM).

Было принято решение поддерживать обратную совместимость с уже написанным преподавателем кодом, для переиспользования тестов.

Соблюдена исходная архитектура проекта:

📁 bookkeeper — исполняемый код

- 📁 models — модели данных

    - 📄 budget.py — бюджет
    - 📄 category.py — категория расходов
    - 📄 expense.py — расходная операция
- 📁 repository — репозиторий для хранения данных

    - 📄 abstract_repository.py — описание интерфейса
    - 📄 memory_repository.py — репозиторий для хранения в оперативной памяти
    - 📄 sqlite_repository.py — репозиторий для хранения в sqlite-based ORM
    - 📄 *_repository.py — репозиторий для непосредственного хранения данных
- 📁 view — графический интерфейс
- 📄 simple_client.py — простая консольная утилита, позволяющая посмотреть на работу программы в действии
- 📄 bookkeeper.py - основное приложение
- 📄 utils.py — вспомогательные функции

📁 tests — тесты (структура каталога дублирует структуру bookkeeper)

***Важно! Программа использует Python файлы, сгенерированные Qt Designer.***

Проект создан с помощью `poetry`.

Для запуска программы проделайте следующую последовательность действий, находясь ***в виртуальном окружении Poetry***:

```commandline
poetry install
./build.py
poetry run bookkeeper
```

Для запуска тестов и статических анализаторов используйте следующие команды:

```commandline
poetry run pytest --cov
poetry run mypy --strict bookkeeper
poetry run pylint bookkeeper --ignore-patterns=Ui_
poetry run flake8 bookkeeper
```

***Пожалуйста, обратите внимание, что автором было принято (возможно неверное) решение использовать Qt Designer, и полагаться на перегенерацию .py файлов при каждом изменении интерфейса. Потому, пожалуйста, рассмотрите возможность использовать pylint с флагом `--ignore-patterns=Ui_`***

### Архитектурные замечания

В проекте применяется архитектура, указанная на рисунке ниже. Было принято решение использовать дополнительную прослойку над PonyORM в виде репозитория для большего удобства в случае переноса системы на другой ORM, а также для переиспользования существующего кода.

![Architectural](arch.svg)

Код модулей Presenter.py, *Repository.py допускает значительно большие возможности, чем поддерживает интерфейс: бэкенд спроектирован таким образом, чтобы поддерживать удаление и изменение Category, Expense и Budget. В силу нехватки времени, поддержка во View выполнена лишь частично.

### Видеопрезентация

По следующей [ссылке](https://disk.yandex.com/i/QcefXs144mnaBQ) можно ознакомиться с краткой видеопрезентацией работоспособной версии проекта.
