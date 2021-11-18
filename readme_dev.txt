
TODO
1. re-create str.rar
2. by generating of PNGs create a file with mapping binvox -- png
3. prep and describe show-cases
4. done -- vn- docker container
5. vn- unit tests
6. done --vn- web hosting for showcases

Info
pip3 install -r requirements.txt
python.exe -m pip install --upgrade pip

Unit-Tests
 https://docs.pytest.org/
 https://docs.python.org/3/library/unittest.html

# History (newest on top)
17.11.21
merge into main (v.0.4.0)
fix run-time errors
adapt version to v.0.4.0
merge into main (v.0.3.0)

14.11.21
simplify - remove folder 'temp'
solve issue with creating of voc.pth. Just splitt voc.pth by using splitt_files(),
than commit the parts, and finaly merge the parts into voc.pth

30.10.21
add unit_tests/__init__.py  and than run command --  pytest unit_tests
try to get tests running -- https://stackoverflow.com/questions/11452299/import-parent-directory-for-brief-tests
add folder unit_tests
remove unused files

11.08.21
add achieve_legal_model_simple

30.07.21
python.exe -m pip install --upgrade pip
add requirements.txt

29.07.21
add folder misc

23.07.21
store generated binvox and txt which contains the info which binvox are combined

18.07.21
create folder data/STL
create folders weights, weights/base
tyr to run create_tr_set.py


17.07.21
create folders  data/TrSet, data/ValSet, data/FNSet
init clone from https://github.com/PeizhiShi/SsdNet.git