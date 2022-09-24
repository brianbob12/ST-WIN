
from Core.GameObjects.PositionedGameObject import PositionedGameObject

from numpy import ndarray

class PositionedAngledGameObject(PositionedGameObject):
  __slots__=("angle")

  def __init__(self, startingPosition:ndarray, startingAngle:float, name=None):
    super().__init__(startingPosition,name)
    self.angle:float= startingAngle
