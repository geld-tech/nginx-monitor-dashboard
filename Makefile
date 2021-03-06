# Globals
LOCAL_DEV_ENV=local-dev-env
LOCAL_CACHE=.cache
SRV_DEV_ENV=local-dev-env/server
NPM_DEV_ENV=local-dev-env/webapp

# Package Details
PACKAGE_NAME=nginx-monitor-dashboard
PACKAGE_DESC=Running application locally
PACKAGE_AUTHOR=geld.tech
PACKAGE_VERSION=0.0.1
PACKAGE_DATE=01-01-1970
PACKAGE_DIR=/opt/geld/webapps/$(PACKAGE_NAME)

# UI Tests
PROTO=http
HOST=0.0.0.0
PORT=5000
WAIT=10

## Run all targets locally
all: stop save-cache clean isort lint local-dev-env test vue-dev-tools npm-install npm-lint npm-audit npm-build webapp-setup webapp-settings
	@echo "Build completed successfully!"

## Remove all local build artifacts
clean: stop clean-pyc
	$(call echo_title, "LOCAL DEV ENV CLEANUP")
	rm -rf $(LOCAL_DEV_ENV)

## Remove python artifacts
clean-pyc:
	$(call echo_title, "PYTHON FILES CLEANUP")
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.pyo' -exec rm --force {} +

## Clean all files including cache for NPM
clean-all: clean
	$(call echo_title, "CACHE FILES CLEANUP")
	-rm -rf $(LOCAL_CACHE)

## Save NPM cache
save-cache:
	$(call echo_title, "SAVE CACHE")
	@echo "== NPM =="
	@if [ -d "$(LOCAL_DEV_ENV)/webapp/node_modules/" ]; then \
	    rm -rf $(LOCAL_CACHE)/node_modules/; \
	    mkdir -p $(LOCAL_CACHE); \
	    mv $(LOCAL_DEV_ENV)/webapp/node_modules/ $(LOCAL_CACHE) ||: ; \
	fi

## Sort Python import statements
isort:
	$(call echo_title, "PYTHON ISORT")
	sh -c "isort --skip-glob=.tox --recursive sources/server/ "

## Check coding style of Flask application, enforce no syntax errors or undefined names, and flags other issues
lint:
	$(call echo_title, "PYTHON LINTER")
	flake8 sources/server/ --show-source --max-line-length=239 --max-complexity=10 --statistics --count

## Run unit tests (alongside a stub status service)
tests:
	@$(MAKE) test
	@$(MAKE) nginx-status-stop > /dev/null

## Private target to run unit tests
test: nginx-status-start
	$(call echo_title, "PYTHON UNIT TESTS")
	python -m unittest discover -s tests
	@sleep 3

## Run UI Tests (overridable parameters: PROTO, HOST, PORT, WAIT)
test-ui:
	$(call echo_title, "PYTHON SELENIUM UI TESTS")
	@echo "Executing UI tests on $(PROTO)://$(HOST):$(PORT) (delay of $(WAIT) seconds)"
	ls tests/uiTest*.py | xargs -i python {} --proto=$(PROTO) --host=$(HOST) --port=$(PORT) --delay=$(WAIT)

