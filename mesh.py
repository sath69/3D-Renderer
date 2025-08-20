from vector import Vector3

class Triangle:
    def __init__(self, v1, v2, v3):
        self.vertices = [v1,v2,v3]
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3

class Tetrahedron:
    def __init__(self):
       self.vertices = [
            Vector3(1,0,1),
            Vector3(0,0,0),
            Vector3(1,1,0),
            Vector3(0,1,1),
       ]

       self.triangles = [
           Triangle(self.vertices[1],self.vertices[0],self.vertices[2]),
           Triangle(self.vertices[3],self.vertices[0],self.vertices[1]),
           Triangle(self.vertices[2],self.vertices[3],self.vertices[0]),
           Triangle(self.vertices[1],self.vertices[2],self.vertices[3]),
       ]
    

class Cube:
   def __init__(self):
       self.vertices = [
           Vector3(0,0,0),
           Vector3(0,1,0),
           Vector3(0,0,1),
           Vector3(1,0,0),
           Vector3(1,1,0),
           Vector3(1,0,1),
           Vector3(0,1,1),
           Vector3(1,1,1)
       ]
       self.triangles = [
           
           #South
           Triangle(self.vertices[0], self.vertices[4], self.vertices[3]),
           Triangle(self.vertices[0], self.vertices[1], self.vertices[4]),
           #East
           Triangle(self.vertices[3], self.vertices[7], self.vertices[5]),
           Triangle(self.vertices[3], self.vertices[4], self.vertices[7]),
           #North
           Triangle(self.vertices[5], self.vertices[7], self.vertices[6]),
           Triangle(self.vertices[5], self.vertices[6], self.vertices[2]),
           #West
           Triangle(self.vertices[2], self.vertices[6], self.vertices[1]),
           Triangle(self.vertices[2], self.vertices[1], self.vertices[0]),
           #Top
           Triangle(self.vertices[1], self.vertices[6], self.vertices[7]),
           Triangle(self.vertices[1], self.vertices[7], self.vertices[4]),
           #Bottom
           Triangle(self.vertices[5], self.vertices[2], self.vertices[0]),
           Triangle(self.vertices[5], self.vertices[0], self.vertices[3]),
       ]
