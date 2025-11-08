import pygame
from matrix import Matrix
from mesh import Cube,Tetrahedron,Triangle
from vector import Vector3
import pyopencl as openCL
import numpy as np

code = """
    __kernel void multiplyMat(__global float* input,__global float* matrix, __global float* output)
    {
        float x = input[0];
        float y = input[1];
        float z = input[2];
        
        float x_out = x*matrix[0] + y*matrix[4] + z*matrix[8] + matrix[12];
        float y_out = x*matrix[1] + y*matrix[5] + z*matrix[9] + matrix[13];
        float z_out = x*matrix[2] + y*matrix[6] + z*matrix[10] + matrix[14];
        float w_out = x*matrix[3] + y*matrix[7] + z*matrix[11] + matrix[15];

        if (w_out != 0.0f)
        {
            x_out /= w_out;
            y_out /= w_out;
            z_out /= w_out;
        }
        
        output[0] = x_out;
        output[1] = y_out;
        output[2] = z_out;
    }
"""

#Kernel 
context = openCL.create_some_context()
queue = openCL.CommandQueue(context)


bld = openCL.Program(context, code).build()
multiplyMat_kernel = openCL.Kernel(bld, "multiplyMat")

#Define pygame window
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3D Renderer")
clock = pygame.time.Clock()
start_ticks = pygame.time.get_ticks()
FPS = 100 

def multiplyMatrix(input, matrix):
      
       _input = np.array([input.x, input.y, input.z,1], dtype=np.float32)
       _matrix = np.array(matrix, dtype=np.float32).reshape(4,4)
       _output = np.zeros(3,dtype=np.float32)

       _inputBuffer = openCL.Buffer(context, openCL.mem_flags.READ_ONLY | openCL.mem_flags.COPY_HOST_PTR,hostbuf=_input)
       _matrixBuffer = openCL.Buffer(context, openCL.mem_flags.READ_ONLY | openCL.mem_flags.COPY_HOST_PTR,hostbuf=_matrix)

       _outputBuffer = openCL.Buffer(context, openCL.mem_flags.WRITE_ONLY, _output.nbytes)

       multiplyMat_kernel.set_args(_inputBuffer, _matrixBuffer, _outputBuffer)
       openCL.enqueue_nd_range_kernel(queue, multiplyMat_kernel, (1,), None)

       openCL.enqueue_copy(queue, _output, _outputBuffer)
      

       return Vector3(_output[0],_output[1],_output[2])

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    screen.fill((0, 0, 0))  
    
    #Get elapsed time for smooth rotations
    theta = 0
    elapsed_time = (pygame.time.get_ticks()-start_ticks)/1000
    theta += 1 * (elapsed_time)
    
    #Define geometry, projection and rotation matrices
    cube = Cube()
    tetrahedron = Tetrahedron()
    matrix = Matrix()
    projectionMatrix = matrix.projectionMatrix(screen)
    zRotMatrix = matrix.zRotation(theta)
    xRotMatrix = matrix.xRotation(theta)
    
    """
    #Render tetrahedron
    for tri in tetrahedron.triangles:

       #Perform Z axis rotation
       triRotZ1 = matrix.multiplyMatrix(tri.v1, zRotMatrix)
       triRotZ2 = matrix.multiplyMatrix(tri.v2, zRotMatrix)
       triRotZ3 = matrix.multiplyMatrix(tri.v3, zRotMatrix)

       #Perform Y axis rotation
       triRotZX1 = matrix.multiplyMatrix(triRotZ1, xRotMatrix)
       triRotZX2 = matrix.multiplyMatrix(triRotZ2, xRotMatrix)
       triRotZX3 = matrix.multiplyMatrix(triRotZ3, xRotMatrix)

       #Projection
       v1 = matrix.multiplyMatrix(triRotZX1.translate_z(triRotZX1,3), projectionMatrix)
       v2 = matrix.multiplyMatrix(triRotZX2.translate_z(triRotZX2,3), projectionMatrix)
       v3 = matrix.multiplyMatrix(triRotZX3.translate_z(triRotZX3,3), projectionMatrix)
       
       triangleProjected = Triangle(v1,v2,v3)

       #Scale the triangles into view
       triangleProjected.v1.x += 0.8
       triangleProjected.v1.y += 0.8
       triangleProjected.v2.x += 0.8
       triangleProjected.v2.y += 0.8
       triangleProjected.v3.x += 0.8
       triangleProjected.v3.y += 0.8

       triangleProjected.v1.x *= 0.5 * screen.get_width() 
       triangleProjected.v1.y *= 0.5 * screen.get_height()
       triangleProjected.v2.x *=  0.5 * screen.get_width() 
       triangleProjected.v2.y *= 0.5 * screen.get_height()
       triangleProjected.v3.x *=  0.5 * screen.get_width() 
       triangleProjected.v3.y *= 0.5 * screen.get_height()

       #Draw triangle
       pygame.draw.polygon(screen, (0, 200, 255), [(triangleProjected.v1.x, triangleProjected.v1.y), (triangleProjected.v2.x, triangleProjected.v2.y), (triangleProjected.v3.x, triangleProjected.v3.y)], 2) 
       
    """
    #Render cube
    for tri in cube.triangles:

        #Perform Z axis rotation
        triRotZ1 = multiplyMatrix(tri.v1, zRotMatrix)
        triRotZ2 = multiplyMatrix(tri.v2, zRotMatrix)
        triRotZ3 = multiplyMatrix(tri.v3, zRotMatrix)
       
        #Perform Y axis rotation
        triRotZX1 = multiplyMatrix(triRotZ1, xRotMatrix)
        triRotZX2 = multiplyMatrix(triRotZ2, xRotMatrix)
        triRotZX3 = multiplyMatrix(triRotZ3, xRotMatrix)
       
        #Projection
        v1 = multiplyMatrix(triRotZX1.translate_z(triRotZX1,3), projectionMatrix)
        v2 = multiplyMatrix(triRotZX2.translate_z(triRotZX2,3), projectionMatrix)
        v3 = multiplyMatrix(triRotZX3.translate_z(triRotZX3,3), projectionMatrix)
       
        triangleProjected = Triangle(v1, v2, v3)
       
        #Scale the triangles into view
        triangleProjected.v1.x += 0.8
        triangleProjected.v1.y += 0.8
        triangleProjected.v2.x += 0.8
        triangleProjected.v2.y += 0.8
        triangleProjected.v3.x += 0.8
        triangleProjected.v3.y += 0.8

        triangleProjected.v1.x *= 0.5 * screen.get_width() 
        triangleProjected.v1.y *= 0.5 * screen.get_height()
        triangleProjected.v2.x *=  0.5 * screen.get_width() 
        triangleProjected.v2.y *= 0.5 * screen.get_height()
        triangleProjected.v3.x *=  0.5 * screen.get_width() 
        triangleProjected.v3.y *= 0.5 * screen.get_height()
       
        #Draw triangle
        pygame.draw.polygon(screen, (0, 200, 255), [(int(triangleProjected.v1.x), int(triangleProjected.v1.y)), (int(triangleProjected.v2.x), int(triangleProjected.v2.y)), (int(triangleProjected.v3.x), int(triangleProjected.v3.y))], 2) 
      
    pygame.display.flip()
    clock.tick(FPS)



