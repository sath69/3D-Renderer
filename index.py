import pygame
from matrix import Matrix
from mesh import Cube,Tetrahedron,Triangle
from vector import Vector3

#Define pygame window
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3D Renderer")
clock = pygame.time.Clock()
start_ticks = pygame.time.get_ticks()
FPS = 100 

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
       pygame.draw.polygon(screen, (0, 200, 255), [(triangleProjected.v1.x, triangleProjected.v1.y), (triangleProjected.v2.x, triangleProjected.v2.y), (triangleProjected.v3.x, triangleProjected.v3.y)], 1) 
    
    """
    #Render cube
    for tri in cube.triangles:

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
       pygame.draw.polygon(screen, (0, 200, 255), [(triangleProjected.v1.x, triangleProjected.v1.y), (triangleProjected.v2.x, triangleProjected.v2.y), (triangleProjected.v3.x, triangleProjected.v3.y)], 1) 
     """ 
    pygame.display.flip()
    clock.tick(FPS)