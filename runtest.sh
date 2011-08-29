DIR=`dirname $0`
cd $DIR
nosetests -s --with-coverage --cover-package=dict_update_watcher -x
