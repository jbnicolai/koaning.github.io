#!/usr/bin/env python
from livereload import Server, shell
from pelican import Pelican
from pelican.settings import read_settings

p = Pelican(read_settings('pelicanconf.py'))

def compile():
    try:
        p.run()
    except SystemExit as e:
        pass

compile()

server = Server()
server.watch('content/', compile)
server.watch('../koaning-theme/', compile)
server.serve(root='output')
