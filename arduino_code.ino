#include <Wire.h>
#include <LiquidCrystal_I2C.h>

#define BUZZER 23

LiquidCrystal_I2C lcd(0x27, 16, 2);  // address may be 0x27 or 0x3F

String data = "";

void setup() {
  Serial.begin(9600);

  pinMode(BUZZER, OUTPUT);
  digitalWrite(BUZZER, LOW);

  lcd.init();
  lcd.backlight();

  lcd.setCursor(0,0);
  lcd.print("Driver System");
}

void loop() {
  if (Serial.available()) {
    data = Serial.readStringUntil('\n');

    lcd.clear();
    lcd.setCursor(0,0);
    lcd.print("Status:");

    lcd.setCursor(0,1);
    lcd.print(data);

    // 🔊 BUZZER LOGIC
    if (data == "DROWSY" || data == "DOWN") {
      digitalWrite(BUZZER, HIGH);
    } else {
      digitalWrite(BUZZER, LOW);
    }
  }
}
