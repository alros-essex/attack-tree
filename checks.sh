# run bandit
pip3 install bandit
bandit --ini .bandit -r > bandit.txt

# run pylint
pip3 install pylint
#pylint --rcfile=pylintrc attack > reports/pylint.txt
pylint *.py > pylint.txt