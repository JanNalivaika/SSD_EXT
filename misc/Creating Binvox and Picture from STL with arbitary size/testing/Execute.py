import time
t1 = time.time()
exec(open("testing.py").read())
exec(open("Bar_Remover.py").read())
exec(open("combiner.py").read())
exec(open("../PNGfromArray.py").read())
print(time.time() - t1)

# 100 = 5s
# 500 = 400s
# 1000 = 3_200s
# 2000 = 16_000s
# 3100 = 46_000s