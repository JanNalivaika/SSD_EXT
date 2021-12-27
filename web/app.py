import os
from flask import Flask, render_template, request
import validate
import glob
import shutil


app = Flask(__name__, template_folder='templates', static_url_path="/web/static", static_folder='static')


@app.route('/')
def hello_world():
    ret = """
    <h2> v.0.5.0 is running ... </h2>
    <br><br><br>
    <img src='web/static/docker_001.png'/>
    """

    cwd = os.getcwd()
    
    ret += "<br>" + cwd

    items = [ret]
    return render_template('home.html', items=items)


@app.route('/debug')
def debug():
    ret = "..."
    items = [ret]
    return render_template('debug.html', items=items)


@app.route('/validate')
def run_validate():
    #
    ret = ""
    try:
        ret += run_validate_internal()
    except BaseException as err:
        ret += """
        <h1>Error</h1>
        """
        print(f"Unexpected error: {err=}, {type(err)=}")
        ret += str(err)

    items = [ret]
    return render_template('validate.html', items=items)



def run_validate_internal():
    #
    log = validate.run()
    ret = """
    <h1>OK</h1>
    """

    folder_res = 'data/MulSet/set20'  # TODO magic string, managed outside of this func
    folder_static = 'web/static/generated'
    pattern = "*.png"

    if not os.path.exists(folder_static):
        os.makedirs(folder_static)

    if not os.path.exists(folder_static):
        ret += "<br> folder NOT available" + folder_static

    validate.remove_files(folder_static, pattern)

    files = glob.glob(folder_res + '/' + pattern)
    for f in files:
        shutil.copy(f, folder_static)

    print("Copy done")

    files = glob.glob(folder_static + '/' + pattern)
    sorted_files = sorted(files)

    ret += "<div style='display:flex'>"
    for f in sorted_files:
        ret += "<div style='margin-left:5px;margin-left:5px'>"
        temp = os.path.basename(f)
        ret += "<img src='" + folder_static + "/" + temp + "' width='200' height='200'/>"
        ret += "<div style='margin-left:15px;'>" + temp + "</div>"
        ret += "</div>"
    ret += "</div>"

    ret += "<div>" + log + "</div>"

    return ret


@app.route('/upload')
def upload_file():
    ret = render_template('upload.html')
    return ret


@app.route('/uploader', methods=['GET', 'POST'])
def uploader():
    if request.method == 'POST':
        file_storage = request.files['file']
        file_storage.save('web/' + file_storage.filename)
        return 'file uploaded successfully'

if __name__ == "__main__":
    app.run(host='0.0.0.0')
