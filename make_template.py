import json, urllib.parse
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter as L
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import FormulaRule
from defaults import ins, mat
d=json.load(open('data_app.json')); FIX={'50WFV'}
VG={'Heineken':('2026-10-30','2026-11-14'),'Modelo':('2026-11-05','2026-12-02'),'Kof':('2026-11-05','2026-12-02')}
RUTAS=d['rutas']
ORD=lambda r:(d['order'].get(r['ruta'],[]).index(r['cr']) if r['cr'] in d['order'].get(r['ruta'],[]) else 9999)
COLS=[('Ruta','UBICACIÓN',22,'Obligatorio'),('CR','UBICACIÓN',9,'Obligatorio'),('Tienda','UBICACIÓN',26,'Obligatorio'),
('Municipio','UBICACIÓN',18,'Opcional'),('Dirección','UBICACIÓN',46,'Opcional'),
('Coordenadas (pegar de Google Maps)','UBICACIÓN',30,'Ej. 19.1234, -96.1234'),('Orden','UBICACIÓN',8,'1, 2, 3… (opcional)'),
('Marca','QUÉ INSTALAR',12,'Elegir de la lista'),('Tipo','QUÉ INSTALAR',10,'Lona o Pendón'),('Medida (m)','QUÉ INSTALAR',13,'Ej. 1.35 x 4.85'),('Medida original','QUÉ INSTALAR',13,'Si cambió'),
('Promoción','PROMOCIÓN',58,'Texto que lleva la pieza'),('Vigencia desde','PROMOCIÓN',13,'AAAA-MM-DD'),('Vigencia hasta','PROMOCIÓN',13,'AAAA-MM-DD'),
('Acción','TRABAJO EN EL LUGAR',12,'Elegir de la lista'),('Qué hacer en el lugar','TRABAJO EN EL LUGAR',55,'Pasos a seguir'),('Material (pieza)','TRABAJO EN EL LUGAR',28,'Lo que se lleva'),
('Accesorios y herramientas','TRABAJO EN EL LUGAR',34,'Separar con ;  Ej. cinchos; cinta; escalera'),('Observaciones de la tienda','TRABAJO EN EL LUGAR',30,'Horario, encargado, acceso'),
('Abrir en Google Maps','AYUDA',20,'Solo ayuda (la app no la usa)')]
GC={'UBICACIÓN':'1F4E78','QUÉ INSTALAR':'833C0B','PROMOCIÓN':'375623','TRABAJO EN EL LUGAR':'6A2C91','AYUDA':'595959'}
rows=[]
for r in d['recs']:
    a=d['addr'].get(r['cr'],{}); rows.append((RUTAS.index(r['ruta']),(r['mpo'] or a.get('mpo','')).upper(),r['tienda'],r,'' if r['cr'] in FIX else a.get('dir','')))
rows.sort(key=lambda x:(x[0],ORD(x[3]),x[1],x[2]))
wb=Workbook(); wi=wb.active; wi.title='Instrucciones'; ws=wb.create_sheet('Recorrido'); wr=wb.create_sheet('Resumen'); wc=wb.create_sheet('Catalogos')
thin=Side(style='thin',color='BFBFBF'); bd=Border(left=thin,right=thin,top=thin,bottom=thin)
yel=PatternFill('solid',fgColor='FFF2CC'); gry=PatternFill('solid',fgColor='EDEDED')
# bandas de grupo
c0=1
for g in dict.fromkeys(c[1] for c in COLS):
    n=[i for i,c in enumerate(COLS,1) if c[1]==g]; ws.merge_cells(start_row=1,start_column=n[0],end_row=1,end_column=n[-1])
    x=ws.cell(1,n[0],g); x.font=Font(bold=True,color='FFFFFF',size=12); x.fill=PatternFill('solid',fgColor=GC[g]); x.alignment=Alignment(horizontal='center',vertical='center')
for i,(h,g,w,hint) in enumerate(COLS,1):
    c=ws.cell(2,i,h); c.font=Font(bold=True,color='FFFFFF'); c.fill=PatternFill('solid',fgColor=GC[g]); c.alignment=Alignment(wrap_text=True,vertical='center',horizontal='center'); c.border=bd
    k=ws.cell(3,i,hint); k.font=Font(italic=True,color='7F7F7F',size=9); k.fill=gry; k.alignment=Alignment(wrap_text=True,vertical='center',horizontal='center'); k.border=bd
    ws.column_dimensions[L(i)].width=w
ws.row_dimensions[1].height=22; ws.row_dimensions[2].height=34; ws.row_dimensions[3].height=28
Y={6,7,18,19}  # columnas a completar
for _,mpo,_,r,dir_ in rows:
    v=VG.get(r['marca'],('',''))
    q=(dir_+', '+mpo+', Veracruz, México') if dir_ else 'OXXO '+r['tienda']+', '+mpo+', Veracruz, México'
    ws.append([r['ruta'],r['cr'],r['tienda'],mpo,dir_,'',(ORD(r)+1 if ORD(r)<9999 else ''),r['marca'],r['tipo'],r['medida'],r['orig'],r['promo'] or '',v[0],v[1],'Instalar',ins(r),mat(r),'','','Abrir en Maps'])
    i=ws.max_row
    for c in range(1,len(COLS)+1):
        x=ws.cell(i,c); x.border=bd; x.alignment=Alignment(wrap_text=True,vertical='top')
        if c in Y or (c==5 and not dir_): x.fill=yel
    m=ws.cell(i,20); m.hyperlink='https://www.google.com/maps/search/?api=1&query='+urllib.parse.quote(q); m.font=Font(color='0563C1',underline='single')
