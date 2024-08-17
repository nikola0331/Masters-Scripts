import pyopencl as cl
import numpy as np
import matplotlib.pyplot as plt 

# Create random input arrays
array_size = 10
#input_array1 = np.random.rand(array_size).astype(np.float32)
#input_array2 = np.random.rand(array_size).astype(np.float32)

y_1 = []
f = open('y_1.txt')
for line in f.readlines():
    y_1.append(float(line))
f.close()

y_2 = []
f = open('y_2.txt')
for line in f.readlines():
    y_2.append(float(line))
f.close()

input_array1 = np.asarray(y_1, dtype = np.float32)
input_array2 = np.asarray(y_2, dtype = np.float32)


# Initialize OpenCL context and queue
platform = cl.get_platforms()[0]
device = platform.get_devices()[0]
context = cl.Context([device])
queue = cl.CommandQueue(context)

# Create OpenCL buffer objects for input arrays and output array
input_buffer1 = cl.Buffer(context, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR, hostbuf=input_array1)
input_buffer2 = cl.Buffer(context, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR, hostbuf=input_array2)
output_buffer = cl.Buffer(context, cl.mem_flags.WRITE_ONLY, input_array1.nbytes)
output_buffer2 = cl.Buffer(context, cl.mem_flags.WRITE_ONLY, input_array1.nbytes)


# Define the OpenCL kernel code for element-wise multiplication
kernel_code = """
__kernel void multiply(__global const float* input1, __global const float* input2, __global float* output, global float* output2) {
    int global_id = get_global_id(0);
    output[global_id] = input1[global_id] * input2[global_id];
    
    int pointer = 0;
    
    for (int i = 0; i < 200; i++) {
        float sum = 0.0;
        if (pointer < 32) {
            for (int j = 0; j < pointer; j++) {
                sum += output[j];
            }
        } else {
            for (int j = pointer - 31; j < pointer; j++) {
                sum += output[j];
            }
        }
     
	output2[i] = (sum/32.0);
	pointer++;
    }
}
"""

# Create an OpenCL program from the kernel code
program = cl.Program(context, kernel_code).build()

# Execute the kernel
program.multiply(queue, input_array1.shape, None, input_buffer1, input_buffer2, output_buffer, output_buffer2)

# Read the result from the output buffer
output_array = np.empty_like(input_array1)
cl.enqueue_copy(queue, output_array, output_buffer)

output_array2 = np.empty_like(input_array1)
cl.enqueue_copy(queue, output_array2, output_buffer2)

# Print the results

print("Output array:", output_array)
print("Output array 2:", output_array2)

plt.plot(output_array2)
plt.show()
