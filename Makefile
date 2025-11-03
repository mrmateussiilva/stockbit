.PHONY: test test-coverage test-watch help

help:
	@echo "Comandos disponíveis:"
	@echo "  make test              - Executa todos os testes"
	@echo "  make test-coverage     - Executa testes com cobertura"
	@echo "  make test-integration  - Executa apenas testes de integração"
	@echo "  make test-models       - Executa apenas testes de modelos"
	@echo "  make test-views        - Executa apenas testes de views"
	@echo "  make test-forms        - Executa apenas testes de formulários"

test:
	python manage.py test

test-coverage:
	coverage run --source='.' manage.py test estoque
	coverage report
	coverage html
	@echo "\nRelatório HTML gerado em: htmlcov/index.html"

test-integration:
	python manage.py test estoque.tests.test_integration

test-models:
	python manage.py test estoque.tests.test_models

test-views:
	python manage.py test estoque.tests.test_views

test-forms:
	python manage.py test estoque.tests.test_forms

test-verbose:
	python manage.py test --verbosity=2

test-failed:
	python manage.py test --failed

