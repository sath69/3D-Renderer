class Vector3:
    def __init__(self, x, y, z):
          self.x = x
          self.y = y
          self.z = z
    
    #Translation by Z
    def translate_z(self,v, amount):
      return Vector3(v.x, v.y, v.z + amount)