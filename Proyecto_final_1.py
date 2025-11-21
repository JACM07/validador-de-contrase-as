print("Proyecto final Teoría de la Computación")

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
            # hasta que se cumplan todas las condiciones
            if tipo == 'invalido':
                self.estado_actual = 'q_error'
            # Permanece en el mismo estado o transiciona para cumplir otras condiciones
            elif self.estado_actual == 'q2' and tipo == 'letra_mayus':
                self.estado_actual = 'q4'
            elif self.estado_actual == 'q2' and tipo == 'especial':
                self.estado_actual = 'q3'
            elif self.estado_actual == 'q3' and tipo == 'letra_mayus':
                self.estado_actual = 'q4'
            elif self.estado_actual == 'q3' and tipo == 'numero':
                self.estado_actual = 'q2'
        
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
            print(f"Carácter {i+1}: '{char}' → Estado: {self.estado_actual}")
            self.mostrar_condiciones()
            print("-" * 30)
        
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