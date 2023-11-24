#define PIN_16 16
#define PIN_14 14
#define PIN_12 12
#define PIN_13 13
#define PIN_15 15
#define PIN_0 0
#define PIN_4 4
#define PIN_5 5
#define CICLO_ASPERSOR 480000  // 8 minutos en milisegundos
#define CICLO_RIEGO 86400000   // 24 horas en milisegundos

// 14, 12, 13, 15, 0, 4, 5

void setup() {
  // Configurar pines
  pinMode(PIN_16, OUTPUT);
  pinMode(PIN_14, OUTPUT);
  pinMode(PIN_12, OUTPUT);
  pinMode(PIN_13, OUTPUT);
  pinMode(PIN_15, OUTPUT);
  pinMode(PIN_0, OUTPUT);
  pinMode(PIN_4, OUTPUT);
  pinMode(PIN_5, OUTPUT);
  
}

void loop() {

    TIEMPO = 0

    digitalWrite(PIN_16, HIGH);


    digitalWrite(PIN_14, HIGH);
    delay(CICLO_ASPERSOR);
    TIEMPO += CICLO_ASPERSOR;
    digitalWrite(PIN_14, LOW);

    digitalWrite(PIN_12, HIGH);
    delay(CICLO_ASPERSOR);
    TIEMPO += CICLO_ASPERSOR;
    digitalWrite(PIN_12, LOW);

    digitalWrite(PIN_13, HIGH);
    delay(CICLO_ASPERSOR);
    TIEMPO += CICLO_ASPERSOR;
    digitalWrite(PIN_13, LOW);

    digitalWrite(PIN_15, HIGH);
    delay(CICLO_ASPERSOR);
    TIEMPO += CICLO_ASPERSOR;
    digitalWrite(PIN_15, LOW);

    digitalWrite(PIN_0, HIGH);
    delay(CICLO_ASPERSOR);
    TIEMPO += CICLO_ASPERSOR;
    digitalWrite(PIN_0, LOW);
    
    digitalWrite(PIN_4, HIGH);
    delay(CICLO_ASPERSOR);
    TIEMPO += CICLO_ASPERSOR;
    digitalWrite(PIN_4, LOW);
    
    digitalWrite(PIN_5, HIGH);
    delay(CICLO_ASPERSOR);
    TIEMPO += CICLO_ASPERSOR;
    digitalWrite(PIN_5, LOW);

    
    digitalWrite(PIN_16, LOW);
    delay(CICLO_RIEGO - TIEMPO);
}
