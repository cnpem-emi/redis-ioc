run: 
	curl -o "spreadsheet/Redes e Beaglebones.xlsx" https://gitlab.cnpem.br/IoT/redis-ioc/raw/master/scripts/spreadsheet/Redes%20e%20Beaglebones.xlsx
	python3 ./generate.py
	python3 ./simar.py
	bash -c 'set -x; set -e; source functions; run'