import json
import requests
from flask import current_app
from flask_babel import _

#該函式定義需要翻譯的文字、源語言和目標語言為引數，
# 並返回翻譯後文本的字串。 
# 它首先檢查配置中是否存在翻譯服務的 Key，
# 如果不存在，則會返回錯誤。 
# 錯誤也是一個字串，所以從外部看，這將看起來像翻譯文字。
#  這可確保在出現錯誤時使用者將看到有意義的錯誤訊息。
def translate(text, source_language, dest_language):
    if 'MS_TRANSLATOR_KEY' not in current_app.config or not current_app.config['MS_TRANSLATOR_KEY']:
        print(current_app.config['MS_TRANSLATOR_KEY'])
        return _('Error: the translation service is not configured.')
    auth = {
        'Ocp-Apim-Subscription-Key': current_app.config['MS_TRANSLATOR_KEY'],
        'Ocp-Apim-Subscription-Region': 'westus2'}
    print(auth)
    r = requests.post(
        'https://api.cognitive.microsofttranslator.com/translate?api-version=3.0&from={}&to={}'.format(
            source_language, dest_language), headers=auth, json=[
                {'Text': text}])
    print(r)
    if r.status_code != 200:
        return _('Error: the translation service failed.')
    return r.json()[0]['translations'][0]['text']