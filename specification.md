# Спецификация проекта: Система автоматического построения грамматики и AST для языка 1С

Данный документ содержит подробное описание требований и задач для каждого этапа разработки, что позволит разработчикам и AI-агентам понимать, что конкретно нужно реализовать по каждому чекпоинту.

## Этап 1: Инфраструктура и базовая грамматика

### Задача 1.1: Настройка проектной инфраструктуры

#### Требования и описание задачи

1. **Создание репозитория с базовой структурой проекта**
   - Создать основную структуру директорий согласно описанию в README.md
   - Инициализировать Git-репозиторий
   - Создать основные конфигурационные файлы (.gitignore, LICENSE)

2. **Настройка виртуального окружения**
   - Создать виртуальное окружение Python (venv)
   - Настроить скрипт для активации окружения

3. **Установка зависимостей**
   - Создать и заполнить файл requirements.txt
   - Установить основные зависимости:
     - Lark для построения парсера
     - CrewAI для создания AI-агентов
     - Библиотеки для логирования
     - Библиотеки для тестирования

4. **Разработка базовой архитектуры приложения**
   - Создать структуру основных модулей (grammar, ast, agents, utils)
   - Определить интерфейсы взаимодействия между модулями
   - Реализовать файл `__init__.py` для каждого модуля
   - Создать основной класс приложения

5. **Настройка CI/CD для автоматического тестирования**
   - Настроить GitHub Actions или GitLab CI
   - Создать скрипты для автоматического тестирования
   - Настроить линтеры и форматировщики кода

6. **Настройка логирования**
   - Разработать систему логирования с использованием loguru
   - Определить форматы и уровни логирования
   - Настроить вывод логов в файлы и консоль

7. **Создание конфигурационных файлов**
   - Разработать систему конфигурации (YAML/JSON)
   - Создать конфигурационные файлы для различных сред (dev, test, prod)
   - Реализовать загрузку и валидацию конфигурации

#### Технические требования
- Использовать Python 3.8+
- Следовать принципам PEP8 для стиля кода
- Организовать документацию с использованием docstrings в стиле Google
- Реализовать модульную структуру с низкой связанностью компонентов

### Задача 1.2: Разработка минимальной рабочей грамматики

#### Требования и описание задачи

1. **Изучение базовых конструкций языка 1С**
   - Исследовать синтаксис языка 1С (версия 8.3+)
   - Определить основные конструкции для реализации в грамматике
   - Собрать примеры кода для тестирования

2. **Создание файла грамматики Lark с основными правилами**
   - **Объявление переменных и присваивания**:
     - Объявление переменных (Перем, Var)
     - Операторы присваивания (=)
     - Типы данных (Число, Строка, Дата, Булево)
   
   - **Базовые управляющие конструкции**:
     - Условные операторы (Если/Тогда/Иначе)
     - Циклы (Для/Цикл)
     - Базовые логические операторы (И, ИЛИ, НЕ)
   
   - **Объявление функций/процедур с простым телом**:
     - Определение процедуры (Процедура/КонецПроцедуры)
     - Определение функции (Функция/КонецФункции)
     - Параметры функций и процедур
     - Возврат значений (Возврат)

3. **Разработка класса парсера**
   - Создать класс для работы с Lark-парсером
   - Реализовать методы для парсинга строк и файлов
   - Добавить обработку ошибок парсинга
   - Реализовать диагностику проблем при парсинге

4. **Создание базовых тестов**
   - Разработать модульные тесты для проверки парсера
   - Создать тестовые файлы с примерами 1С-кода
   - Реализовать проверку корректности построения дерева разбора

#### Технические требования
- Грамматика должна быть реализована в формате Lark EBNF
- Парсер должен корректно обрабатывать основные конструкции 1С
- Время парсинга небольших файлов (до 100 строк) должно быть не более 1 секунды
- Обеспечить устойчивость к ошибкам с информативными сообщениями

## Этап 2: Построение и расширение AST

### Задача 2.1: Разработка структуры AST

#### Требования и описание задачи

1. **Определение классов узлов AST**
   - Разработать базовый абстрактный класс узла AST
   - Создать иерархию классов для различных узлов:
     - Узлы для литералов (число, строка, дата, булево)
     - Узлы для переменных и идентификаторов
     - Узлы для операторов (арифметические, логические)
     - Узлы для управляющих конструкций
     - Узлы для объявлений (переменные, функции)
   - Реализовать методы для работы с узлами (добавление/удаление потомков)

2. **Реализация трансформации Lark-дерева в AST**
   - Создать классы-трансформеры для преобразования Lark-дерева в AST
   - Реализовать обработку различных правил грамматики
   - Добавить сохранение метаданных (позиция в исходном коде, комментарии)
   - Реализовать обработку ошибок преобразования

