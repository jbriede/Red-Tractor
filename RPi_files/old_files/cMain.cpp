/*
 Copyright (C) 2011 J. Coliz <maniacbug@ymail.com>

 This program is free software; you can redistribute it and/or
 modify it under the terms of the GNU General Public License
 version 2 as published by the Free Software Foundation.

 03/17/2013 : Charles-Henri Hallard (http://hallard.me)
              Modified to use with Arduipi board http://hallard.me/arduipi
						  Changed to use modified bcm2835 and RF24 library
TMRh20 2014 - Updated to work with optimized RF24 Arduino library

 */

/**
 * Example RF Radio Ping Pair
 *
 * This is an example of how to use the RF24 class on RPi, communicating to an Arduino running
 * the GettingStarted sketch.
 */

#include <cstdlib>
#include <iostream>
#include <sstream>
#include <string>
#include <RF24/RF24.h>
#include <stdlib.h>
#include <stdio.h>
#include <boost/array.hpp>
#include <boost/asio.hpp>

using namespace std;
using boost::asio::ip::udp;
//
// Hardware configuration
//

// CE Pin, CSN Pin, SPI Speed

// Setup for GPIO 22 CE and CE1 CSN with SPI Speed @ 1Mhz
//RF24 radio(RPI_V2_GPIO_P1_22, RPI_V2_GPIO_P1_26, BCM2835_SPI_SPEED_1MHZ);

// Setup for GPIO 22 CE and CE0 CSN with SPI Speed @ 4Mhz
//RF24 radio(RPI_V2_GPIO_P1_15, BCM2835_SPI_CS0, BCM2835_SPI_SPEED_4MHZ);

// Setup for GPIO 22 CE and CE0 CSN with SPI Speed @ 8Mhz
RF24 radio(RPI_V2_GPIO_P1_22, RPI_V2_GPIO_P1_24, BCM2835_SPI_SPEED_8MHZ);


// Radio pipe addresses for the 2 nodes to communicate.
//const uint8_t pipes[][6] = {"1Node","2Node"};
const uint64_t pipes[2] = { 0xABCDABCD71LL, 0x544d52687CLL };


int main(int argc, char** argv){

  //bool role_ping_out = true, role_pong_back = false;
  //bool role = role_pong_back;



  // Print preamble:
  //printf("RF24/examples/pingtest/\n");

  // Setup and configure rf radio
  radio.begin();

  // optionally, increase the delay between retries & # of retries
  radio.setRetries(15,15);
  // Dump the configuration of the rf unit for debugging
  radio.printDetails();

/***********************************/
  // This simple sketch opens two pipes for these two nodes to communicate
  // back and forth.


radio.openWritingPipe(pipes[1]);
radio.openReadingPipe(1,pipes[0]);
radio.startListening();

//UDP initializations
boost::asio::io_service io_service;
udp::socket socket(io_service, udp::endpoint(udp::v4(), 5005));//5005    
boost::array<char, 128> sensor_buf;
udp::endpoint remote_endpoint;	

	// forever loop
	while (1)
	{
	//
	// Pong back role.  Receive each packet, dump it out, and send it back
	//
		
		// if there is data ready
		//printf("Check available...\n");

		if ( radio.available() )
		{

        char instruct[12]= {0};                             //  ------------------------------------- (EDITED LINE)

       //int bytesRead = 0;
       //char instruct;                            //  ------------------------------------- (EDITED LINE THAT WORKS... iffy)
        //int16_t instruct;

			// Fetch the payload, and see if this was the last one.
        radio.read( instruct, 12 );
	radio.stopListening();
	
// UDP Server communication with pMain.py
	
	
//	try
//	{
		remote_endpoint.port(5006);
		boost::system::error_code error;
		
		std::string instructs = std::string(instruct, 12);
		std::cout << instructs << std::endl;
		if(error && error != boost::asio::error::message_size)
			throw boost::system::system_error(error);
		
		boost::system::error_code ignored_error;
		
		socket.send_to(boost::asio::buffer(instructs), remote_endpoint, 0, ignored_error); //send instruct to pMain.py
		
		remote_endpoint.port(5005);
		size_t len = socket.receive_from(boost::asio::buffer(sensor_buf), 
			remote_endpoint, 0, error); //recieve sensor packet from pMain.py
		std::string sensor = std::string(sensor_buf.data(), len);
		std::cout << sensor << std::endl;                           // alternate--> std::cout.write(instruct_buf.data(), len);
						// write back sensor packet	
        	radio.write(sensor_buf.data(), len );
		
//	}
//	catch (std::exception& e)
//	{
//		std::cerr << e.what() << std::endl;
//	}	
	

// Now, resume listening so we catch the next packets.
	radio.startListening();
// Spew it
        printf("%s \n", instruct);

			
			delay(25); //Delay after payload responded to, minimize RPi CPU time
			
		}// if radio available
	
	

	} // forever loop

  return 0;
}

