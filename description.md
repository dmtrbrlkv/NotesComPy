# Библиотека NotesComPy

Библиотека позволяет взаимодействовать с объектами Notes через COM

## Ограничения
Взаимодействие реализовано через COM, поэтому работает только под Windows. Также необходим установленный клиент IBM Lotus Notes (HCL Notes). Подлючение идет от имени пользователя, указанного в файле конфигурации Notes (notes.ini). Также возможна работа от текущего залогиненного пользователя.

## Доступные классы
Реализованы следующие основные классы и их методы:
* NotesSession
* NotesDatabase
* NotesDocument
* NotesView
* NotesDocumentCollection
* NotesACL
* NotesACLEntry
* NotesAgent
* NotesLog

Для расширенной работы с коллекциям документов реализован класс CustomCollection, позволяющий работать с документами из разных баз и эмулирующий тразакционное сохранение.
Для большинства классов раелизована возможость экспорта данных и другие возможности, изначально отсутвующие в классах Notes.


## Работа с библиотекой
Разберем основный возможности библиотеки на примере работы с простой notes базой IT crowd. База состоит из двух справочников - Levels и  Languages и основной карточки Person.

Справочник языков программирования:
![Языки программирования](img/languages.png)

Справочник уровней:
![Уровни](img/levels.png)

Сотрудники:
![Сотрудники](img/persons.png)

Для сотрудника можно указать ФИО и телефон и выбрать из справочника языки, которыми он владеет и его уровень:
![Сотрудник](img/person.png)

В справочниках есть кнопка **Update person**, запускающая агент, обновляющий в карточках сотрудников измененное название языка или уровня.

#### Инициализация
Прежде всего необходимо проинициализировать сессию, передав в нее пароль от текущего user.id:
```
from notescompy import init_session, open_database
s = session.init_session("python")
```
Можно посмотреть текущего пользователя:

```
print(s.UserName)
```

> CN=Python/O=PyLN

#### Работа с базой
Теперь можно получить базу, передав сервер и путь:
```
db = open_database('PyLN', 'itcrowd.nsf')
```

Посмотрим размер базы и ее название:

```
print(db.title, db.size)
```
> IT Crowd 884736.0

Из базы можно получить коллекцию всех документов, ACL, получить конкретный документ или создать новый, получить представление и агент:
```
all_col = db.all_documents
acl = db.acl
doc = db.get_document_by_unid("9A899214038E229843258541003BFFDB")
new_doc = db.create_document()
view = db.get_view("Levels")
agent = db.get_agent("UpdatePerson")
```
Работу с получившимися объектами разберем в соотвествующий разделах.

Также доступен поиск по формуле. Обычно вторым и третьим параметрами мы передаем Nothing и 0, поэтому эти значения заданы по умолчанию, достаточно задать только формулу.

Надем всех сотрудников, у которых в имени встречается John:

```
col = db.search("@contains(FullName;'John'")
```

#### Документ
Для начала возьмем документ из примера с базой:
```
from notescompy import init_session, open_database
s = init_session("python")
db = open_database('PyLN', 'itcrowd.nsf')
doc = db.get_document_by_unid("9A899214038E229843258541003BFFDB")
```
Посмотрим его форму:
````
print(doc.get_item_value("Form"))
````
> ['Person']

Как вы могли заметить, наименование методов слегка не привычно, в LotusScript мы привыкли к `doc.GetItemValue`, однако это не соответствует требованиям PEP8. Тем не менее реализована возможносты обращаться к методам и свойстам с привычными наименованиями.
Посмотрим значение поля Level LotusScript-стиле
```
print(doc.GetItemValue("Level"))
```
> ['Senior']

Как известно, `GetItemValue` возвращает массив значений (список в Python), даже если значение в поле одно и мы постоянно берем от него нулевое значение
```
print(doc.get_item_value("Level")[0])
```
> Senior

Но это же Python, должен быть сахар и это метод `get_item_value0`
```
print(doc.get_item_value0("Level"))
```
> Senior

В обоих случаях возвращается не список, а строка.

