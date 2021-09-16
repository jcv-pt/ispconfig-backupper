# ISPConfig - Backupper

Backupper is a Python library to backup ISPConfig client data to remote web storage

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install Backupper required libs.

```bash
pip install -r requirements.txt
```

Copy & edit the config smaple file located at:

```
cp data/config/sample.default.ini data/config/default.ini
```

## Usage

Backupper can be runned with:

```sh
python backupper
```

Available arguments:

| Flag       | Description                                    | Accepted Values |
| ---------- | ---------------------------------------------- | --------------- |
| -h, --help | Shows help screen with all available arguments | --              |
| --verbose  | Weather to show system.out                     | 0,1             |

## License

[MIT](https://choosealicense.com/licenses/mit/)