run:
	npm run build
	mv dist/index.html static/index.html
	rm -r static/static
	mv dist/static static/