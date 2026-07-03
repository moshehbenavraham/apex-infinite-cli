.PHONY: ollama-up ollama-down ollama-status ollama-logs ollama-restart ollama-pull ollama-chat

ollama-up:
	@./scripts/ollama-docker.sh up

ollama-down:
	@./scripts/ollama-docker.sh down

ollama-status:
	@./scripts/ollama-docker.sh status

ollama-logs:
	@./scripts/ollama-docker.sh logs

ollama-restart:
	@./scripts/ollama-docker.sh restart

ollama-pull:
	@./scripts/ollama-docker.sh pull

ollama-chat:
	@./scripts/ollama-docker.sh --chat
