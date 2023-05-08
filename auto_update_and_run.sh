#! bin/bash

echo "Pulling most recent changes from repo"
git pull

echo "Activating venv"
source jobsworth/bin/activate

echo "Ensuring requirements installed"
pip install -r requirements.txt

echo -e "\nStarting up job"
echo -e "\n-~- -~- -~- -~- -~- -~- -~- -~- -~- -~-\n"
python3 main.py --headless-operation  # headless operation must be set for cronjob to execute
echo -e "\n-~- -~- -~- -~- -~- -~- -~- -~- -~- -~-\n"

echo "Job exited with status: $?"
echo "Deactivating venv"
deactivate
echo "Finished."