## Prepare local development environment
local-dev-env:
	$(call echo_title, "LOCAL DEV ENV")
	@echo "== Prepare folders =="
	mkdir -p $(LOCAL_DEV_ENV)
	cp -r sources/server/ $(LOCAL_DEV_ENV)
	cp -r sources/webapp/ $(LOCAL_DEV_ENV)
	cp -r stub/ $(LOCAL_DEV_ENV)
	$(eval PACKAGE_NAME=localdev)
	@echo "== Replace place holders =="
	find $(LOCAL_DEV_ENV) -type f | xargs sed -i "s/__PACKAGE_NAME__/$(PACKAGE_NAME)/g"
	find $(LOCAL_DEV_ENV) -type f | xargs sed -i "s/__PACKAGE_DESC__/$(PACKAGE_DESC)/g"
	find $(LOCAL_DEV_ENV) -type f | xargs sed -i "s/__PACKAGE_AUTHOR__/$(PACKAGE_AUTHOR)/g"
	find $(LOCAL_DEV_ENV) -type f | xargs sed -i "s/__VERSION__/$(PACKAGE_VERSION)/g"
	find $(LOCAL_DEV_ENV) -type f | xargs sed -i "s/__DATE__/$(PACKAGE_DATE)/g"
	@if [ -d "$(LOCAL_CACHE)/node_modules/" ]; then \
		echo "== Restore NPM cache =="; \
		set -x; \
		mv $(LOCAL_CACHE)/node_modules/ $(LOCAL_DEV_ENV)/webapp/ ||: ; \
		set +x; \
	fi

## Ensure Vue application is built with DevTools enabled (requires Firefox or Chrome plugin)
vue-dev-tools:
	$(call echo_title, "VUE DEVTOOLS")
	sed -i '/Vue.config.productionTip = false/a Vue.config.devtools = true' $(LOCAL_DEV_ENV)/webapp/src/main.js

## Install NPM Modules in local dev environment
npm-install: local-dev-env
	$(call echo_title, "NPM INSTALL")
	cd $(NPM_DEV_ENV) ; npm install

## Runs linter on Vue web application files
npm-lint: npm-install
	$(call echo_title, "NPM LINT")
	cd $(NPM_DEV_ENV) ; npm run lint

## Runs NPM audit to flag security issues
npm-audit: npm-install
	# On case of a failure, run conditionally using the - prefix (see command  below):
	#	-cd $(NPM_DEV_ENV) ; npm audit   # Failures ignored locally with -, but will be executed on Travis before distribution
	#
	# Or, upgrade nodejs/npm such as the following on CentOS/EL 7 systems via repository:
	#	/usr/bin/yum remove -y nodejs
	#	/usr/bin/yum clean all
	#	/bin/rm -rf /var/cache/yum
	#	/bin/rm /etc/yum.repos.d/nodesource*
	#	/usr/bin/curl --silent --location https://rpm.nodesource.com/setup_8.x | bash -
	#
	$(call echo_title, "NPM AUDIT")  # Run conditionally as not installed on all systems
	cd $(NPM_DEV_ENV) ; npm audit    # NPM Audit introduced in npm 6

## Runs a full build using NPM
npm-build: npm-install
	$(call echo_title, "NPM BUILD")
	cd $(NPM_DEV_ENV) ; npm run build

## Start metrics collector daemon
daemon-start:
	$(call echo_title, "START METRICS DAEMON")
	@echo "Starting stub background daemon locally, use 'make daemon-stop' to terminate.."
	@echo ""
	python $(SRV_DEV_ENV)/monitor-collectord.py start --debug
	@echo ""
	@sleep 3

## Stop metrics collector daemon
daemon-stop:
	$(call echo_title, "STOP METRICS DAEMON")
	-python $(SRV_DEV_ENV)/monitor-collectord.py stop
	-pkill -f $(SRV_DEV_ENV)/monitor-collectord.py

