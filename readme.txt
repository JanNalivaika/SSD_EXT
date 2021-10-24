
History (newest on top)

24.10.21
to fix error:  model = binvox_rw.read_as_3d_array(f).data
got error on github:
 ./Scripts/SSD/data/voc0712.py:236:21: F821 undefined name 'utils'
 model = utils.binvox_rw.read_as_3d_array(f).data
commit/push weights into repo
get it compilable - it works!
replace import layer by import .layer (relative import)
compile error in ssd.py - 'layer not found'
update ssd.py from dev-branch
got error "blabla depricated"