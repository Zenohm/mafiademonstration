.PHONY: docs po mo

help:
	@echo "test - run the test py.test suite"
	@echo "coverage - generate a coverage report and open it"
	@echo "docs - generate Sphinx HTML documentation and open it"
	@echo "apk - build an android apk with buildozer"
	@echo "deploy - deploy the app to your android device"
	@echo "clean - remove unneeded build files before git push"

test:
	python setup.py test

coverage:
	python setup.py test -a '--cov=mafiademonstration --cov-report=html'
	xdg-open htmlcov/index.html

docs:
	$(MAKE) -C docs html
	xdg-open docs/build/html/index.html

apk:
	buildozer -v android debug

deploy:
	buildozer android deploy logcat

clean:
	rm -rf .cache
	rm -rf mafiademonstration.egg-info
	rm -rf mafiademonstration/__pycache__
	rm -rf tests/__pycache__
