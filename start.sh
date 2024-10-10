#!/bin/sh

# Configurar la variable DISPLAY
DISPLAY=:99
export DISPLAY

# Iniciar Xvfb
Xvfb :99 -screen 0 1024x768x24 &
XVFB_PID=$!

# Iniciar dbus
dbus-daemon --system --fork

# Esperar a que Xvfb se inicie
sleep 2

# Ejecutar Gunicorn
gunicorn --bind 0.0.0.0:8000 app.app.asgi:application

# Finalizar Xvfb al salir
kill $XVFB_PID
