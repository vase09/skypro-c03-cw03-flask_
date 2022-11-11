## entrypoint.sh
python3.10 data_scripts/create_tables.py
python3.10 data_scripts/load_fixtures.py
flask run -h 0.0.0.0 -p 5000
