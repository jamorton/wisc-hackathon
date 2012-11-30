#!/bin/sh
rm -f hackpack.db
python -c "import main; main.create_tables()"
