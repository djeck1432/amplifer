# Сбор статистики в социальных сетях
Данная программа, поможет вам проанализировать посты в ваших социальных сетях и показать ядро ваших поклонников.


## How to install

Python3 have to be already installed. Then use pip (or pip3, there is a contravention with Python2) to install dependencies: :<br>

``` git clone https://github.com/djeck1432/amplifer.git ```

After you downloaded the repository open a folder ```amplifer``` using next command: <br>

```cd amplifer```

Now all of the required libraries and modules have to be installed:<br>

```pip install -r requirements.txt ```<br>

Now we are ready for the script .
## Как запустить 
Для запуска скрипта, в терминале выполните следующую команду:<br>
```python smm_analyze.py [социальная сеть]```<br>
```instagram``` - instagram;<br>
```facebook``` - facebook; <br>
```vkontakte``` - vkontakte;<br>
Пример запуска:<br>
```python smm_analyze.py instagram```<br>


## Переменные окружения 

```INSTAGRAM_LOGIN``` - логин в ```Instagram```;<br>
```INSTAGRAM_PASSWORD``` - пароль от ```Instagram```;<br>
```INSTAGRAM_ACCAUNT``` - имя аккаунта в ```Instagram```;<br>
<br>
```VK_TOKEN``` - токен от  ```Vkontakte```;<br>
```VK_GROUP_NAME ```- названия группы в ```Vkontakte```;<br>
<br>
```FACEBOOK_TOKEN```- токен от ```Facebook```;<br>
```FACEBOOK_GROUP_ID``` - ```id``` группы в  ```Facebook```;
