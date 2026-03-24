.PHONY: run deploy

MIYOO_IP ?= 192.168.1.53

run:
	python3 app.py

deploy:
	@echo "Packaging and transferring application to Miyoo Mini over SSH..."
	@mkdir -p ./ECUInstrumenter
	@cp __init__.py app.py config.json settings.json launch.sh ./ECUInstrumenter/ 2>/dev/null || :
	@cp -R assets config core models sim ui ./ECUInstrumenter/
	@scp -r ./ECUInstrumenter root@$(MIYOO_IP):/mnt/SDCARD/App/
	@rm -rf ./ECUInstrumenter
	@echo "\nDeployment complete! You can launch 'ECU Instrumenter' on your Miyoo Mini now."
