

from typing import Optional
from Core.GameObjects.GameObject import GameObject

#handles multiprocessing
class Root(GameObject):

  def __init__(self, name: Optional[str] = None):
    super().__init__(name)

  def instantiateDefaultCallbackRoutes(self):
    return super().instantiateDefaultCallbackRoutes()