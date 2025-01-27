# Assignments

## Download the codes

```
git clone https://github.com/AlaFalaki/assignments.git
```

## How to run?

*The projects are implemented using Python version 3.11.5.*

1. Create a virtual environment and activate it:

```
cd assignments
python -m venv .venv
source .venv/bin/activate

# For Windows:
# myenv\Scripts\activate
```

2. Install the required packages: (Pydantic + PyTest)

```
pip install -r requirements.txt
```

3. A. Run assignment 1:

```
cd assignment-01
python run.py

# Or, test:
# pytest tests/test.py -v
```

3. B. Run assignment 2:

```
cd assignment-02
python run.py

# Or, test:
# pytest tests/test.py -v

```

## Logging

Both projects by default show the `INFO` level logs by running the `run.py` scripts. If you like to get more details, change the logging level to `logging.DEBUG` or comment out the `logging.basicConfig` line from the script.
