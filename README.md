# githupdate.py

`githupdate.py` is a Python script designed to help users update their softwares easily from github.

## Features

- **Update easily** You can specify the program is what version at, it looks into the github repo, and

## Usage

Example showcase:

```python
import githupdate as ghp

updater = ghp.githupdate("Repo Owner", "Repo Name") # You can specify what file extension file should it download (fext=".zip") and where should it download the temporary update file (download_path=os.path.dirname(__file__)+'\\GHP\\') [these are their default values]
updater.update("1.0.0") #Current version number
```
