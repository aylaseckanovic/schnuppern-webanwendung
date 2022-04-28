.PHONY: all clean

all: grades.db webanwendung.pdf webanwendung.html

grades.db: tables.sql insert_test_data.py
	rm -f grades.db
	sqlite3 grades.db <tables.sql
	python3 insert_test_data.py

webanwendung.pdf: webanwendung.md
	pandoc -t ms $^ -o $@

webanwendung.html: webanwendung.md
	pandoc -s -t html5 --toc $^ -o $@

clean:
	rm -f grades.db
	rm -f webanwendung.pdf
	rm -f webanwendung.html
