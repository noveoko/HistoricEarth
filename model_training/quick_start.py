from os import system
from os.path import exists


def clone_repo():
    system("git clone https://github.com/taesungp/contrastive-unpaired-translation.git CUT")

def install_requirementes():
    requirements = [
    "cd CUT",
    "pip install -r CUT/requirements.txt"
    ]

    for r in requirements:
        system(r)

script = 'python CUT/train.py'
        
def perform_training(learning_rate=0.0001,number_of_epochs=200, training_data='map_to_image/'):
    if exists(training_data):
        SCRIPT = f"{script} --dataroot {training_data} --name map_to_photo_CUT --CUT_mode CUT --n_epochs {number_of_epochs} --lr {learning_rate}"
        system(SCRIPT)
        

#clone_repo()
#install_requirementes()
perform_training()