## Prepare application
webapp-setup: npm-build
	$(call echo_title, "PREPARE")
	mkdir $(SRV_DEV_ENV)/static/
	cp -r $(NPM_DEV_ENV)/static/* $(SRV_DEV_ENV)/static/
	cp -r $(NPM_DEV_ENV)/dist/css/ $(SRV_DEV_ENV)/static/
	cp -r $(NPM_DEV_ENV)/dist/js/ $(SRV_DEV_ENV)/static/
	mkdir $(SRV_DEV_ENV)/templates/
	cp $(NPM_DEV_ENV)/dist/*.html $(SRV_DEV_ENV)/templates/

## Create a stub settings.cfg file
webapp-settings:
	$(call echo_title, "CREATE STUB SETTINGS")
	@touch $(SRV_DEV_ENV)/config/settings.cfg.dev
	@echo "[admin]" >> $(SRV_DEV_ENV)/config/settings.cfg.dev
	@echo "password = Y25mZmpiZXExMjM=" >> $(SRV_DEV_ENV)/config/settings.cfg.dev
	@echo "" >> $(SRV_DEV_ENV)/config/settings.cfg.dev
	@echo "[ganalytics]" >> $(SRV_DEV_ENV)/config/settings.cfg.dev
	@echo "ua_id = 1234567" >> $(SRV_DEV_ENV)/config/settings.cfg.dev

## Configure stub settings.cfg
webapp-config: webapp-settings
	$(call echo_title, "SETUP STUB SETTINGS")
	cp -f $(SRV_DEV_ENV)/config/settings.cfg.dev $(SRV_DEV_ENV)/config/settings.cfg

## Start web application
webapp-start:
	$(call echo_title, "START WEB APPLICATION")
	@python -c  "import os; print os.urandom(24)" > $(SRV_DEV_ENV)/config/secret.uti
	@echo "Starting web application locally, use 'make webapp-stop' to terminate.."
	@echo ""
	python $(SRV_DEV_ENV)/application.py &
	@echo ""
	@sleep 1

## Stop web application
webapp-stop:
	$(call echo_title, "STOP WEB APPLICATION")
	-pkill -f $(SRV_DEV_ENV)/application.py

## Start Nginx status stub daemon
nginx-status-start:
	$(call echo_title, "START NGINX STATUS STUB DAEMON")
	@echo ""
	-python $(SRV_DEV_ENV)/../stub/nginx-status-stub.py &
	-sleep 3

## Stop Nginx status stub daemon
nginx-status-stop:
	$(call echo_title, "STOP NGINX STATUS STUB DAEMON")
	@echo ""
	-pkill -f $(SRV_DEV_ENV)/../stub/nginx-status-stub.py

## Start local development environment
start: all nginx-status-start daemon-start webapp-start

## Stop local development environment
stop: daemon-stop webapp-stop nginx-status-stop

## Validate latest .deb package on a local Ubuntu image with Docker
docker-run-deb:
	$(call echo_title, "DOCKER RUN DEB")
	sudo docker run -i -t -p $(PORT):8004 --rm ubuntu:xenial /bin/bash -c ' apt clean all && apt update ; \
		apt install -y python wget vim ; \
		wget https://raw.githubusercontent.com/gdraheim/docker-systemctl-replacement/master/files/docker/systemctl.py ; \
		cp /usr/bin/systemctl /usr/bin/systemctl.bak ; \
		yes | cp -f systemctl.py /usr/bin/systemctl ; \
		chmod a+x /usr/bin/systemctl ; \
		test -L /bin/systemctl || ln -sf /usr/bin/systemctl /bin/systemctl ; \
		echo "deb http://dl.bintray.com/geldtech/debian /" |  tee -a /etc/apt/sources.list.d/geld-tech.list ; \
		apt-key adv --recv-keys --keyserver keyserver.ubuntu.com EA3E6BAEB37CF5E4 ; \
		apt clean all ; \
		apt update ; \
		apt install -y nginx-monitor-dashboard ; \
		wget https://raw.githubusercontent.com/geld-tech/nginx-monitor-dashboard/master/stub/nginx-status-stub.py ; \
		/usr/bin/python nginx-status-stub.py & \
		systemctl status nginx-monitor-dashboard ; \
		systemctl status nginx-monitor-dashboard-collector ; \
		touch $(PACKAGE_DIR)/config/settings.cfg.dev ; \
		echo "[admin]" >> $(PACKAGE_DIR)/config/settings.cfg.dev ; \
		echo "password = Y25mZmpiZXExMjM=" >> $(PACKAGE_DIR)/config/settings.cfg.dev ; \
		echo "" >> $(PACKAGE_DIR)/config/settings.cfg.dev ; \
		echo "[ganalytics]" >> $(PACKAGE_DIR)/config/settings.cfg.dev ; \
		echo "ua_id = 1234567" >> $(PACKAGE_DIR)/config/settings.cfg.dev ; \
		cp -f $(PACKAGE_DIR)/config/settings.cfg.dev $(PACKAGE_DIR)/config/settings.cfg ; \
		systemctl start nginx-monitor-dashboard ; \
		systemctl status nginx-monitor-dashboard ; \
		systemctl status nginx-monitor-dashboard-collector ; \
		$$SHELL '

## Validate latest .rpm package on a local CentOS image with Docker
docker-run-rpm:
	$(call echo_title, "DOCKER RUN RPM")
	sudo docker run -i -t -p $(PORT):8004 --rm centos:7 /bin/bash -c ' yum clean all ; \
		yum install -y python wget vim ; \
		yum install -y epel-release ; \
		wget https://raw.githubusercontent.com/gdraheim/docker-systemctl-replacement/master/files/docker/systemctl.py ; \
		cp /usr/bin/systemctl /usr/bin/systemctl.bak ; \
		yes | cp -f systemctl.py /usr/bin/systemctl ; \
		chmod a+x /usr/bin/systemctl ; \
		test -L /bin/systemctl || ln -sf /usr/bin/systemctl /bin/systemctl ; \
		useradd -MU www-data && usermod -L www-data ; \
		echo -e "[geld.tech]\nname=geld.tech\nbaseurl=http://dl.bintray.com/geldtech/rpm\ngpgcheck=0\nrepo_gpgcheck=0\nenabled=1" | \
			tee -a /etc/yum.repos.d/geld.tech.repo ; \
		yum install -y nginx-monitor-dashboard ; \
		wget https://raw.githubusercontent.com/geld-tech/nginx-monitor-dashboard/master/stub/nginx-status-stub.py ; \
		/usr/bin/python nginx-status-stub.py & \
		systemctl status nginx-monitor-dashboard ; \
		systemctl status nginx-monitor-dashboard-collector ; \
		touch $(PACKAGE_DIR)/config/settings.cfg.dev ; \
		echo "[admin]" >> $(PACKAGE_DIR)/config/settings.cfg.dev ; \
		echo "password = Y25mZmpiZXExMjM=" >> $(PACKAGE_DIR)/config/settings.cfg.dev ; \
		echo "" >> $(PACKAGE_DIR)/config/settings.cfg.dev ; \
		echo "[ganalytics]" >> $(PACKAGE_DIR)/config/settings.cfg.dev ; \
		echo "ua_id = 1234567" >> $(PACKAGE_DIR)/config/settings.cfg.dev ; \
		cp -f $(PACKAGE_DIR)/config/settings.cfg.dev $(PACKAGE_DIR)/config/settings.cfg ; \
		systemctl start nginx-monitor-dashboard ; \
		systemctl status nginx-monitor-dashboard ; \
		systemctl status nginx-monitor-dashboard-collector ; \
		$$SHELL '


# PHONYs
.PHONY: clean isort lint test local-dev-env
.PHONY: vue-dev-tools npm-install npm-lint npm-audit npm-build
.PHONY: webapp-setup webapp-settings webapp-config
.PHONY: webapp-start webapp-stop
.PHONY: daemon-start daemon-stop
.PHONY: nginx-status-start nginx-status-stop
.PHONY: start stop


# Functions
define echo_title
	@echo ""
	@echo ""
	@echo "$$(tput bold)### $(1) ###$$(tput sgr0)"
	@echo ""
endef


# Self-documentated makefile (DO NOT EDIT PAST THIS LINE)
.DEFAULT_GOAL := show-help
.PHONY: show-help
show-help:
	@echo "$$(tput bold)Available rules:$$(tput sgr0)"
	@echo
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| LC_ALL='C' sort --ignore-case \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=19 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}' \
	| more $(shell test $(shell uname) == Darwin && echo '--no-init --raw-control-chars')
