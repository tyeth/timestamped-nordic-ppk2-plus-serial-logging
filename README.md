# timestamped-nordic-ppk2-plus-serial-logging
timestamped-nordic-ppk2-plus-serial-logging

Stores timestamped PPK2 and Serial data in timestamped log files

Ensure you have the required libraries installed:

```sh
pip install pynrfjprog serial pyserial
```

specify voltage for device under test, and optionally com port (finds first using pyserial by default)
```sh
ppk2_logger_with_announce 3.3
```
or
```sh
python ppk2_logger_with_announce.py 3.3 COM4
```
