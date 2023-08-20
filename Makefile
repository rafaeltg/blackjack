install:
	docker build -t blackjack .

play:
	@docker run -it --rm blackjack

test:
	@docker run -it --rm -v "./:/app" blackjack sh /app/blackjack/scripts/test.sh