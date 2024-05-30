from flask import Flask, redirect, url_for, render_template, request
from pymongo import MongoClient
import os
from bson import ObjectId
from dotenv import load_dotenv
from os.path import join, dirname

app=Flask(__name__)
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME = os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

@app.route('/',methods=['GET'])
def home():
    orang = list(db.user.find({}))
    return render_template('home.html', orang = orang)

@app.route('/addData',methods=['POST'])
def addData():
    telepon = request.form['telepon']
    nama = request.form['nama']
    Laptop = request.form['laptop']

    doc = {
        'Telepon': telepon,
        'nama': nama,
        'Laptop': Laptop
    }

    db.user.insert_one(doc)
    return redirect(url_for('home'))

@app.route('/edit/<_id>',methods=['POST', 'GET'])
def editData(_id):
    if request.method == 'POST':
        id = request.form['_id']
        telepon = request.form['telepon']
        nama = request.form['nama']
        Laptop = request.form['laptop']

        doc = {
        'Telepon': telepon,
        'nama': nama,
        'Laptop': Laptop
        }

        db.user.update_one({"_id": ObjectId(_id)}, {"$set":doc})
        return redirect(url_for('home'))
    id = ObjectId(_id)
    data = list(db.user.find({"_id":id}))
    return render_template('edit.html', data=data)

@app.route('/delete/<_id>',methods=['GET'])
def delete(_id):
    db.user.delete_one({"_id": ObjectId(_id)})
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run('0.0.0.0',port=4000,debug=True)