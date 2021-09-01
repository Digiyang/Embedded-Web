#include <stdio.h>
#include <unistd.h>
#include <gpiod.h>


#ifndef CONSUMER
#define CONSUMER "Consumer"
#endif

#include "led_on_off.h"

char *chipname = "gpiochip0";
unsigned int line_num = 14;
unsigned int val;
struct gpiod_chip *chip;
struct gpiod_line *line;
int i, ret;



int led_on()
{
	chip = gpiod_chip_open_by_name(chipname);
	if(!chip)
	{
		perror("Open chip failed!\n");
		goto end;
	}

	line = gpiod_chip_get_line(chip, line_num);
	if (!line)
	{
		perror("Get line failed!\n");
		goto close_chip;
	}

	ret = gpiod_line_request_output(line, CONSUMER, 0);
	if (ret < 0)
	{
		perror("Request line as output failed! \n");
		goto release_line;
	}
	// Led On pin 14
	val = 1;
	ret = gpiod_line_set_value(line, val);
	if (ret < 0)
	{
		perror("Set line output failed!\n");
		goto release_line;
	}

	printf("Output %u on line #%u\n\n", val, line_num);

release_line:
	gpiod_line_release(line);
close_chip:
	gpiod_chip_close(chip);
end:
	return 0;
}

int led_off()
{
	
	chip = gpiod_chip_open_by_name(chipname);
	if (!chip)
	{
		perror("Open Chip failed\n");
		goto end;
	}

	line = gpiod_chip_get_line(chip, line_num);
	if (!line)
	{
		perror("Get line failed!\n");
		goto close_chip;
	}

	ret = gpiod_line_request_output(line, CONSUMER, 0);
	if (ret < 0)
	{
		perror("Requuest line as output failed!\n");
		goto release_line;
	}
	
	// Led OFF
	val = 0;
	ret = gpiod_line_set_value(line, val);
	if (ret < 0)
	{
		perror("Set line output failed!\n");
		goto release_line;
	}

	printf("Output %u on line #%u\n\n", val, line_num);

release_line:
	gpiod_line_release(line);
close_chip:
	gpiod_chip_close(chip);
end:
	return 0;
}
