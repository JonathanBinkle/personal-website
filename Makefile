# Redirect commands to ./docker/Makefile. Keep this one just for convinience.
%:
	@touch ./docker/.env.dev ./docker/.env.prod
	@sed -i '/^WWW_ROOT_HOST/d' ./docker/.env.dev ./docker/.env.prod
	@echo "WWW_ROOT_HOST='$(shell pwd)/portfolio'" >> ./docker/.env.dev
	@echo "WWW_ROOT_HOST='$(shell pwd)/portfolio'" >> ./docker/.env.prod
	@$(MAKE) -C ./docker $@
