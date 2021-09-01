#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#include "led_on_off.h"

int main (int argc, char **argv)
{
	printf("Content-type: text/html\n\n");

	printf("Turning led OFF\n");
	led_off();
	
	return 0;
}
