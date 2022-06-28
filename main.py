import code_getter, random,hashlib,datetime
import requests as re
from flask import *
app = Flask(__name__)
app.config['SECRET_KEY'] = "KeepItSmiple:)"
with open("db/langs.json") as fp:
    langs = json.load(fp)
with open("db/data.json") as fp:
    data = json.load(fp)
with open("db/themes.json") as fp:
    themes = json.load(fp)
with open("db/pending_themes.json") as fp:
    pending_themes = json.load(fp)


def saveJson():
    with open("db/data.json", "w+") as fp:
        json.dump(data, fp, indent=4)
    with open("db/themes.json", "w+") as fp:
        json.dump(themes, fp, indent=4)
    with open("db/pending_themes.json", "w+") as fp:
        json.dump(pending_themes, fp, indent=4)

def hasher(text) -> str:return hashlib.sha256(text.encode("ascii")).hexdigest()

def auth(username, pw):
    try:
        if data[username]['pw'] == hasher(pw):
            return True
        return False
    except KeyError:
        return False

def get_leaderboard():
    leaderBoard = {}
    for player in data.keys():
        leaderBoard[player] = data[player]['pts']
    return list(dict(sorted(leaderBoard.items(), key=lambda item: item[1])).keys())[::-1]

@app.route('/')
def index():
	username = request.cookies.get('username')
	pw = request.cookies.get('pw')
	if auth(username, pw):
		if "theme" not in data[username].keys():
			data[username]["theme"] = "black_and_white"
			saveJson()
		return render_template("index.html", r=random.randint(0, 9273), allData=data, theme=themes[data[username]['theme']],username=username, leaderboard=get_leaderboard(), themeName=data[username]['theme'])
	return render_template("auth.html", r=random.randint(0, 9273), theme=themes["black_and_white"])

@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        pw = request.form['pw']
        if len(username) > 15 or len(pw) > 50 or len(email) > 25:
            flash("Username, password or email is too long")
        if username in data:
            flash("Username already in use", category="error")
        for user in data:
            if data[user]['email'] == email:
                flash("Email already in use", category="error")
        data[username] = {
            "email": email,
            "pw": hasher(pw),
            "pts":0,
            "games":0,
            "best_streak":0,
            "joined":datetime.datetime.now().strftime("%d/%m/%Y"),
            "theme":"black_and_white"
        }
        saveJson()
        cookie = make_response(redirect("/"))
        cookie.set_cookie('pw', pw)
        cookie.set_cookie('username', username)
        flash("Account created", category="success")
        return cookie

    flash("Something went wrong", category="error")
    return redirect('/')

@app.route('/logout')
def logout():
    cookie = make_response(redirect("/"))
    cookie.set_cookie('pw', "")
    cookie.set_cookie('username', "")
    return cookie

@app.route('/endgame', methods=['POST'])
def endgame():
    if request.method == 'POST':
        username = request.cookies.get('username')
        pw = request.cookies.get('pw')
        if auth(username, pw):
            pts = int(request.form['pts'])
            data[username]['pts'] += pts
            data[username]['games'] += 1 
            if pts > data[username]['best_streak']:
                data[username]['best_streak'] = pts
            saveJson()
            return jsonify({"pts":pts, "best_streak":data[username]['best_streak']})
        return jsonify({"error":"Not logged in"})
    return jsonify({"error":"Not logged in"})

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        pw = request.form['pw']
        print(hasher(pw))
        print(data[username]['pw'])
        if auth(username, pw):
            cookie = make_response(redirect("/"))
            cookie.set_cookie('pw', pw)
            cookie.set_cookie('username', username)
            flash("Logged in", category="success")
            return cookie
        flash("Wrong username or password", category="error")
        return redirect('/')

    flash("Something went wrong", category="error")
    return redirect("/")

@app.route('/api')
def api():
    code = code_getter.get()
    text = re.get(code['code']).text
    print(code['code'])
    res = []
    for i in range(3):
        x = random.choice(langs)
        if code['lang'] != x and x not in res:
            res.append(x)
    res.append(code['lang'])
    random.shuffle(res)
    if len(res) != 4:
        res.append(random.choice(langs))
    return jsonify({"langs":res, "code":text, "c":code['lang'], "uri":code['code'].split("/raw/")[0].split('/')[4]})

@app.route('/change-pw', methods=['POST'])
def change_pw():
    username = request.cookies.get('username')
    pw = request.cookies.get('pw')
    if auth(username, pw):
        if hasher(request.form['old-pw']) == hasher(pw):
            print(request.form['new-pw'])
            print(hasher(request.form['new-pw']))
            data[username]['pw'] = hasher(request.form['new-pw'])
            res = make_response(redirect("/"))
            res.set_cookie('pw', request.form['new-pw'])
            saveJson()
            flash("Password updated!", category="success")
            return res
        flash("Wrong password", category="error")
        return redirect('/')
    flash("Something went wrong", category="error")
    return redirect('/')

@app.route('/change-theme', methods=['POST'])
def change_theme():
    username = request.cookies.get('username')
    pw = request.cookies.get('pw')
    if auth(username, pw):
        data[username]['theme'] = request.form['theme']
        saveJson()
        return jsonify({"status":"OK"})
    return "error"

@app.errorhandler(404)
def page_404(error):
    return render_template("404.html", r=random.randint(0, 9037))


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
    # app.run(host='0.0.0.0', port=8000, debug=True)