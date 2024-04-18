from django import template

register = template.Library()
CENSORED_WORDS = ('панк', 'депутат', 'выборы')
@register.filter
def censor(text):
    censored_text = text
    for censored_word in CENSORED_WORDS:
        censored_text = censored_text.replace(censored_word, censored_word[:1] + '*' * (len(censored_word) - 1))
    return censored_text
