#include <wiringPi.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <json-c/json.h>

#define PIN 16

int bits[5] = {0,0,0,0,0}; // buffer for data
double temp,hum;

void read(){
	uint8_t state = HIGH;
	uint8_t co = 0;
	uint8_t j = 0, i;

	bits[0]=bits[1]=bits[2]=bits[3]=bits[4]= 0;

	// pull pin down
	pinMode(PIN, OUTPUT);
	digitalWrite(PIN, HIGH);
	delay(500);
	digitalWrite(PIN, LOW);
	delay(20);

	// read pin
	pinMode(PIN, INPUT);

	// detect change and read
	for (i=0; i < 85; i++)
	{
		co = 0;
		while(digitalRead(PIN) == state)
		{
			co++;
			delayMicroseconds(2);
			if (co == 255){
				break;
			}
		}
	state = digitalRead(PIN);

	if ( co == 255) break;

	if ((i >= 4) && (i%2 == 0)) {
      	// shove each bit into the storage bytes
     	bits[j/8] <<= 1;
      	if (co > 16)
        bits[j/8] |= 1;
      	j++;
   		}
	}
	// check we read 40 bits (8bit x 5 ) + verify checksum in the last byte
  	// print it out if data is good
  	if ((j >= 40) && (bits[4] == ((bits[0] + bits[1] + bits[2] + bits[3]) & 0xFF)) )
	{
		float h = (float)((bits[0] << 8) + bits[1]) / 10;
		if ( h > 100)
		{
			h = bits[0];
			//hum = h;
		}
		float c = (float)(((bits[2] & 0x7F) << 8) + bits[3]) / 10;
		if ( c > 125)
		{
			c = bits[2];
			//temp = c;
		}
		if ( bits[2] & 0x80)
		{
			c = -c;
		}
		printf("Temperature = %.1f C\n",c);
		printf("Humidity = %.1f\n",h);
	}
	else 
	{
		printf("bad value\n");
	}
}

int main( void )
{

	if ( wiringPiSetup() == -1 )
		exit( 1 );

	while ( 1 )
	{
		printf("Content-Type: text/html\n\n");
		read();

        	json_object * object = json_object_new_object();
        	json_object * temperatur = json_object_new_double(temp);
        	json_object * feuchtigkeit = json_object_new_double(hum);

        	json_object_object_add(object, "Temperature\n", temperatur);
        	json_object_object_add(object, "Humidity\n", feuchtigkeit);

        	printf("json file: %sn", json_object_to_json_string(object));
        	//printf("</body>\n");
        	//printf("</html>\n");
	}
	/*printf( "Raspberry Pi DHT11/DHT22 temperature/humidity test\n" );

	if ( wiringPiSetup() == -1 )
		exit( 1 );

	while ( 1 )
	{
		read();
		delay( 2000 );
	}*/

	return(0);
}
