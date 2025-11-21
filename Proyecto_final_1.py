#TODO hay error, bug

#Proyecto final teoría de la computación
#Validador de contrseñas
'''
Condiciones:
•	Debe iniciar con una letra
•	Debe contener al menos un número
•	Debe contener al menos un carácter especial de estos: @, #, $, %, &
•	Debe tener mínimo 8 caracteres
•	Debe contener al menos una letra mayúscula
'''

class ValidadorPasswordAF:
    def __init__(self):
        # Definir alfabeto
        self.LETRAS_MIN = 'abcdefghijklmnopqrstuvwxyz'
        self.LETRAS_MAY = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.NUMEROS = '0123456789'
        self.ESPECIALES = '@#$%&'
        
        # Estado inicial
        self.estado_actual = 'q0'
        self.longitud = 0
        self.condiciones_cumplidas = {
            'inicia_letra': False,
            'tiene_numero': False,
            'tiene_especial': False,
            'tiene_mayuscula': False,
            'longitud_minima': False
        }
        
        # Historial para debugging
        self.historial = []
    
    def reset(self):
        """Reiniciar el autómata"""
        self.estado_actual = 'q0'
        self.longitud = 0
        self.condiciones_cumplidas = {k: False for k in self.condiciones_cumplidas}
        self.historial = []
    
    def transicion(self, caracter):
        """Aplicar transición según el carácter actual"""
        self.longitud += 1
        estado_anterior = self.estado_actual
        
        # Si ya estamos en estado de aceptación, nos mantenemos ahí
        if self.estado_actual == 'q_acept':
            self.historial.append({
                'caracter': caracter,
                'estado_anterior': estado_anterior,
                'estado_actual': self.estado_actual,
                'tipo': 'aceptado',
                'longitud': self.longitud
            })
            return
        
        # Determinar tipo de carácter
        if caracter in self.LETRAS_MIN:
            tipo = 'letra_min'
        elif caracter in self.LETRAS_MAY:
            tipo = 'letra_mayus'
            self.condiciones_cumplidas['tiene_mayuscula'] = True
        elif caracter in self.NUMEROS:
            tipo = 'numero'
            self.condiciones_cumplidas['tiene_numero'] = True
        elif caracter in self.ESPECIALES:
            tipo = 'especial'
            self.condiciones_cumplidas['tiene_especial'] = True
        else:
            tipo = 'invalido'
        
        # Aplicar transiciones según estado actual
        if self.estado_actual == 'q0':
            if tipo in ['letra_min', 'letra_mayus']:
                self.estado_actual = 'q1' if tipo == 'letra_min' else 'q4'
                self.condiciones_cumplidas['inicia_letra'] = True
            else:
                self.estado_actual = 'q_error'
                
        elif self.estado_actual == 'q1':
            if tipo == 'letra_mayus':
                self.estado_actual = 'q4'
            elif tipo == 'numero':
                self.estado_actual = 'q2'
            elif tipo == 'especial':
                self.estado_actual = 'q3'
            elif tipo == 'letra_min':
                self.estado_actual = 'q1'
            else:
                self.estado_actual = 'q_error'
                
        elif self.estado_actual in ['q2', 'q3', 'q4']:
            # Una vez en q2, q3 o q4, permanecemos en estados válidos
            if tipo == 'invalido':
                self.estado_actual = 'q_error'
            # Transiciones entre estados para cumplir condiciones faltantes
            elif self.estado_actual == 'q2':
                if tipo == 'letra_mayus':
                    self.estado_actual = 'q4'
                elif tipo == 'especial':
                    self.estado_actual = 'q3'
            elif self.estado_actual == 'q3':
                if tipo == 'letra_mayus':
                    self.estado_actual = 'q4'
                elif tipo == 'numero':
                    self.estado_actual = 'q2'
            # q4 ya tiene mayúscula, puede permanecer en q4 o ir a q2/q3
        
        # Verificar si alcanzamos estado de aceptación
        if (self.estado_actual in ['q2', 'q3', 'q4'] and 
            self.longitud >= 8 and 
            all(self.condiciones_cumplidas.values())):
            self.estado_actual = 'q_acept'
        
        # Guardar historial
        self.historial.append({
            'caracter': caracter,
            'estado_anterior': estado_anterior,
            'estado_actual': self.estado_actual,
            'tipo': tipo,
            'longitud': self.longitud
        })
    
    def validar_password(self, password):
        """Validar una contraseña completa"""
        self.reset()
        
        print(f"🔐 Validando: {password}")
        print("=" * 50)
        
        for i, char in enumerate(password):
            if self.estado_actual == 'q_error':
                print(f"❌ Carácter '{char}' en posición {i+1} inválido. Contraseña rechazada.")
                return False
            
            self.transicion(char)
            
            # Mostrar progreso
            estado_display = self.estado_actual
            if self.estado_actual == 'q_acept':
                estado_display = "q_acept ✅"
            elif self.estado_actual == 'q_error':
                estado_display = "q_error ❌"
                
            print(f"Carácter {i+1}: '{char}' → Estado: {estado_display}")
            self.mostrar_condiciones()
            print("-" * 30)
            
            # Si llegamos a estado de error, terminar
            if self.estado_actual == 'q_error':
                print(f"❌ Contraseña inválida en carácter {i+1}")
                return False
        
        # Verificación final
        if self.estado_actual == 'q_acept':
            print("✅ ¡CONTRASEÑA VÁLIDA! Cumple todas las condiciones.")
            return True
        else:
            print("❌ CONTRASEÑA INVÁLIDA. No cumple todas las condiciones:")
            self.mostrar_condiciones()
            return False
    
    def mostrar_condiciones(self):
        """Mostrar estado actual de las condiciones"""
        condiciones = self.condiciones_cumplidas.copy()
        condiciones['longitud_minima'] = self.longitud >= 8
        
        for cond, cumple in condiciones.items():
            estado = "✅" if cumple else "❌"
            print(f"  {estado} {cond.replace('_', ' ').title()}")
        
        print(f"  📏 Longitud actual: {self.longitud}/8")
        
        # Mostrar estado actual del autómata
        if self.estado_actual == 'q_acept':
            print("  🎯 Estado: ACEPTACIÓN")
        elif self.estado_actual == 'q_error':
            print("  💥 Estado: ERROR")
        else:
            print(f"  🔄 Estado: {self.estado_actual}")

