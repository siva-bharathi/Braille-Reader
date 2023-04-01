# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, flash
from werkzeug.utils import secure_filename
from flask import render_template
from flask import request
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
import os

# a file named "geek", will be opened with the reading mode.


               

UPLOAD_FOLDER = 'static/uploads/'
app = Flask(__name__)
app.secret_key = "Secret Key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

allext = set(['txt'])

def allfile(filename):
	return '.' in filename and filename.rsplit('.',1)[1].lower() in allext

@app.route('/')
@app.route('/home')
@app.route('/index')
def home():
	return render_template('index.html')

@app.route('/upload')
def upload():
	return render_template('upload.html',message='')

@app.route('/download', methods = ['POST'])
def register():
	file = request.files['file']
	filename = 'normalbook.txt'
	file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
	
	cfile = open('static/uploads/normalbook.txt', 'r')
	cfile1 = open('braillebook.txt','w')
	normal_char = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z', 'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z' ,'1','2','3','4','5','6','7','8','9','0','.',',','\'',';',':','-','?','!','&','@','$','(',')']
	braille_char = ['100000','100100','110000','110100','100100','111000','111100','101100','011000','011100','100010','101010','110010','110110','100110','111010','111110','101110','011010','011110','100011','101011','011101','110011','110111','100111','100000','100100','110000','110100','100100','111000','111100','101100','011000','011100','100010','101010','110010','110110','100110','111010','111110','101110','011010','011110','100011','101011','011101','110011','110111','100111','010111100000','010111101000','010111110000','01011110100','010111010100','010111111000','010111111100','010111101100','010111011000','010111011100','001101','001000','000010','001010','001100','000011','001011','001110','010000111011','010000100000','010000110000','010000101001','000100010110']
	cdata = cfile.readlines()
	for line in cdata:
		wordList = line.split()
		if len(wordList)==0:
			print("")
		else:
			for word in wordList:
				for char in word:
					if char in normal_char:
						# find and print conversion
						pos = normal_char.index(char)
						# //print(braille_char[pos])
						cfile1.write(braille_char[pos])
					else:
						continue
				print(word)
				cfile1.write('000000')
	cfile.close()
	cfile1.close()
		
	cfile = open('braillebook.txt', 'r')
	cfile1 = open('braille8bit.txt','w')
	data = str(cfile.readlines())
	data = data.replace("['",'')
	data = data.replace("']",'')
	print(len(data))
	word8 = []
	for i in range(0,len(data)):
		if len(word8) !=8:
			word8.append(data[i])
		else :
			w="".join(word8)
			print(w)
			cfile1.write(w+"\n")
			word8.clear()

	w="".join(word8)
	print(w)
	cfile1.write(w+"\n")
	iter = 0
	numdig = 0
	cfile = open('braille8bit.txt', 'r')
	cfile1 = open('static/uploads/converted.txt','w')
	data = cfile.readlines()
	print()
	equv = [1,2,4,8,16,32,64,128]

	for i in range(0,len(data)):
		wordwithoutn = data[i].rstrip()
		for j in wordwithoutn:
			numdig = numdig + int(j)*equv[iter]
			iter = iter+1
		cfile1.write(str(numdig)+"\n")
		numdig=0
		iter = 0
    
	return render_template('download.html',message='')

app.run(debug = True)

