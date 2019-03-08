# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import RadioField, StringField
from wtforms.widgets import RadioInput, HTMLString, html_params
from wtforms.validators import DataRequired, InputRequired
from answer import answers


class DiscInput(RadioInput):
    input_type = 'radio'

    def __call__(self, field, **kwargs):
        if field.checked:
            kwargs['checked'] = True
        kwargs.setdefault('id', field.id)
        kwargs.setdefault('type', self.input_type)
        if 'value' not in kwargs:
            kwargs['value'] = field._value()
        if 'required' not in kwargs and 'required' in getattr(field, 'flags', []):
            kwargs['required'] = True
        return HTMLString('<span class="radiowrapper"><input %s></span>' % self.html_params(name=field.name, **kwargs))


class DiscListWidget(object):
    def __init__(self, html_tag='div', prefix_label=True):
        assert html_tag in ('div',)
        self.html_tag = html_tag
        self.prefix_label = prefix_label

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        html = ['<%s %s>' % (self.html_tag, html_params(**kwargs))]
        for subfield in field:
            if self.prefix_label:
                html.append('<div>%s %s</div>' % (subfield.label, subfield()))
            else:
                html.append('<div>%s %s</div>' % (subfield(), subfield.label))
        html.append('</%s>' % self.html_tag)
        return HTMLString(''.join(html))


def get_fields():
    ret = {"username": StringField(u'姓名', validators=[InputRequired(message=u'请输入姓名')])}
    i = 1
    for a in answers:
        answer = a['answer']
        values = a['values']
        ret['answer' + str(i)] = RadioField(a['question'], choices=zip(values, answer), default='', id='q{}'.format(i),
                                            render_kw={'class': 'ui-radio'}, option_widget=DiscInput(),
                                            widget=DiscListWidget(prefix_label=False),
                                            validators=[DataRequired(u'请选择该题')])
        i += 1
    return ret


DiscForm = type('DiscForm', (FlaskForm,), get_fields())