last=ws.max_row
ws.freeze_panes='D4'; ws.auto_filter.ref=f'A3:{L(len(COLS))}{last}'
ws.conditional_formatting.add(f'F4:F{last}',FormulaRule(formula=['LEN($F4)>0'],fill=PatternFill('solid',bgColor='C6EFCE')))
def dv(f,col):
    x=DataValidation(type='list',formula1=f,allow_blank=True,errorStyle='warning',showErrorMessage=True,errorTitle='Valor distinto',error='No está en la lista. ¿Seguro?'); ws.add_data_validation(x); x.add(f'{col}4:{col}{last+200}')
dv('"Heineken,Modelo,Kof"','H'); dv('"Lona,Pendón"','I'); dv('"Instalar,Reemplazar,Retirar,Revisar"','O'); dv("=Catalogos!$A$2:$A$12",'A')
ws.sheet_view.zoomScale=90
# Catálogos
wc.append(['Rutas','Marcas','Tipos','Acciones','Accesorios sugeridos'])
for i in range(5): wc.cell(1,i+1).font=Font(bold=True)
for i,x in enumerate(RUTAS,2): wc.cell(i,1,x)
for i,x in enumerate(['Heineken','Modelo','Kof'],2): wc.cell(i,2,x)
for i,x in enumerate(['Lona','Pendón'],2): wc.cell(i,3,x)
for i,x in enumerate(['Instalar','Reemplazar','Retirar','Revisar'],2): wc.cell(i,4,x)
for i,x in enumerate(['Cinchos','Cinta doble cara','Cuerda','Escalera','Tijeras','Ojillos'],2): wc.cell(i,5,x)
for c in 'ABCDE': wc.column_dimensions[c].width=24
# Resumen
wr['A1']='Avance de captura'; wr['A1'].font=Font(bold=True,size=14)
for i,h in enumerate(['Ruta','Espacios','Con coordenadas','% con coordenadas'],1):
    c=wr.cell(3,i,h); c.font=Font(bold=True,color='FFFFFF'); c.fill=PatternFill('solid',fgColor='1F4E78'); c.border=bd
for k,x in enumerate(RUTAS,4):
    wr.cell(k,1,x); wr.cell(k,2,f'=COUNTIF(Recorrido!$A$4:$A$1000,A{k})'); wr.cell(k,3,f'=COUNTIFS(Recorrido!$A$4:$A$1000,A{k},Recorrido!$F$4:$F$1000,"<>")'); wr.cell(k,4,f'=IFERROR(C{k}/B{k},0)'); wr.cell(k,4).number_format='0%'
t=4+len(RUTAS); wr.cell(t,1,'TOTAL').font=Font(bold=True)
wr.cell(t,2,f'=SUM(B4:B{t-1})'); wr.cell(t,3,f'=SUM(C4:C{t-1})'); wr.cell(t,4,f'=IFERROR(C{t}/B{t},0)'); wr.cell(t,4).number_format='0%'
for r_ in range(4,t+1):
    for c in range(1,5): wr.cell(r_,c).border=bd
for c,w in zip('ABCD',[28,12,18,20]): wr.column_dimensions[c].width=w
# Instrucciones
T=[('RECORRIDO LONAS P12 · Cómo llenar este Excel',1),('',0),
('1. Cada FILA es UN espacio a instalar. Una tienda con dos espacios (por ejemplo Modelo y Heineken) ocupa dos filas con el mismo CR.',0),
('2. Colores: AMARILLO = por completar · VERDE = coordenadas listas · GRIS (fila 3) = guía de lo que va en cada columna. No borres las filas 1 a 3.',0),
('3. COORDENADAS (lo más importante para el mapa): en la columna "Abrir en Google Maps" toca "Abrir en Maps", mantén presionado el lugar correcto, copia los números que aparecen arriba (ej. 19.1234, -96.1234) y pégalos en "Coordenadas". También sirve pegar el enlace largo de Google Maps. Sin coordenadas la tienda igual aparece en la lista y se navega con Google Maps; solo no sale en el mapa de la app.',0),
('4. PROMOCIÓN: el texto que lleva la pieza y su vigencia (AAAA-MM-DD). La app avisa si la promoción aún no inicia o ya venció.',0),
('5. TRABAJO EN EL LUGAR: "Acción" (Instalar, Reemplazar, Retirar o Revisar), "Qué hacer en el lugar" (pasos), "Material (pieza)" (lo que se lleva) y "Accesorios y herramientas" separados con punto y coma (;). Los textos de "Qué hacer" y "Material" vienen como SUGERENCIA: edítalos con tus pasos reales.',0),
('6. ORDEN (opcional): número de visita dentro de cada ruta. Si lo dejas vacío, la app ordena por municipio y código postal.',0),
('7. Para una ruta nueva escribe otro nombre en "Ruta". Marca: Heineken, Modelo o Kof (otra marca también se acepta). Medida con formato 1.35 x 4.85.',0),
('8. Guarda el archivo y en la app pulsa "📥 Cargar Excel". La app reemplaza los datos y arma rutas, tiendas, mapa, instrucciones y lista de material.',0),
('9. No cambies los nombres de los encabezados de la fila 2 ni el nombre de la hoja "Recorrido". Puedes agregar filas al final.',0),
('10. La hoja "Resumen" muestra cuántas coordenadas llevas por ruta.',0)]
for i,(t_,b) in enumerate(T,1):
    c=wi.cell(i,1,t_); c.alignment=Alignment(wrap_text=True,vertical='top'); c.font=Font(bold=bool(b),size=15 if b else 11,color='C8102E' if b else '000000')
wi.column_dimensions['A'].width=125
wb.save('Plantilla_Recorrido.xlsx'); print(len(rows),'filas')
