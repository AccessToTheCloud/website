# Check if a .env file exists, and then load it
ifneq (,$(wildcard ./.env))
    include .env
    export
endif

# Primary targets

deploy: guard-AZURE_ACCOUNT_NAME build azure-login
	$(eval NOW=$(shell date -u '+%FT%TZ'))
	# Upload to azure all the files in the _site build folder
	@echo 'Time is $(NOW)'
	az storage blob upload-batch --auth-mode login --source ./_site --destination '$$web' --account-name $(AZURE_ACCOUNT_NAME) --overwrite
	# Remove any dangling files that may be left over in azure
	# i.e any files that didn't get touched during this deployment
	@echo 'Removing all files that are unmodified since $(NOW)'
	az storage blob delete-batch --auth-mode login --source '$$web' --account-name $(AZURE_ACCOUNT_NAME) --if-unmodified-since '$(NOW)'

install:
	bundle install
	cd azure_function_apps/ContactFormHttpTrigger; poetry install;

build: clean install
	bundle exec jekyll build

dev:
	make -j 3 dev-jekyll-server dev-azurite-server dev-contact-form-http-trigger

test: install
	cd azure_function_apps/ContactFormHttpTrigger && poetry run python -m unittest discover

clean:
	rm -rf ./_site

# Secondary targets

azure-login: guard-AZURE_SERVICE_PRINCIPAL_USERNAME guard-AZURE_SERVICE_PRINCIPAL_PASSWORD guard-AZURE_SERVICE_PRINCIPAL_TENANT
	@echo 'Logging into azure with service principal...'
	@az login --service-principal --username $(AZURE_SERVICE_PRINCIPAL_USERNAME) --password=$(AZURE_SERVICE_PRINCIPAL_PASSWORD) --tenant $(AZURE_SERVICE_PRINCIPAL_TENANT)

dev-jekyll-server: build
	bundle exec jekyll serve --livereload --open-url --port 4001 --livereload-port 35730

dev-azurite-server: install
	cd azure_function_apps/ContactFormHttpTrigger && azurite --silent --location /tmp/azurite --debug log/azurite_debug.log

dev-contact-form-http-trigger: install
	cd azure_function_apps/ContactFormHttpTrigger && poetry run func start

# Guard to fail the make target if the specified env variable doesn't exist
# https://lithic.tech/blog/2020-05/makefile-wildcards
guard-%:
	@if [ -z '${${*}}' ]; then echo 'ERROR: variable $* not set' && exit 1; fi
