from python:3

workdir /opt/src/
add ./requirements.txt /opt/src/
run pip install -r requirements.txt
add ./ /opt/src/

run ln -sf /opt/src/ /opt/game

workdir /opt/game/
entrypoint [ "./app.py" ]

