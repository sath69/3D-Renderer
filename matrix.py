from vector import Vector3
import math

#Matrix
class Matrix:
     
  #Projection matrix
  def projectionMatrix(self,screen):
      fNear = 0.1
      fFar = 1000.0
      fovValue = math.pi * 0.5
      aspect_ratio = screen.get_height() / screen.get_width()
      fov = 1 / math.tan(fovValue*0.5)
      q = fFar / (fFar - fNear)
      matProj = [[aspect_ratio * fov,0.0,0.0,0.0],[0.0,fov,0.0,0.0],[0.0,0.0,q,1.0],[0.0,0.0,(-fFar * fNear)/(fFar - fNear),0.0]]
      return matProj
  
  #Perform matrix multiplication 4x4
  def multiplyMatrix(self, input, matrix):
       x = input.x * matrix[0][0] + input.y * matrix[1][0] + input.z * matrix[2][0] + matrix[3][0]
       y = input.x * matrix[0][1] + input.y * matrix[1][1] + input.z * matrix[2][1] + matrix[3][1]
       z = input.x * matrix[0][2] + input.y * matrix[1][2] + input.z * matrix[2][2] + matrix[3][2]
       w = input.x * matrix[0][3] + input.y * matrix[1][3] + input.z * matrix[2][3] + matrix[3][3]
    
       if w != 0:
         x /= w
         y /= w
         z /= w
       return Vector3(x,y,z)
  
  #Rotation around Z
  def zRotation(self,deltaTime):
      rotZMatrix = [[math.cos(deltaTime),math.sin(deltaTime),0,0],[-math.sin(deltaTime),math.cos(deltaTime),0,0],[0,0,1,0],[0,0,0,1]]
      return rotZMatrix

  #Rotation around X
  def xRotation(self, deltaTime):
      rotXMatrix = [[1,0,0,0],[0,math.cos(0.5*deltaTime),math.sin(0.5*deltaTime),0],[0,-math.sin(0.5*deltaTime),math.cos(0.5*deltaTime),0],[0,0,0,1]]
      return rotXMatrix

