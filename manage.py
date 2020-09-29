from backend import create_app

# 调用导入 create_app()  不能直接用导入 app
app = create_app()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
