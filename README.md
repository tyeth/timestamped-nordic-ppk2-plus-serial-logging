# timestamped-nordic-ppk2-plus-serial-logging
timestamped-nordic-ppk2-plus-serial-logging

Ensure you have the required libraries installed:

```sh
pip install pynrfjprog serial
```

specify voltage for device under test, and optionally com port (com3 by default)
`ppk2_logger_with_announce 3.3`
or
`python ppk2_logger_with_announce.py 3.3 COM4`
