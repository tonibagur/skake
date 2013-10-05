rm ./.coverage
rm -rf tests/cover
#nosetests -w tests/ --with-coverage --cover-html --pdb --pdb-failures
nosetests -w tests/ --with-coverage --cover-html

