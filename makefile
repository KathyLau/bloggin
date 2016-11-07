make: app.py
	#not much

run: make
	python app.py

clean:
	rm -rf *~
	rm -f data/*
