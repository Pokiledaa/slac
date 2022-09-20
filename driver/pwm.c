#include <stdio.h>
#include <stdint.h>
#include <unistd.h>
#include <sys/stat.h>

/*
    CONSIDERATION :
        This Snippet of code it complitly temrory and need to be modifiled in term of
        scalabilty and performande

    Writter : Parsa Oskouie
    Emanil : parsaoski.po@gmail.com
*/



#define ENABLE  1

typedef struct pwm_device_t {
    uint32_t pwm_chip ;
    uint32_t pwm_channel;
    uint32_t frequency;
    uint32_t period;
    uint32_t duty_cycle;
}pwm_device_t;


pwm_device_t ccs_pwm_a={
    .pwm_chip = 8,
    .pwm_channel = 0,
    .frequency = 1000,
    .period = 0,
    .duty_cycle = 0,
};

void ccs_pwm_config (uint32_t ccs_type);
void ccs_pwm_set_frequency (uint32_t ccs_type ,uint32_t freq);
void ccs_pwm_set_duty_cycle (uint32_t ccs_type,float duty);
static int is_directory_exists(const char *path);



// int main (void){

//    ccs_pwm_config(1);
//    sleep(5);
//    ccs_pwm_set_duty_cycle(1,5);
//    sleep(5);
//    ccs_pwm_set_duty_cycle(1,100);
//    sleep(5);


// }


void ccs_pwm_set_frequency (uint32_t ccs_type ,uint32_t freq){

    const char* pwm_period_path = "/sys/class/pwm/pwmchip8/pwm0/period";
    FILE * fptr = fopen(pwm_period_path,"w");
    ccs_pwm_a.frequency = freq;
    ccs_pwm_a.period = 1000000000UL/ccs_pwm_a.frequency;
    fprintf(fptr,"%d",ccs_pwm_a.period);

    fclose (fptr);
}


void ccs_pwm_set_duty_cycle (uint32_t ccs_type,float duty){

    const char* pwm_duty_path = "/sys/class/pwm/pwmchip8/pwm0/duty_cycle";
    FILE * fptr = fopen(pwm_duty_path,"w");
    float percent = 0.0;
    if (duty>=100) {
        duty = 100;
    }
    // real_duty = (duty/100) * period
    percent = duty/100 ;
    ccs_pwm_a.duty_cycle = (uint32_t)(percent*ccs_pwm_a.period);
    fprintf(fptr,"%d",ccs_pwm_a.duty_cycle);
    fclose(fptr);
}


void ccs_pwm_config (uint32_t ccs_type){
    // Local Variable
    uint8_t dir_exist = 0;
    const char* pwm_channel_path = "/sys/class/pwm/pwmchip8/pwm0";
    const char* pwm_channel_export_path = "/sys/class/pwm/pwmchip8/export";
    const char* pwm_channel_enable_path = "/sys/class/pwm/pwmchip8/pwm0/enable";




    // We check  here if the directory exist and if not we need to export the pwm channel
    dir_exist = is_directory_exists(pwm_channel_path);
    if (dir_exist == 0){

        FILE * fptr = fopen(pwm_channel_export_path,"w");
        // expporting the pwm channel
        fprintf(fptr,"%d",ccs_pwm_a.pwm_channel);
        printf("pwm Channel Exported");
        fclose(fptr);
    }

    // The if We made sure That the Pwm Channel has been created we will set the frequency
    ccs_pwm_set_frequency(ccs_type,ccs_pwm_a.frequency);
    // then will set the duty cycle for 100 percent ;
    ccs_pwm_set_duty_cycle(ccs_type,ccs_pwm_a.duty_cycle);

    // at the last we should enable the pwm signal :))
     FILE* e_fptr = fopen(pwm_channel_enable_path,"w");
     fprintf(e_fptr,"%d",ENABLE);
     fclose(e_fptr);

}

/**
 * Function to check whether a directory exists or not.
 * It returns 1 if given path is directory and  exists
 * otherwise returns 0.
 */
static int is_directory_exists(const char *path)
{
    struct stat stats;

    stat(path, &stats);

    // Check for file existence
    if (S_ISDIR(stats.st_mode))
        return 1;

    return 0;
}

/*
 Hint Files temp here for now
 we we want to call c library from pwm.so we should declare it it as normal void if we use static keyworld it wont expose itself for python or any other library.
 we use thi command for compiling the code :
    gcc -shared -fPIC -o pwm.so pwm.c

  Furthure its a example one need to be modified in better way but its good for now :))
*/
