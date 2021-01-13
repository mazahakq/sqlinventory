Скрипт python для AWX Custom Inventory  
Выполняет получение списка узлов из БД, разбивает на группы и применяет переменные  
Скрипт использует pyodbc для работы с БД, что требует установку пакета на хосте AWX  
Используемый Драйвер ODBC должен быть предустановлен на хосте AWX  
  
Переменные окружения (обязательные, рекомендовано указывать в credential):  
  HOSTNAME_DATABASE - Хост базы данных  
  NAME_DATABASE     - Имя базы данных  
  DRIVER_ODBC       - Драйвер подключения к БД (default {ODBC Driver 17 for SQL Server})  
  USERNAME_DATABASE - Логин подключения к БД  
  PASSWORD_DATABASE - Пароль подключения к БД  
  
Для работы с AWX рекомендуется создать Custom Type Credential, описанных в каталоге object  
  injector_cred_type_database.yaml  
  input_cred_type_database.yaml  
  
Дополнительные переменные окружения:  
  SCRIPTSQL_FILE    - Имя файла скрипта расположенного в каталоге sql (default inventory.sql)  
  SCRIPT_TEXT       - Текст скрипта, если указан переопределяет использование файла скрипта SCRIPTSQL_FILE  
  
Переменные окружения для скрипта sql (заменяет $example в тексте скрипта):  
  SQL_REGION       - Площадка узлов  
  SQL_COMPLEX   - Комплекс узлов  
  SQL_SUBSYSTEM - Подсистема узлов  
  SQL_CIRCUIT   - Контур узлов  
  SQL_SEGMENT   - Сегмент узлов  
  SQL_DOMAIN    - Домен узлов  
  SQL_ROLE      - Роль узлов  
  При указании переменных использовать конструкцию: "'Название площадки'", либо если список "'Название площадки 1','Название площадки 2'"  
  
Применяемые индивидуальные переменные для узлов:  
  'region'    - Площадка узла из БД  
  'complex'   - Комплекс узла из БД  
  'subsystem' - Подсистема узла из БД  
  'circuit'   - Контур узла из БД  
  'segment'   - Сегмент узла из БД  
  'domain'    - Домен узла из БД  
  'role'      - Роль узла из БД  
  
Группировка узлов:  
  Группировка по ОС - WINDOWS и LINUX  
  Применение переменные для группы из файлов конфигурации каталога vars:  
    vars_linux.yaml  
    vars_windows.yaml  
  
Для локальной отладки необходимо установить:  
  python3  
  pip  
  Через pip установить pyodbc (example: pip install pyodbc -i http://n7701-suimpporeg:8081/repository/piprepo/simple --trusted-host n7701-suimpporeg)  
  Информация по установке ODBC драйвера - https://docs.microsoft.com/ru-ru/sql/connect/python/pyodbc/python-sql-driver-pyodbc?view=sql-server-ver15  
  
Пример определение переменных в WINDOWS:  
  $env:HOSTNAME_DATABASE="Hostname";  
  $env:NAME_DATABASE="Dbname";  
  $env:USERNAME_DATABASE="user";  
  $env:PASSWORD_DATABASE="";  
  $env:DRIVER_ODBC="{ODBC Driver 17 for SQL Server}";  
  
Пример определение переменных в LINUX:  
  HOSTNAME_DATABASE="Hostname"  
  NAME_DATABASE="Dbname"  
  USERNAME_DATABASE="user"  
  PASSWORD_DATABASE=""  
  DRIVER_ODBC="{ODBC Driver 17 for SQL Server}"  
  
При использовании переменных среды убедитесь, что python их использует (работает в одном окружении).  