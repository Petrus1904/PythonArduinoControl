#define lowByte(w) ((uint8_t) ((w) & 0xff))
#define highByte(w) ((uint8_t) ((w) >> 8))

#define AnalogIn A0
#define PWMpin 6

int Vout;
int PWMin;
byte InByte;

void setup() {
  // Use the fastest baudrate to increase sampling rate
  Serial.begin(115200);
  // set timer 0 divisor to 1 for PWM frequency of 62500.00 Hz
  // timer 0 affects PWM pins 5 and 6.
  // Note that changing this to Timer 0 ruins any time based command
  // like delay() or millis(). 
  TCCR0B = TCCR0B & B11111000 | B00000001;
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(PWMpin, OUTPUT);
  analogWrite(PWMpin, 0);
}

void loop() {
  // Wait for serial input
  if (Serial.available() > 0) {
    InByte = Serial.read();
    
    switch((int)InByte)
    {
      case 1: //Update PWM output without acknowledgment
        digitalWrite(LED_BUILTIN, LOW);
        //read next value which represents the new input value
        while(Serial.available()==0) {}
        PWMin = (int)Serial.read();
        analogWrite(PWMpin, PWMin);
        break;
        
      case 2: //Request measurement
        digitalWrite(LED_BUILTIN, HIGH);
        Vout = analogRead(AnalogIn);
        // value is between 0 and 1024, so it occupies 2 bytes. Send each sequentially
        Serial.write(highByte(Vout));
        Serial.write(lowByte(Vout));
        break;
        
      case 3: //Update PWM output with acknowledgment
        digitalWrite(LED_BUILTIN, LOW);
        //read next value which represents the new input value
        while(Serial.available()==0) {}
        PWMin = (int)Serial.read();
        analogWrite(PWMpin, PWMin);
        Serial.write(1);
        break;
    }
  }
}
