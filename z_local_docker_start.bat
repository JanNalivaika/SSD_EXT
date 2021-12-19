
set image=local_ssd_image
set container=ctn_local_ssd

docker rm --force %container%

docker run --name %container% -dp 80:80 %image% python -m flask run --host=0.0.0.0 --port=80

@echo off

REM docker run --name %container% -dp 5000:5000 local_ssd_image python -m flask run --host=0.0.0.0 
REM docker run --name %container% -dp   80:80   local_ssd_image python -m flask run --host=0.0.0.0 --port=80
REM docker run --name %container% -dp 5000:5000 local_ssd_image

@echo off


pause