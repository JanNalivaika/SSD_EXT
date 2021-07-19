
echo Attention - EXPECTED RUNNING TIME is 24 hours

echo start
copy .\binvox.exe .\stls\
cd stls
del *.binvox
pause
for %%f in (*.stl) do binvox.exe -d 64 %%f
pause
