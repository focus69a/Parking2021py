korzystam ze srodowiska conda activate flask
do srodowiska flask dointalowujemy moduly konieczne jak
    flask
    requests



//stworzylem plik requirements.txt ktory moze byc uzyty do stworzenie srodowiska 'flask' z zaleznosciami
    conda list -e > requirements.txt

odtworzenie srodowiska flask to:
    conda create --name <env> --file requirements.txt


If you want a file which you can use to create a pip virtual environment (i.e. a requirements.txt in the right format)
 you can install pip within the conda environment, the use pip to create requirements.txt
zeby zrobic plik requirements dla pip to trzeba zrobic to tak:
    conda activate <env>
    conda install pip
    pip freeze > requirements_p.txt

Then use the resulting requirements_p.txt to create a pip virtual environment:

    python3 -m venv env
    source env/bin/activate
    pip install -r requirement_p.txt