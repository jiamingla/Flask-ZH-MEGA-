from app import create_app, db, cli
from app.models import User, Post
#flask shell的絕妙之處不在於它預先匯入了app，
#而是你可以配置一個 “shell 上下文”，
# 也就是可以預先匯入一份物件列表。
app = create_app()
cli.register(app)

#app.shell_context_processor裝飾器將該函式註冊為一個 shell 上下文函式。 
# 當flask shell命令執行時，
# 它會呼叫這個函式並在 shell 會話中註冊它返回的專案。 
# 函式返回一個字典而不是一個列表，原因是對於每個專案，
# 你必須透過字典的鍵提供一個名稱以便在 shell 中被呼叫。
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}

