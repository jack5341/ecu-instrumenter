.PHONY: run deploy check

MIYOO_IP ?= 192.168.1.53

check:
	@echo "Compiling Python files to check syntax..."
	@python3 -m py_compile app.py mock_server.py
	@find core ui sim models config -name "*.py" -exec python3 -m py_compile {} +
	@echo "✅ All Python files passed syntax check!"

run:
	python3 app.py

deploy:
	@echo "Checking for uncommitted changes..."
	@if [ -n "$$(git status --porcelain)" ]; then \
		echo "ERROR: You have uncommitted changes. Please commit first!"; \
		exit 1; \
	fi
	@echo "Pushing changes to remote repository..."
	@git push
	@echo "Syncing via Git on Miyoo Mini..."
	@ssh root@$(MIYOO_IP) " \
		if [ ! -d '/mnt/SDCARD/App/ECUInstrumenter/.git' ]; then \
			echo 'Repository not found. Cloning for the first time...'; \
			cd /mnt/SDCARD/App && git clone https://github.com/jack5341/ecu-instrumenter.git ECUInstrumenter; \
		else \
			cd /mnt/SDCARD/App/ECUInstrumenter && git pull origin main; \
		fi && \
		find /mnt/SDCARD/App/ECUInstrumenter -name '*.pyc' -delete"
	@echo "\nDeployment complete! You can launch 'ECU Instrumenter' on your Miyoo Mini now."