3. **Создание сериализации/десериализации AST**
   - Разработать механизм сериализации AST в JSON/XML
   - Реализовать десериализацию AST из JSON/XML
   - Обеспечить сохранение всех метаданных при сериализации
   - Реализовать валидацию при десериализации

4. **Разработка визуализатора AST**
   - Создать инструмент для визуализации AST в виде графа
   - Реализовать экспорт визуализации в различные форматы (PNG, SVG)
   - Добавить интерактивные возможности для анализа AST

#### Технические требования
- AST должен поддерживать как минимум 15 различных типов узлов
- Каждый узел должен содержать информацию о позиции в исходном коде
- Сериализованное представление AST должно быть человекочитаемым
- Визуализатор должен корректно отображать сложные иерархические структуры

### Задача 2.2: Расширение базовой грамматики

#### Требования и описание задачи

1. **Добавление поддержки для сложных условных конструкций**
   - Добавить поддержку операторов ElseIf/ИначеЕсли
   - Реализовать поддержку Case/When (Выбор/Когда)
   - Добавить тернарные операторы (если доступны в 1С)
   - Реализовать вложенные условные выражения

2. **Добавление поддержки для циклов различных типов**
   - Добавить поддержку цикла While/Пока
   - Реализовать ForEach/Для Каждого
   - Добавить операторы прерывания циклов (Прервать/Break)
   - Реализовать операторы продолжения циклов (Продолжить/Continue)

3. **Добавление поддержки для обработки исключений**
   - Реализовать блоки Try/Except (Попытка/Исключение)
   - Добавить поддержку вызова исключений (ВызватьИсключение)
   - Реализовать информацию об исключениях
   - Добавить блоки Finally (если доступны в 1С)

4. **Добавление поддержки для определения и использования классов**
   - Реализовать объявление классов
   - Добавить поддержку методов классов
   - Реализовать наследование (если доступно в 1С)
   - Добавить поддержку атрибутов классов

5. **Добавление поддержки для импорта модулей**
   - Реализовать импорт модулей
   - Добавить поддержку пространств имён
   - Реализовать квалифицированный доступ к элементам модулей
   - Добавить обработку циклических зависимостей

6. **Создание тестов для новых конструкций**
   - Разработать тесты для каждой новой конструкции
   - Создать интеграционные тесты для комбинированных конструкций
   - Реализовать проверки для крайних случаев

7. **Разработка механизма программного расширения грамматики**
   - Создать API для динамического расширения грамматики
   - Реализовать механизм добавления новых правил
   - Добавить проверку конфликтов при добавлении правил
   - Реализовать возможность отключения отдельных правил

#### Технические требования
- Расширенная грамматика должна поддерживать не менее 90% стандартных конструкций 1С
- Обеспечить обратную совместимость с ранее разработанными компонентами
- Добавить возможность отладки грамматики при возникновении проблем
- Обеспечить производительность парсинга средних файлов (до 500 строк) не более 3 секунд

## Этап 3: Интеграция с AI-агентами

### Задача 3.1: Настройка CrewAI и базовых агентов

#### Требования и описание задачи

1. **Интеграция фреймворка CrewAI**
   - Установить и настроить CrewAI
   - Интегрировать с основной системой
   - Настроить авторизацию и ключи API
   - Реализовать базовые классы для работы с фреймворком

2. **Разработка архитектуры агентов**
   - **Агент-исследователь**:
     - Создать агента для поиска информации о конструкциях 1С
     - Реализовать доступ к документации и примерам
     - Настроить обработку запросов к LLM
     - Добавить кэширование результатов поиска
   
   - **Агент-грамматик**:
     - Создать агента для генерации правил грамматики
     - Реализовать алгоритмы для анализа исходных текстов
     - Настроить интеграцию с LLM для генерации правил
     - Добавить механизм обучения на основе успешных генераций
   
   - **Агент-валидатор**:
     - Создать агента для проверки сгенерированных правил
     - Реализовать алгоритмы для тестирования правил на примерах
     - Настроить метрики успешности валидации
     - Добавить механизм обратной связи для других агентов
   
   - **Агент-оркестратор**:
     - Создать агента для координации работы остальных агентов
     - Реализовать логику последовательности операций
     - Настроить механизм разрешения конфликтов
     - Добавить интерфейс для мониторинга работы агентов

3. **Настройка окружения для работы агентов**
   - Создать конфигурационные файлы для агентов
   - Реализовать механизм хранения состояния агентов
   - Настроить логирование действий агентов
   - Добавить механизм восстановления после сбоев

#### Технические требования
- Агенты должны работать независимо друг от друга и взаимодействовать через сообщения
- Система должна поддерживать асинхронную работу агентов
- Время инициализации всех агентов не должно превышать 10 секунд
- Обеспечить отказоустойчивость при недоступности внешних сервисов (LLM)

