.PHONY: production visual visual-cli visual-real visual-smoke ollama-up ollama-down ollama-status ollama-logs ollama-restart ollama-pull ollama-chat

production:
	@./scripts/run-production.sh

visual:
	@./scripts/run-visual.sh

visual-cli:
	@APEX_VISUAL_LAUNCH_CLI=1 APEX_VISUAL_DRY_RUN=1 ./scripts/run-visual.sh

visual-real:
	@APEX_VISUAL_LAUNCH_CLI=1 APEX_VISUAL_DRY_RUN=0 ./scripts/run-visual.sh

visual-smoke:
	@QT_QPA_PLATFORM=offscreen QT_QUICK_BACKEND=software ./scripts/run-visual.sh --auto-close-ms 900

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
