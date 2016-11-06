import os
from flask import Flask, request, Response

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    # Handle GET
    if request.method == 'GET':
        return 'Hello World!\n'

    # Handle POST
    else:
        print(str(request.data))
        return Response(status=200)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(port=port)
