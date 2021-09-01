PROJ = led
CC = cc
SRC = main.c led_on_off.c
LIBS = -lgpiod
CFLAGS = -D CONSUMER=\"$(PROJ)\"

all:
	$(CC) $(SRC) $(LIBS) $(CFLAGS) -o $(PROJ)
clean:
	rm $(PROJ)
