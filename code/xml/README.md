## XML

This folder contains the Python program and scripts required to generate XML files for the PhiloLogic database.

## Folder Structure

- **\_input**: Input files (more on this later)
- **\_output**: Output `.xml` files
- **code**: Source code for Python program
- **scripts**: Shell scripts to streamline running the program

## Required Input Files

`_input` folder should have the following directory structure.

- `_input`
  - `metadata`: .csv file containing metadata of all entries
  - `notes`: .txt notes (e.g. `0002_Trier_1277_Notes.txt`)
  - `text`: .txt files (e.g. `0002_Trier_1277.txt`)

## Processing input files

The following bash scrips might be useful.

- Remove all files that contains `_Notes`
	- `rm -rf *_Notes*`
- Remove all files that do NOT contain `_Notes`
	- `shopt -s extglob`
	- `rm -rf !(*_Notes*)`

Make sure to have a **backup** of all text files before deleting them.

## Virtual Environment

To make the Python program run consistently on all platforms, I use a [virtual environment](https://docs.python.org/3/tutorial/venv.html) with Python 3.7.0.

- To create the virtual environment:

```
python3 -m venv ~/.ve/ll-python3.7
```

- To use the virtual environment:

```
source ~/.ve/ll-python3.7/bin/activate
```

- To deactivate the virtual environment:

```
deactivate
```

## Running the program

- Go to `xml` folder.

```
cd xml
```

- Activate virtual environment.

```
source scripts/ve.sh
```

- To run normal version:

```
source scripts/run.sh
```

- To run normalized version:

```
source scripts/normalize.sh
```

- Here is a screenshot of the program:

![Imgur](https://i.imgur.com/G3fxbAh.png)
