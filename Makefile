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
	@echo 'Purging CDN endpoint'
	az cdn endpoint purge --ids /subscriptions/86dc3cdb-5ddb-43db-baee-6b86576c3ef6/resourcegroups/Marketing/providers/Microsoft.Cdn/profiles/AttcStaticWebsiteCDN/endpoints/attc-static-website-cdn --content-paths '/*'
	@echo 'Deploying email trigger function app to azure'
	cd azure_function_apps/ContactFormHttpTrigger && func azure functionapp publish attc-website-email-trigger --build remote

install:
	bundle install
	cd azure_function_apps/ContactFormHttpTrigger && poetry install;
	cd azure_function_apps/ContactFormHttpTrigger && poetry export --without-hashes -o requirements.txt

build: clean install
	JEKYLL_ENV=production bundle exec jekyll build

dev:
	make -j 4 dev-jekyll-server dev-azurite-server dev-contact-form-http-trigger dev-mail-server

test: install
	cd azure_function_apps/ContactFormHttpTrigger && poetry run python -m unittest discover

clean:
	rm -rf ./_site
	cd azure_function_apps/ContactFormHttpTrigger && rm -rf log __pycache__ .python_packages

# Secondary targets

azure-login: guard-AZURE_SERVICE_PRINCIPAL_USERNAME guard-AZURE_SERVICE_PRINCIPAL_PASSWORD guard-AZURE_SERVICE_PRINCIPAL_TENANT
	@echo 'Logging into azure with service principal...'
	@az login --service-principal --username $(AZURE_SERVICE_PRINCIPAL_USERNAME) --password=$(AZURE_SERVICE_PRINCIPAL_PASSWORD) --tenant $(AZURE_SERVICE_PRINCIPAL_TENANT)

dev-jekyll-server: build
	@echo 'Running Jekyll in environment: $(JEKYLL_ENV)'
	bundle exec jekyll serve --livereload --open-url --port 4001 --livereload-port 35730

dev-azurite-server: install
	cd azure_function_apps/ContactFormHttpTrigger && azurite --silent --location /tmp/azurite --debug log/azurite_debug.log

dev-contact-form-http-trigger: install
	cd azure_function_apps/ContactFormHttpTrigger && poetry run func start --port 7071

dev-mail-server:
	npx maildev --smtp 1025 --open

# Guard to fail the make target if the specified env variable doesn't exist
# https://lithic.tech/blog/2020-05/makefile-wildcards
guard-%:
	@if [ -z '${${*}}' ]; then echo 'ERROR: variable $* not set' && exit 1; fi