### Задача 3.2: Реализация сценария обнаружения неизвестной конструкции

#### Требования и описание задачи

1. **Обработка ошибок парсинга и выделение неизвестных конструкций**
   - Создать механизм для обнаружения неизвестных конструкций
   - Реализовать алгоритм выделения контекста ошибки
   - Добавить классификацию типов неизвестных конструкций
   - Реализовать хранение информации о проблемных конструкциях

2. **Передача информации агенту-исследователю**
   - Создать протокол обмена данными между парсером и агентом
   - Реализовать механизм очередей для асинхронной обработки
   - Добавить приоритизацию запросов
   - Реализовать мониторинг состояния запросов

3. **Реализация сбора данных агентом-исследователем**
   - Создать механизм поиска в документации 1С
   - Реализовать анализ примеров кода
   - Добавить возможность запроса к LLM для анализа
   - Реализовать структурирование собранной информации

4. **Генерация правил грамматики агентом-грамматиком**
   - Создать алгоритм генерации правил Lark на основе собранных данных
   - Реализовать проверку синтаксической корректности правил
   - Добавить анализ потенциальных конфликтов с существующими правилами
   - Реализовать оптимизацию сгенерированных правил

5. **Валидация сгенерированных правил агентом-валидатором**
   - Создать набор тестов для проверки правил
   - Реализовать механизм проверки на тестовых примерах
   - Добавить метрики качества правил
   - Реализовать механизм обратной связи при проблемах

6. **Интеграция новых правил в существующую грамматику**
   - Создать механизм безопасного добавления правил
   - Реализовать контроль версий грамматики
   - Добавить возможность отката при проблемах
   - Реализовать обновление AST-трансформации для новых правил

#### Технические требования
- Время полного цикла обработки неизвестной конструкции не должно превышать 2 минуты
- Обеспечить успешное распознавание не менее 80% неизвестных конструкций
- Гарантировать отсутствие регрессий при добавлении новых правил
- Реализовать подробное логирование процесса для анализа проблем

## Этап 4: Тестирование и валидация

### Задача 4.1: Разработка системы тестирования

#### Требования и описание задачи

1. **Создание набора тестовых скриптов 1С**
   - **10 простых скриптов**:
     - Скрипты с базовыми операциями (переменные, условия)
     - Простые функции и процедуры
     - Базовые циклы и операторы
   
   - **15 средних скриптов**:
     - Комбинированные конструкции
     - Многомодульные программы
     - Работа с классами и объектами
   
   - **5 сложных скриптов**:
     - Реальные примеры из практики
     - Скрипты с редкими конструкциями
     - Сложные алгоритмические решения

2. **Реализация автоматического запуска тестов**
   - Создать систему CI для автоматического запуска тестов
   - Реализовать механизм запуска тестов после изменения грамматики
   - Добавить генерацию отчетов о тестировании
   - Реализовать уведомления о результатах тестирования

3. **Разработка механизма проверки регрессий**
   - Создать эталонные AST для тестовых скриптов
   - Реализовать сравнение с эталонными AST
   - Добавить анализ изменений при обновлении грамматики
   - Реализовать метрики для оценки отклонений от эталона

4. **Создание метрик для оценки качества парсинга**
   - Разработать метрики покрытия языковых конструкций
   - Реализовать оценку производительности парсинга
   - Добавить метрики точности построения AST
   - Реализовать агрегированные показатели качества

#### Технические требования
- Полный набор тестов должен запускаться за время не более 5 минут
- Метрики должны обеспечивать не менее 95% точности оценки качества
- Система должна обнаруживать не менее 98% регрессий
- Тесты должны работать в автоматическом режиме без вмешательства пользователя

### Задача 4.2: Реализация системы откатов

#### Требования и описание задачи

1. **Разработка механизма версионирования грамматики**
   - Создать систему нумерации версий грамматики
   - Реализовать хранение истории изменений
   - Добавить метаданные для каждой версии (автор, дата, описание)
   - Реализовать механизм сравнения версий

2. **Создание хранилища версий грамматики**
   - Разработать систему хранения версий (локальное/Git)
   - Реализовать механизм экспорта/импорта версий
   - Добавить индексацию для быстрого поиска
   - Реализовать механизм очистки устаревших версий

3. **Реализация обнаружения проблем после обновления**
   - Создать набор проверок для выявления проблем
   - Реализовать мониторинг производительности
   - Добавить механизм оценки совместимости
   - Реализовать систему предупреждений

4. **Автоматический откат при обнаружении ошибок**
   - Создать механизм быстрого отката к стабильной версии
   - Реализовать критерии принятия решения об откате
   - Добавить механизм блокировки проблемных версий
   - Реализовать уведомления о выполненных откатах

