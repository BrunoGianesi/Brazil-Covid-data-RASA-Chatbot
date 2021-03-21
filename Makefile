.PHONY: start
start:
	docker-compose up -d
.PHONY: end
end:
	docker-compose down