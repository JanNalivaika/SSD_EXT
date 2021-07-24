import z_import_a
from z_import_b import *

print("I am in check_import")

def check_foo_empty() :
    print("foo_empty")

def check_foo() :
    print("start  -- foo in check")
    z_import_a.foo_a()
    foo_b()
    print("end   -- foo in check")

if __name__ == '__main__':
    check_foo_empty()