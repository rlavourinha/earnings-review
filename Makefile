.PHONY: build serve publish clean

build:
	python build.py

serve: build
	python -m http.server 8780 --bind 127.0.0.1 --directory output

# Regenera o HTML publicado (GitHub Pages serve docs/ na branch main).
# Depois: git add docs/index.html && git commit && git push.
publish: build
	cp output/earnings_review.html docs/index.html

clean:
	rm -rf output __pycache__
