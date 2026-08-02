.PHONY: jobs check clean

jobs:
	python3 scripts/build_jobs.py

check:
	python3 scripts/check_repo.py

clean:
	rm -rf scripts/__pycache__
