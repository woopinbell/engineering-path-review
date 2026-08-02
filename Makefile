.PHONY: build jobs graphs check test package clean

build: jobs graphs

jobs:
	python3 -B scripts/build_jobs.py

graphs:
	bash scripts/render_graphs.sh

check:
	python3 -B scripts/build_jobs.py --check
	python3 -B scripts/check_repo.py
	python3 -B -m unittest discover -s tests -p "test_*.py"

test:
	python3 -B -m unittest discover -s tests -p "test_*.py"

package: build
	python3 -B scripts/package_release.py

clean:
	rm -rf scripts/__pycache__ dist
