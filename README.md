# Get Covid-19 info through Telegram!

This RASA Chatbot sends you Covid-19 data of Brazil, São Paulo, São Carlos and Atibaia via [Telegram](https://telegram.org/)

## Prerequisites

1. First of all, you will need [Python](https://www.python.org) installed.
2. If you are running on windows, you should get the [Chocolatey](https://chocolatey.org/install).

    2.1 After installing [Chocolatey](https://chocolatey.org/install) you should run de command below to install the following packages: git, make, docker and docker-compose

    ```bash
    choco install git
    choco install make
    choco install docker
    choco install docker-compose
    ```

3. Now you need to configure your [Telegram](https://telegram.org/) bot.

    3.1 Click at this [link](https://telegram.me/BotFather) to open Botfather and send the command "/newbot". Follow it's instructions and you will will be rewarded with a token.

    3.2 Add the infos at the *credentials.yml* file.

4. Create a *AWS S3 Bucket* and add the keys at the *secrets_aws.py*

5. You also need to configure the path from which your rasa port is connected at the *credentials.yml* file, it need to be a public one:
    ```
    webhook_url: "https://<your public url>:<your rasa port>/webhooks/telegram/webhook"
    ```
6. Finally, just run the containers and send messages with telegram!
    ```
    docker-compose up -d
    ```
## Licence

[MIT](https://choosealicense.com/licenses/mit/)

[rasa](https://rasa.com//)