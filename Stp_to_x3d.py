# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 14:11:59 2020

@author: DELL
"""
from urllib import request

from OCC.Display.WebGl import x3dom_renderer
from OCC.Core.BRep import BRep_Builder
from OCC.Core.TopoDS import TopoDS_Shape
from OCC.Core.BRepTools import breptools_Read
from OCC.Extend.DataExchange import read_step_file


from OCC.Display.SimpleGui import init_display
from OCC.Core.TopoDS import topods_Edge
from OCC.Extend.DataExchange import read_step_file
from OCC.Extend.TopologyUtils import TopologyExplorer
from OCC.Display.OCCViewer import rgb_color
from OCC.Core.AIS import AIS_ColoredShape
from random import random
from OCC.Core.AIS import AIS_Shape
from OCC.Core.Bnd import Bnd_Box
from OCC.Core.BRepBndLib import brepbndlib_Add
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder
from OCC.Core.BRepMesh import BRepMesh_IncrementalMesh
from OCC.Core.Quantity import Quantity_Color
from OCC.Core.Quantity import Quantity_Color,Quantity_TOC_RGB
from OCC.Display.SimpleGui import init_display
from OCC.Display.OCCViewer import Viewer3d
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
import os
import socket
import webbrowser
import errno
from flask import Flask, redirect, url_for, request
from flask import Flask, render_template
from werkzeug.utils import secure_filename

num_click=0

def get_available_port(port):
    """ sometimes, the python webserver is closed but the
    port is not made available for a further call. So let's find
    any available port to prevent such issue. This function:
    * takes a port number (an integer), above 1024
    * check if it is available
    * if not, take another one
    * returns the port numer
    """
    if not port > 1024:
        raise AssertionError("port number should be > 1024")
    # check this port is available
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(("127.0.0.1", port))
    except socket.error as e:
        if e.errno == errno.EADDRINUSE:
            print("\nPort %i is already in use. Picking another one." % port)
            # take another one
            s.bind(("", 0))
            port = s.getsockname()[1]
            print("Using port number %i" % port)
        else:
            print("Can't bind to port %i." % port)
    s.close()
    return port
def Exchange_stp_3xd(file="aaa.stp",path="."):
    pass
    file=file
    global num_click
    num_click+=1
    try:
        os.mkdir(str(num_click))
    except:
        pass
    the_shape = read_step_file(file)
    path=str(num_click)
    my_renderer = x3dom_renderer.X3DomRenderer(path=path)
    my_renderer.DisplayShape(the_shape,export_edges=True,color=(random(), random(), random()))
    my_renderer.run()
    return file



from flask import Flask

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'upload/'

@app.route('/')
def index():
    result=Exchange_stp_3xd()
    fp = open(os.path.join("1", 'index.html'))
    html_content = fp.read()
    fp.close()
    return html_content
 

@app.route('/upload')
def upload_file():
   return render_template('upload.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def uploader():
   if request.method == 'POST':
      f = request.files['file']
      f.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(f.filename)))
      print(f.filename)
      path=".\\upload"+"\\"+f.filename
      result=Exchange_stp_3xd(file=path)
      return 'file uploaded successfully'



if __name__ == '__main__':
    app.run("172.16.18.104",5050,threaded=True)