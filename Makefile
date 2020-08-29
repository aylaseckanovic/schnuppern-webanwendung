.PHONY: clean

grades.db: tables.sql insert_test_data.py
	rm -f grades.db
	sqlite3 grades.db <tables.sql
	python insert_test_data.py

clean:
	rm -f grades.db
