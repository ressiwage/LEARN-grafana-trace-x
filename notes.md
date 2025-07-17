https://grafana.com/docs/grafana/latest/setup-grafana/installation/debian/

sudo apt-get install sqlite3

https://grafana.com/grafana/plugins/frser-sqlite-datasource/

sqlite3 main.db
CREATE TABLE maintable(id INTEGER PRIMARY KEY, success INTEGER, message TEXT, timestamp TEXT);
mv main.db /home/grafana/main.db