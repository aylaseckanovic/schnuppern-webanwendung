.PHONY: all clean

all: grades.db webanwendung.pdf

grades.db: tables.sql insert_test_data.py
	rm -f grades.db
	sqlite3 grades.db <tables.sql
	python insert_test_data.py

webanwendung.pdf: webanwendung.md
	pandoc -t ms $^ -o $@

clean:
	rm -f grades.db
	rm -f webanwendung.pdf
