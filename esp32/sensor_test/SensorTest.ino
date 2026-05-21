#include <DHT.h>

const byte DHT_PIN = 18; 
const byte DHT_TYPE = DHT11; 

DHT dht(DHT_PIN, DHT_TYPE); 

void setup() {
    Serial.begin(115200); 
    Serial.println("DHT11 Sensor Test: "); 
    dht.begin(); 
}

void loop() {
    float humidity = dht.readHumidity(); 
    float temperature = dht.readTemperature(); 
     
    if (isnan(humidity) || isnan(temperature)){
        Serial.println("Failed to read from DHT sensor. "); 
        delay(2000); 
        return; 
    }

    Serial.print("Humidity: "); 
    Serial.print(humidity); 
    Serial.print("% "); Serial.print("  |  "); 
    Serial.print("Temperature"); 
    Serial.print(temperature); 
    Serial.println("°C"); 

    delay(2000);
}