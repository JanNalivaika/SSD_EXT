echo start
pause
del *.binvox
for %%f in (*.stl) do binvox.exe -d 64 %%f
pause
