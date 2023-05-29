from tokens import *

def scan(token):
    if token == 'ws':
        try:
            return WHITESPACE
        except Error:
            return f'El token es indefinido'
    if token == 'characters':
        try:
            return CHARACTERS
        except Error:
            return f'El token es indefinido'
    if token == '/*':
        try:
            return LEFTCOMMENT
        except Error:
            return f'El token es indefinido'
    if token == '*/':
        try:
            return RIGHTCOMMENT
        except Error:
            return f'El token es indefinido'
    if token == '%token':
        try:
            return TOKEN
        except Error:
            return f'El token es indefinido'
    if token == '|':
        try:
            return OR
        except Error:
            return f'El token es indefinido'
    if token == 'IGNORE':
        try:
            return IGNORE
        except Error:
            return f'El token es indefinido'
    if token == 'minusword':
        try:
            return MINUSCULA
        except Error:
            return f'El token es indefinido'
    if token == 'mayusword':
        try:
            return MAYUSCULA
        except Error:
            return f'El token es indefinido'
    if token == '%%':
        try:
            return SPLIT
        except Error:
            return f'El token es indefinido'
    if token == ':':
        try:
            return TWOPOINTS
        except Error:
            return f'El token es indefinido'
    if token == ';':
        try:
            return FINISHDECLARATION
        except Error:
            return f'El token es indefinido'
    return f'Token indefinido: '
