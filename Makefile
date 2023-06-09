install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt &&\
			apt-get update && \
				apt-get install -y portaudio19-dev && \
					pip install pyaudio &&\
						apt-get install -y espeak && \
							apt-get install -y flac






test:
	python -m pytest -vv --cov=main --cov=mylib test_*.py

format:	
	black *.py 

lint:
	pylint --disable=R,C --ignore-patterns=test_.*?py *.py mylib/*.py

container-lint:
	docker run --rm -i hadolint/hadolint < Dockerfile

refactor: format lint

deploy:
	#deploy goes here
		
all: install lint test format deploy
