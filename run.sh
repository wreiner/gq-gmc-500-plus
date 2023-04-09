#!/bin/sh

cd /gq-gmc500plus
gunicorn -w 1 'gq-gmc500plus:app' -b 0.0.0.0:8500
