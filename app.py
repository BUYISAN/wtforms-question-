from flask import Flask, request, render_template,jsonify
from disc_form import DiscForm
from answer import answers

app = Flask(__name__)
app.config['SECRET_KEY'] = 'onelogindemopytoolkit'


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'GET':
        form = DiscForm()
    else:
        form = DiscForm(request.form)
        if form.validate_on_submit():
            username = form.username.data
            ans = {}
            for i in range(1, len(answers) + 1):
                q_name = 'answer{}'.format(i)
                ans['answer{}'.format(i)] = getattr(form, q_name).data
            ret = {'username': username,
                   'ans':ans}
            return jsonify(ret)
    return render_template('disc.html', form=form, answers=answers)



if __name__ == '__main__':
    app.run()
