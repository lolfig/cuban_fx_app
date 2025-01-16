import app

if __name__ == '__main__':
  print("Iniciando dashboard...")
  
  app.socketio.run(
    app.server,
    debug=True,
    use_reloader=False,
  )
