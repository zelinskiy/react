import json
import os
import time
from flask import Flask, Response, request

app = Flask(__name__, static_url_path='', static_folder='public')
app.add_url_rule('/', 'root', lambda: app.send_static_file('index.html'))


@app.route('/api/like', methods=['POST'])
def like_handler():
    with open('comments.json', 'r') as f:
        comments = json.loads(f.read())

    if request.method == 'POST':
        cid = request.form.to_dict()["id"]
        comment = next((c for c in comments if str(c['id'])== str(cid)), None)
        if(comment != None):
            comment["likes"] = comment["likes"] + 1

        with open('comments.json', 'w') as f:
            f.write(json.dumps(comments, indent=4, separators=(',', ': ')))

    return Response(
        json.dumps("OK"),
        mimetype='application/json',
        headers={
            'Cache-Control': 'no-cache',
            'Access-Control-Allow-Origin': '*'
        }
    )


@app.route('/api/comments', methods=['GET', 'POST'])
def comments_handler():
    with open('comments.json', 'r') as f:
        comments = json.loads(f.read())

    if request.method == 'POST':
        new_comment = request.form.to_dict()
        new_comment['id'] = int(time.time() * 1000)
        new_comment['likes'] = 0
        comments.append(new_comment)

        with open('comments.json', 'w') as f:
            f.write(json.dumps(comments, indent=4, separators=(',', ': ')))

    return Response(
        json.dumps(comments),
        mimetype='application/json',
        headers={
            'Cache-Control': 'no-cache',
            'Access-Control-Allow-Origin': '*'
        }
    )


if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT", 3000)))