Создадим новый документ в сравочнике языков:
```
lang_doc = db.create_document()
lang_doc.replace_item_value("Form", "Language")
lang_doc.replace_item_value("Name", "Go")
lang_doc.replace_item_value("Description", "Go is an open source programming language that makes it easy to build simple, reliable, and efficient software")
```
На форме есть вычисляемое поле UNID, поэтому вызовем метод `compute_with_form`:
```
lang_doc.compute_with_form()
```
и сохраним (обычно мы сохраняем `doc.Save(True, False)`, поэтому эти значения заданы по умолчанию и их можно опустить):
```
lang_doc.save()
```
В базе появился новый документ:
![Go](img/go.png)


Часто, при получении значений из документа, нужно не одно поле, а сразу несколько, а иногда и какие-то свойства документа или результаты вычисления формул. Для этого можно применить метод `get_values`, который вернет все значения как словарь:

```
values = lang_doc.get_values(["Form", "Name"], "Universalid", "@created", "Дата создания")
print(values)
```
> {'Form': ['Language'], 'Name': ['Go'], 'Universalid': 'C56A8822BD4C0FF54325854C00536CCE', 'Дата создания': [datetime.datetime(2020, 4, 16, 18, 11, 13)]}

А когда нам не нужны списки, можно вернут значения в виде еденичных значений, передав параметр `no_list=True`:

```
values = lang_doc.get_values(["Form", "Name"], "Universalid", "@created", "Дата создания", no_list=True)
print(values)
```
> {'Form': 'Language', 'Name': 'Go', 'Universalid': 'C56A8822BD4C0FF54325854C00536CCE', 'Дата создания': datetime.datetime(2020, 4, 16, 18, 11, 13)}

#### Представления
Получим представление с уровнями:
```
from notescompy import init_session, open_database
s = init_session("python")
db = open_database('PyLN', 'itcrowd.nsf')
view = db.get_view("Levels")
```

Проитерируемся по представлению в LS-стиле:
```
doc = view.get_first_document()
while doc:
    print(doc.universal_id)
    doc = view.get_next_document()
```

Также представление поддерживает питоновский протокол итерации:
```
for doc in view:
    print(doc.universal_id)
```

В обоих случая получим униды всех документов в представлении:
> 8C5A8BCE0F3666A84325854100363E5D
38187A89713365CB4325854100363BF7
0FB66AA59EAE2A0B43258541003638ED

Второй из наиболее используемых методов работы с представлением - это отбор документов по ключу. Возьмем представления с сотрудниками, отсортированное по униду уровня, и отберем всех, знающих Python (унид справочника - 3F1B416909DE674043258541003445AA)

```
view = db.get_view("srchPersonsByLanguage")
col = view.get_all_documents_by_key("3F1B416909DE674043258541003445AA")
print(col.count)
```
> 3

Получили коллекцию из трех документов.


Если нам нужны значения все документов прдставления в том виде, как они отображаются в представлении, то можно воспользоваться методом `get_values`. Возьмем представление с сотрудниками, значения получим как строки, а для объединения мультизначных полей будет использовать / 
![Сотрудники](img/view_values.png)
```
view = db.get_view("Persons")
values = view.get_values(no_list=True, sep= "/")
print(values)
```
> {'F219AA2C843B6DD743258541003C1E99': {'Full name': 'Bill G', 'Level': 'Senior', 'Languages': 'C++', 'Phone': ''}, 'A5426F32DBE6B94143258541003C40CE': {'Full name': 'Gena O Possum', 'Level': 'Junior', 'Languages': 'Python', 'Phone': ''}, '9A899214038E229843258541003BFFDB': {'Full name': 'Ivan Kuznetsov', 'Level': 'Senior', 'Languages': 'Java/Python/C++', 'Phone': ''}, 'DFBCDDFEE3D0764C432585410046CFFE': {'Full name': 'John Cena', 'Level': 'Senior', 'Languages': '', 'Phone': '+7 777 777 77 77'}, '45A4A1F61B47769443258541003609B3': {'Full name': 'John Smith', 'Level': 'Middle', 'Languages': 'Python', 'Phone': ''}}

#### Коллекции