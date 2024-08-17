  #include <stdio.h>
  #include <time.h>
  #include <sys/times.h>
  #include "platform.h"
  #include "xil_printf.h"
  #include "xil_io.h"
  #include "xbasic_types.h"
  #include "xparameters.h"

  // data address of IP block read from Vivado
  #define CUSTOM_IP_BASEADDR 0x00010000  
  Xuint32 *baseaddr_p = (Xuint32 *)CUSTOM_IP_BASEADDR;
  int main()
  {
  unsigned char Nr1[720] = {0x40, 0x40, 0x41, 0x42, ... ,0x3, 0x3, 0x3}; // Nr1
  unsigned char Nr2[720] = {0x43, 0x44, 0x45, 0x46, ..., 0x4, 0x4, 0x4}; // Nr2
    unsigned short runSum = 0x0000;
    uint32_t divide, dataToSend = 0x00000000;
    uint32_t res0, res1, res2, avg;
    
      init_platform();
  
      for (size_t i = 0; i < sizeof(Nr1) / sizeof(Nr1[0]); ++i) {
        // first 16 bits set to the two hex numbers
        dataToSend = Nr1[i] << 24 | (Nr2[i] << 16); 
        // lower 16 bits set to running sum
        dataToSend = dataToSend | runSum;			
        
          *(baseaddr_p+0) = dataToSend; 
          if (i % 4 == 0) {
            divide = 0x00000001;
          } else {
            divide = 0x00000000;
          }
     *(baseaddr_p+2) = divide; //count
  
    // Read multiplier output from registers
    res0 = *(baseaddr_p+0);
    xil_printf("Reg 0 : 0x%08x \n\r", res0);
    res1 = *(baseaddr_p+1);
    xil_printf("Reg 1 : 0x%08x \n\r", res1);
    res2 = *(baseaddr_p+2);
    xil_printf("Reg 2 : 0x%08x \n\r", res2);
    runSum =  res1 & 0xFFFF;
          }
    xil_printf("End of correlator\n\n\r");

    cleanup_platform();

    return 0;
