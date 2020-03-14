# Сбор статистики в социальных сетях
Данная программа, поможет вам проанализировать посты в ваших социальных сетях и показать ядро ваших поклонников.


## Как установить

Python3 должен быть уже установлен. Затем используйте pip (или pip3, есть конфликт с Python2) для установки зависимостей:<br>

``` git clone https://github.com/djeck1432/amplifer.git ```

После того, как скачали репозиторий, откройте в терминале(MacOs) или в консоли(Linux) папку ```amplifer``` следующей командой:<br>

```cd amplifer```

Для того, что бы запустить код, нужно установить необходимые библиотеки:<br>

```pip install -r requirements.txt ```<br>

Готово, мы установили проект и все необходимые библиотеки у нас на компьютере.
<br>
## Как запустить 
Для запуска скрипта, в терминале выполните следующую команду:<br>
```python smm_analyze.py [соцальная сеть]```<br>
```instagram``` - instagram;<br>
```facebook``` - facebook; <br>
```vkontakte``` - vkontakte;<br>
Пример запуска:<br>
```python smm_analyze.py instagram```<br>


## Переменные окружения 

```INSTAGRAM_LOGIN``` - логин в ```Instagram```;<br>
```INSTAGRAM_PASSWORD``` - пароль от ```Instagram```;<br>
<br>
```VK_TOKEN``` - токен от  ```Vkontakte```;<br>
<br>
```FACEBOOK_TOKEN```- токен от ```Facebook```;<br>
```FACEBOOK_GROUP_ID``` - ```id``` группы в  ```Facebook```;