# Programa principal
def main():
    validador = ValidadorPasswordAF()
    
    print("🚀 VALIDADOR DE CONTRASEÑAS CON AUTÓMATA FINITO")
    print("Reglas:")
    print("• Debe iniciar con letra")
    print("• Debe contener al menos un número") 
    print("• Debe contener al menos un carácter especial (@ # $ % &)")
    print("• Debe tener al menos una mayúscula")
    print("• Longitud mínima: 8 caracteres")
    print("=" * 60)
    
    # Casos de prueba automáticos
    test_cases = [
        "Passw0rd#",        # ✅ Válida
        "Passw0rd#extra",   # ✅ Válida (más de 8 caracteres)
        "password",         # ❌ Falta número, especial, mayúscula
        "12345678",         # ❌ No inicia con letra  
        "Password",         # ❌ Falta número y especial
        "passw0rd",         # ❌ Falta especial y mayúscula
        "P@ssw",            # ❌ Muy corta
        "A1b2c3d4e5f6#",    # ✅ Válida (más de 8)
    ]
    
    print("\n🧪 EJECUTANDO CASOS DE PRUEBA AUTOMÁTICOS:")
    print("=" * 60)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 Caso de prueba {i}: '{test_case}'")
        print("-" * 40)
        resultado = validador.validar_password(test_case)
        print(f"Resultado: {'✅ VÁLIDA' if resultado else '❌ INVÁLIDA'}")
        print("=" * 60)
    
    # Modo interactivo
    print("\n🎮 MODO INTERACTIVO:")
    print("=" * 60)
    
    while True:
        password = input("\nIngrese la contraseña a validar (o 'salir' para terminar): ")
        
        if password.lower() == 'salir':
            break
            
        print("\n" + "=" * 60)
        resultado = validador.validar_password(password)
        print("=" * 60)
        
        if resultado:
            print("\n🎉 ¡Contraseña aceptada!")
        else:
            print("\n💡 Sugerencia: Asegúrese de cumplir todas las reglas.")
        
        input("\nPresione Enter para continuar...")

if __name__ == "__main__":
    main()