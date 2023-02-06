
from flask import Flask, request, render_template, make_response,redirect, session, jsonify, Response
import json, time
from datetime import timedelta
import numpy as np
from unidecode import unidecode
from re import sub

app = Flask(__name__)



with open("".join(['./static/novel-time.json']), "r", encoding= 'utf-8') as f:
  datanoveljson = json.load(f)

datanoveltimereversejson = datanoveljson[::-1]

datanovelnamejson = sorted(datanoveljson, key=lambda x: x['name'])

datanovelnamereversejson = datanovelnamejson[::-1]

webpage = 49

class tool:
    class minitool:
        def while_replace(string:str):
            string = "".join(string.splitlines())
            while '  ' in string:
                string = string.replace('  ', ' ')
            string = sub(r"[\n\t]*", "", string)
            return string
        def removeSymbols(string) -> str:
            st1 = tool.minitool.while_replace(str((unidecode(str(string))).strip()
            .replace('<', '(').replace('>', ')').replace('[', '(').replace('\\', '')
            .replace(']', ')').replace('','').replace('{', '(')
            .replace('}', ')').replace('￥', '').replace('','')
            .replace('/', '').replace(':', "").replace('*','')
            .replace('"',"'").replace('?','').replace('|',"-").replace('...', ' ')))
            try:
                while st1[-1] == '.' or st1[-1] == ' ':
                    st1 = st1[:-1]
                st1 = tool.minitool.while_replace(st1)
            except:
                pass
            return st1




@app.route("/novelpage=<int:count>")
def novel(count):
  if count < webpage:
    original_array = np.array(datanoveljson)
    sub_arrays = np.array_split(original_array, webpage)
    back = f'/novelpage={max(count-1, 0)}'
    next = f'/novelpage={min(count+1, webpage-1)}'
    return render_template('novel.html', data = sub_arrays[count], back = back, next = next, numresult =len(sub_arrays[count]), curenpage = count)
  return render_template('404.html'), 404

@app.route("/noveltimereversepage=<int:count>")
def noveltimereverse(count):
  if count < webpage:
    original_array = np.array(datanoveltimereversejson)
    sub_arrays = np.array_split(original_array, webpage)
    back = f'/noveltimereversepage={max(count-1, 0)}'
    next = f'/noveltimereversepage={min(count+1, webpage-1)}'
    return render_template('novel.html', data = sub_arrays[count], back = back, next = next, numresult =len(sub_arrays[count]), curenpage = count)
  return render_template('404.html'), 404

@app.route("/novelnamepage=<int:count>")
def novelname(count):
  if count < webpage:
    original_array = np.array(datanovelnamejson)
    sub_arrays = np.array_split(original_array, webpage)
    back = f'/novelnamepage={max(count-1, 0)}'
    next = f'/novelnamepage={min(count+1, webpage-1)}'
    return render_template('novel.html', data = sub_arrays[count], back = back, next = next, numresult =len(sub_arrays[count]), curenpage = count)
  return render_template('404.html'), 404

@app.route("/novelnamereversepage=<int:count>")
def novelnamereverse(count):
  if count < webpage:
    original_array = np.array(datanovelnamereversejson)
    sub_arrays = np.array_split(original_array, webpage)
    back = f'/novelnamereversepage={max(count-1, 0)}'
    next = f'/novelnamereversepage={min(count+1, webpage-1)}'
    return render_template('novel.html', data = sub_arrays[count], back = back, next = next, numresult =len(sub_arrays[count]), curenpage = count)
  return render_template('404.html'), 404

@app.route('/novelsearch', methods=["GET", "POST"])
def novelsearch():
  if request.method == 'POST':
    start = time.time()
    selected_options = request.form.getlist('checkbox')
    listdata = []
    for i in datanoveljson:
        count = 0
        for option in selected_options:
            for item in i['tag']:
                try:
                    if tool.minitool.removeSymbols((option).replace(' ', '')).strip().lower() in tool.minitool.removeSymbols((item).replace(' ', '')).strip().lower():
                        count += 1
                        break
                except:
                    pass
        if count == len(selected_options):
            listdata.append(i)
    end = time.time()
    processtime = timedelta(seconds=end-start)
    print(processtime)
    return render_template('novelsearchresult.html', data = listdata, numresult = len(listdata), time = str(processtime))
  return render_template('novelsearch.html')

@app.route('/novel', methods=["GET", "POST"])
def search():
  if request.method == 'POST':
    start = time.time()
    query = request.form['query'].strip().lower()
    query = tool.minitool.removeSymbols(query.replace(' ', ''))
    listdata = [i for i in datanoveljson if any(query in tool.minitool.removeSymbols(item.replace(' ', '')).strip().lower() for item in i['category']) or query in tool.minitool.removeSymbols(i['name'].replace(' ', '')).strip().lower()]
    end = time.time()
    processtime = timedelta(seconds=end-start)
    print(processtime)
    return render_template('novelsearchresult.html', data = listdata, numresult = len(listdata), time = str(processtime))
  else:
    return redirect('/novelpage=0')




@app.errorhandler(404) 
def page_not_found(e):
    print(e)
    return render_template('404.html'), 404

app.run(port = 5500)