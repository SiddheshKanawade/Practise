build:
	pip install -e .

run:
	python -m uvicorn src.main:app --reload