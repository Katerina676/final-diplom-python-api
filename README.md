# Дипломная работа к профессии Python-разработчик «API Сервис заказа товаров для розничных сетей».

## Описание

Приложение предназначено для автоматизации закупок в розничной сети. Пользователи сервиса — покупатель (менеджер торговой сети, который закупает товары для продажи в магазине) и поставщик товаров.

**Клиент (покупатель):**

- Менеджер закупок через API делает ежедневные закупки по каталогу, в котором
  представлены товары от нескольких поставщиков.
- В одном заказе можно указать товары от разных поставщиков — это
  повлияет на стоимость доставки.
- Пользователь может авторизироваться, регистрироваться и восстанавливать пароль через API.
    
**Поставщик:**

- Через API информирует сервис об обновлении прайса.
- Может включать и отключать прием заказов.
- Может получать список оформленных заказов (с товарами из его прайса).


### Задача

Необходимо разработать backend-часть (Django) сервиса заказа товаров для розничных сетей.

**Базовая часть:**
* Разработка сервиса под готовую спецификацию (API);
* Возможность добавления настраиваемых полей (характеристик) товаров;
* Импорт товаров;
* Отправка накладной на email администратора (для исполнения заказа);
* Отправка заказа на email клиента (подтверждение приема заказа).

**Продвинутая часть:**
* Выделение медленных методов в отдельные процессы (email, импорт, экспорт).



### Для запуска проекта необходимо:

Установить зависимости:

```bash
pip install -r requirements.txt
```

Вам необходимо будет создать базу и прогнать миграции:

```bash
manage.py makemigrations
manage.py migrate
manage.py createsuperuser
```

Выполнить команду:

```bash
python manage.py runserver
```
### Прописать адрес Redis сервера в settings 

Выполнить команду в втором терминале:

```bash
celery -A netology_pd_diplom worker -l INFO -P eventlet
```
Запустить тесты:
```bash
pytest
```