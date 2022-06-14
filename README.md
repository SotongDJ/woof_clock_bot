# woof_clock_bot

Chatbot that base on Mastodon.py for Mastodon instance

## Installation

* clone repo and submodule

    * Windows

    ```pwsh
    git clone https://github.com/SotongDJ/woof_clock_bot.git
    cd woof_clock_bot
    git submodule init
    git submodule update --init --recursive
    # future submodule update
    git submodule update --remote --recursive
    ```

    * Linux

    ```bash
    git clone https://github.com/SotongDJ/woof_clock_bot.git
    cd woof_clock_bot
    git submodule init
    git submodule update --init --recursive
    # future submodule update
    git submodule update --remote --recursive
    ```

## Configuration

* set [bot_name] in self.bot_name

* prepare secret/token file

    * secret-[bot_name].json

    ```JSON
    {
        "access_token": "API token",
        "hostname" : "https://insert your mastodon instance"
    }
    ```

    * config-[bot_name].json

    ```JSON
    {
        "sleep_time": 60
    }
    ```

