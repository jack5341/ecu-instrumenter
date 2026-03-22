.PHONY: run deploy

# Set your Miyoo Mini's IP address here (can be overridden via command line)
MIYOO_IP ?= 192.168.1.53

run:
	python3 ecu_dashboard.py

deploy:
	@echo "Packaging and transferring application to Miyoo Mini over SSH..."
	@mkdir -p ./ECUInstrumenter
	@cp *.py config.json launch.sh assets/icon.png ./ECUInstrumenter/
	@scp -r ./ECUInstrumenter root@$(MIYOO_IP):/mnt/SDCARD/App/
	@rm -rf ./ECUInstrumenter
	@echo "\nDeployment complete! You can launch 'ECU Instrumenter' on your Miyoo Mini now."
