# Get Covid-19 info through Telegram!

This program sends you Covid-19 data of Brazil, São Paulo, São Carlos and Atibaia via [Telegram](https://telegram.org/)

## Prerequisites

1. First of all, you will need [Python](https://www.python.org) installed.
2. If you are running on windows, you should get the [Chocolatey](https://chocolatey.org/install).

    2.1 After installing [Chocolatey](https://chocolatey.org/install) you should run de command below to install the Make package.

    ```bash
    choco install make
    ```

3. Now you need to configure your [Telegram](https://telegram.org/) bot.

    3.1 Click at this [link](https://telegram.me/BotFather) to open Botfather and send the command "/newbot". Follow it's instructions and you will will be rewarded with a token.

    3.2 To config you bot on [Telegram](https://telegram.org/) you need to run the command below and inser the token when expected.

    ```bash
    make telegram-config
    ```
    
4. To run the apllication go into the virtual enviroment using
    ```bash
    start .\venv\Scripts\activate
    ``` 
    for Windows and
    ```bash
    source venv/Scripts/activate
    ```
    for Linux. Then just type the code below while inside the Covid_Data Folder
    ```bash
    make send
    ```

## Licence

[MIT](https://choosealicense.com/licenses/mit/)

[telegram-send](https://pypi.org/project/telegram-send/)