5. **Улучшенное логирование для отслеживания изменений**
   - Разработать систему структурированного логирования
   - Реализовать механизм анализа логов
   - Добавить агрегацию информации о проблемах
   - Реализовать визуализацию истории изменений

#### Технические требования
- Время отката к предыдущей стабильной версии не должно превышать 5 секунд
- Система должна хранить не менее 20 последних версий грамматики
- Обеспечить целостность данных при отказе системы в процессе отката
- Логи должны содержать полную информацию для восстановления состояния

## Этап 5: Развертывание и оптимизация

### Задача 5.1: Контейнеризация и развертывание

#### Требования и описание задачи

1. **Создание Dockerfile**
   - Разработать Dockerfile для упаковки системы
   - Реализовать многоэтапную сборку для оптимизации размера
   - Добавить необходимые зависимости и конфигурацию
   - Реализовать проверки безопасности

2. **Настройка параметризации через переменные окружения**
   - Создать систему параметризации через env-переменные
   - Реализовать валидацию значений переменных
   - Добавить документацию по доступным параметрам
   - Реализовать значения по умолчанию

3. **Разработка скриптов для развертывания**
   - Создать скрипты для различных сред (dev, test, prod)
   - Реализовать проверки перед развертыванием
   - Добавить возможность откатов при проблемах
   - Реализовать мониторинг процесса развертывания

4. **Документирование процесса установки**
   - Создать подробную документацию по установке
   - Реализовать описание требований к окружению
   - Добавить описание типовых проблем и их решений
   - Реализовать руководство по первоначальной настройке

#### Технические требования
- Размер итогового Docker-образа не должен превышать 2GB
- Время запуска контейнера до готовности должно быть не более 30 секунд
- Образ должен работать в средах Linux, Windows и MacOS
- Документация должна быть понятной для пользователей разного уровня

### Задача 5.2: Реализация горячего обновления и оптимизация

#### Требования и описание задачи

1. **Разработка механизма горячего обновления грамматики**
   - Создать систему обновления без перезапуска сервиса
   - Реализовать атомарность операций обновления
   - Добавить механизм блокировки на время обновления
   - Реализовать уведомления о выполненных обновлениях

2. **Оптимизация производительности парсинга и построения AST**
   - Провести профилирование узких мест
   - Реализовать алгоритмические оптимизации
   - Добавить механизмы кэширования
   - Реализовать параллельную обработку где возможно

3. **Добавление API для внешнего взаимодействия**
   - Создать REST API для работы с системой
   - Реализовать аутентификацию и авторизацию
   - Добавить документацию API (Swagger/OpenAPI)
   - Реализовать версионирование API

4. **Финальное тестирование и исправление проблем**
   - Провести комплексное тестирование всей системы
   - Реализовать стресс-тестирование
   - Добавить исправления выявленных проблем
   - Реализовать финальную оптимизацию

#### Технические требования
- Время горячего обновления грамматики не должно превышать 2 секунды
- Оптимизированная система должна обрабатывать файлы на 30% быстрее
- API должно обрабатывать не менее 100 запросов в секунду
- Система должна стабильно работать при длительной нагрузке (24+ часов)

## Метрики успеха проекта

### Метрики качества грамматики и парсинга
- **Процент успешно распознанных конструкций языка 1С: ≥ 95%**
  - Измерение: тестирование на репрезентативном наборе конструкций
  - Периодичность: после каждого значимого обновления грамматики

- **Точность построения AST (соответствие эталонному): ≥ 98%**
  - Измерение: сравнение с вручную проверенными эталонами
  - Периодичность: еженедельно

- **Время парсинга файла размером 1000 строк: ≤ 2 секунды**
  - Измерение: среднее время на стандартном тестовом наборе
  - Периодичность: после оптимизаций производительности

### Метрики AI-агентов
- **Процент успешной идентификации неизвестных конструкций: ≥ 85%**
  - Измерение: тестирование на наборе ранее неизвестных конструкций
  - Периодичность: после каждого обновления логики агентов

- **Процент корректно сгенерированных правил грамматики: ≥ 80%**
  - Измерение: проверка сгенерированных правил экспертами
  - Периодичность: ежемесячно

- **Среднее время обработки новой конструкции: ≤ 90 секунд**
  - Измерение: среднее время полного цикла обработки
  - Периодичность: после оптимизаций производительности

### Метрики стабильности и надежности
- **Время восстановления после сбоя (откат): ≤ 5 секунд**
  - Измерение: время отката к стабильной версии
  - Периодичность: при каждом инциденте

- **Количество успешных обновлений грамматики без регрессий: ≥ 90%**
  - Измерение: отношение успешных обновлений к общему числу
  - Периодичность: ежемесячно

- **Доступность системы (uptime): ≥ 99.9%**
  - Измерение: время работы без сбоев
  - Периодичность: ежемесячно 