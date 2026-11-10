# Textos sugeridos por defecto (editables en el Excel)
def ins(r):
    if not r['marca']: return ''
    if r['tipo'].lower().startswith('pend'):
        return 'Retirar el pendón anterior si existe · colocar el pendón nuevo, visible desde la calle · tomar foto del antes y del después'
    return 'Retirar la lona anterior si existe · limpiar la superficie · colocar la lona tensada y alineada · tomar foto del antes y del después'
def mat(r):
    if not r['marca']: return ''
    return f"{r['tipo']} {r['marca']} {r['medida']} m"
