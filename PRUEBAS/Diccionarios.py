# -*- coding: utf-8 -*-
# comentario

MiDicc = {'nombre' : 'Gustavo',
          'paterno' : 'Martinez',
          'materno' : 'Velasco',
          'edad' : '55',
          'sexo' : 'masculino',
          'calle' : 'Juan de Montoro',
          'numero' : '422',
          'colonia' : 'Centro',
          'ciudad' : 'Aguascalientes',
          }

print("\n")
valor = 'sexo'
print("llave: '{}', valor: '{}'".format(valor, MiDicc[valor]))
print("\n\n")

print (u"Parámetros:")
print (MiDicc.keys())
print (MiDicc.values())
print (MiDicc.items())
print (MiDicc.get('materno'))
print (MiDicc.setdefault('estatura' , 1.75))
print (MiDicc.pop('edad'))
print (MiDicc)