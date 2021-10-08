
echo Attention - EXPECTED RUNNING TIME is x hours

echo start
copy .\binvox.exe .\stls_medium\
cd stls_medium
del *.binvox
pause
for %%f in (*.stl) do binvox.exe -d 64 %%f
pause
