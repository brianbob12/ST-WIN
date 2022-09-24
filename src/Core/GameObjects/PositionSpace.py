

from typing import Dict, List, Optional
from Core.GameObjects.GameObject import GameObject
from Core.GameObjects.PositionedGameObject import PositionedGameObject
from numpy import ndarray,zeros

class PositionSpace(GameObject):
  __slots__=(
    "positionedGameObjects",
    "dimensionality"  
  )

  def __init__(self,dimensionality:int=2, name: Optional[str] = None):
    super().__init__(name)
    #stores a list of positioned game objects for easy rendering
    #the PositionedGameObject class will add itself to this list
    self.positionedGameObjects:List[PositionedGameObject]= []
    self.dimensionality: int= dimensionality

  def instantiateDefaultCallbackRoutes(self):
    self.implementedCallbacks:Dict[str,bool]={
      "onCreate":False,
      "onTick":False,
      "onDestroy":False,
      "onTickClassCallback":len(self.tickClassCallbacks)>0
    }

  def getAbsolutePosition(self)->ndarray:
    return zeros(self.dimensionality)

  @staticmethod
  def getAbsoluteRotation()->float:
    return 0.0