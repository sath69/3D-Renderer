import pygame
from matrix import Matrix
from mesh import Cube,Tetrahedron,Triangle
from vector import Vector3
import pyopencl as openCL
import numpy as np

code = """
    __kernel void multiplyMat(__global float4* vertices,__global float* matrix, __global float4* output)
    {
        int i = get_global_id(0);
        float4 v = vertices[i];
        
        float x = v.x;
        float y = v.y;
        float z = v.z;
        float w = v.w;

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
        
        output[i] = (float4)(x_out, y_out,z_out,1.0f);
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

def multiplyMatrix(vertices, matrix):
      
       _num_vertices = vertices.shape[0]
       _matrix = np.array(matrix, dtype=np.float32).reshape(16)
       _output = np.zeros_like(vertices)

       _inputBuffer = openCL.Buffer(context, openCL.mem_flags.READ_ONLY | openCL.mem_flags.COPY_HOST_PTR,hostbuf= vertices)
       _matrixBuffer = openCL.Buffer(context, openCL.mem_flags.READ_ONLY | openCL.mem_flags.COPY_HOST_PTR,hostbuf=_matrix)

       _outputBuffer = openCL.Buffer(context, openCL.mem_flags.WRITE_ONLY, _output.nbytes)

       multiplyMat_kernel.set_args(_inputBuffer, _matrixBuffer, _outputBuffer)
       openCL.enqueue_nd_range_kernel(queue, multiplyMat_kernel, (_num_vertices,), None)
       openCL.enqueue_copy(queue, _output, _outputBuffer)
       return _output

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
    
    
    #Render tetrahedron
    verts = []
    for tri in tetrahedron.triangles:
        
        verts.extend([
            [tri.v1.x, tri.v1.y, tri.v1.z, 1.0],
            [tri.v2.x, tri.v2.y, tri.v2.z, 1.0],
            [tri.v3.x, tri.v3.y, tri.v3.z, 1.0]])
    verts = np.array(verts, dtype=np.float32)
       
       
    #Perform Z axis rotation
    triRotZ = multiplyMatrix(verts, zRotMatrix)
       
    #Perform X axis rotation
    triRotZX = multiplyMatrix(triRotZ, xRotMatrix)
    triRotZX[:, 2] += 3.0
    
    #Projection
    triangleProjected = multiplyMatrix(triRotZX, projectionMatrix)
       
    #Scale the triangles into view
    triangleProjected[:, 0] += 0.8
    triangleProjected[:, 1] += 0.8

    triangleProjected[:,0] *= 0.25 * screen.get_width() 
    triangleProjected[:, 1] *= 0.25 * screen.get_height()

    #Draw triangle
    for i in range(0, len(triangleProjected), 3):
          vertices = [
            (int(triangleProjected[i][0]), int(triangleProjected[i][1])),
            (int(triangleProjected[i+1][0]), int(triangleProjected[i+1][1])),
            (int(triangleProjected[i+2][0]), int(triangleProjected[i+2][1]))
          ]
          pygame.draw.polygon(screen, (0, 200, 255), vertices, 2)
        
       
    
    #Render cube
    verts = []
    for tri in cube.triangles:
        
        verts.extend([
            [tri.v1.x, tri.v1.y, tri.v1.z, 1.0],
            [tri.v2.x, tri.v2.y, tri.v2.z, 1.0],
            [tri.v3.x, tri.v3.y, tri.v3.z, 1.0]])
    verts = np.array(verts, dtype=np.float32)
        
    #Perform Z axis rotation
    triRotZ = multiplyMatrix(verts, zRotMatrix)
       
    #Perform X axis rotation
    triRotZX = multiplyMatrix(triRotZ, xRotMatrix)
       
    triRotZX[:, 2] += 3.0
    #Projection
    triangleProjected = multiplyMatrix(triRotZX, projectionMatrix)
       
    #Scale the triangles into view
    triangleProjected[:, 0] += 0.8
    triangleProjected[:, 1] += 0.8

    triangleProjected[:,0] *= 0.5 * screen.get_width() 
    triangleProjected[:, 1] *= 0.5 * screen.get_height()

    #Draw triangle 
    for i in range(0, len(triangleProjected), 3):
        vertices = [
            (int(triangleProjected[i][0]), int(triangleProjected[i][1])),
            (int(triangleProjected[i+1][0]), int(triangleProjected[i+1][1])),
            (int(triangleProjected[i+2][0]), int(triangleProjected[i+2][1]))
        ]
        pygame.draw.polygon(screen, (0, 200, 255), vertices, 2)
        
      
    pygame.display.flip()
    clock.tick(FPS)



