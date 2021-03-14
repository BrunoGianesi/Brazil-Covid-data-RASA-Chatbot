.PHONY: send
send: Telegram.py
	python Telegram.py

.PHONY: telegram-config
telegram-config: 
	telegram-send --configure
	