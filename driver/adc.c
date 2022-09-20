#include <stdio.h>
#include <stdint.h>
#include <unistd.h>
#include <stdlib.h>

/*
    CONSIDERATION :
        This Snippet of code it complitly temrory and need to be modifiled in term of
        scalabilty and performande

    Writter : Parsa Oskouie
    Emanil : parsaoski.po@gmail.com
*/


typedef struct DeviceProperty_t{
	uint32_t raw ;
	uint32_t scale;
	uint32_t sampling_frequency;
}DeviceProperty_t;


DeviceProperty_t Device1={
		.raw = 0,
		.scale = 2,
		.sampling_frequency = 1600,
};



uint32_t find_device1 (uint32_t scale);
static uint32_t read_raw_device1 (void);
uint32_t read_mean_raw_device1(uint32_t time);
float read_mean_voltage_device1(uint32_t time);


//int main (void){
//	float volt;
//
//	volt = read_mean_voltage_device1(10);
//	printf("%2.2f",volt);
//
//
//}







uint32_t find_device1 (uint32_t scale){
	const char * iio_device1_in_voltage1_scale_path = "/sys/bus/iio/devices/iio:device1/in_voltage1_scale";
	//const char * iio_device1_in_voltage1_sf_path = "/sys/bus/iio/devices/iio:device1/in_voltage1_sampling_frequency";
	FILE *f_scale;
	//FILE *f_sf;

	// Here We Just Check One File to Make sure that we have our device ready
	// no need to check all files to found if iio is available or not
	f_scale = fopen(iio_device1_in_voltage1_scale_path,"w");
//	f_sf = fopen(iio_device1_in_voltage1_sf_path,"r");
	if (f_scale==NULL){
		printf("\r\nError Couldnt Find Device\r\n");
		return 1;
	}
	// We set Scale Here For now :)))
	Device1.scale = scale;
	fprintf(f_scale,"%d",scale);
	fclose(f_scale);
	return 0;
}

static uint32_t read_raw_device1 (void){
	const char * iio_device1_in_voltage1_raw_path = "/sys/bus/iio/devices/iio:device1/in_voltage1_raw";
	FILE *f_raw;
	char tmp[50];
	uint32_t value = 0;
	f_raw = fopen(iio_device1_in_voltage1_raw_path,"r");
	fread(&tmp,4,1,f_raw);
	value = atoi(tmp);
	fclose(f_raw);
	return value;
}

uint32_t read_mean_raw_device1(uint32_t time){
	uint32_t value=0;
	uint32_t sum=0;
	uint32_t mean=0;
	uint32_t itr=0;
	for(itr=0;itr<time;itr++){
		value = read_raw_device1();
		sum +=value;
	}
	mean = sum /time;
	return mean;
}

float read_mean_voltage_device1(uint32_t time){

	uint32_t value=0;
	uint32_t sum=0;
	uint32_t mean=0;
	uint32_t itr=0;
	float voltage=0;
	// Calculation Of The Mean
	for(itr=0;itr<time;itr++){
		value = read_raw_device1();
		sum +=value;
	}
	mean = sum /time;
	// here First We Use The Mean Of The Raw Inputs and Then We will calculate voltage
	voltage = (float)(mean*Device1.scale)/1000.0;
	//	printf("%d",value);
	//	printf("\r\n%d",Device1.scale);
	//	printf("\r\n%f\r\n",voltage);
	return voltage;
}



/*
 Hint Files temp here for now
 we we want to call c library from pwm.so we should declare it it as normal void if we use static keyworld it wont expose itself for python or any other library.
 we use thi command for compiling the code :
    gcc -std=gnu11 -shared -fPIC -o adc.so adc.c

    Normal Compile :
    	gcc -std=gnu11 adc.c -o adc

  Furthure its a example one need to be modified in better way but its good for now :))
*/

