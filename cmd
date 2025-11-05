#python3 -m venv venv

source venv/bin/activate
venv\Scripts\Activate.ps1
venv\Scripts\activate.bat

python -m pip install --upgrade pip

pip install numpy matplotlib scikit-learn
pip install tensorflow


pip install gymnasium[atari,accept-rom-license]
pip install "gymnasium[classic-control]"
pip install ale-py

pip install gym[atari]

pip freeze > requirements.txt
pip install -r requirements.txt

pip list
