DIR=`dirname $0`
cd $DIR
pytest --capture=tee-sys --tb=short --cov=dict_update_watcher --cov-report=term-missing "${@:1}"
