from __future__ import annotations

from typing import Dict, Optional, Union
from Core.Exceptions import PositionedGameObjectNotPartOfPositionSpace
from Core.GameObjects.GameObject import GameObject
from Core.GameObjects.PositionSpace import PositionSpace

from numpy import ndarray

class PositionedGameObject(GameObject):

  __slots__=(
    "position",
    "positionSpace",
    "positionedRoot"
    )

  def __init__(self, startingPosition:ndarray ,name: Optional[str] = None):
    super().__init__(name)

    #position is relative to parent
    self.position:ndarray= startingPosition

  def instantiateDefaultCallbackRoutes(self):
    self.implementedCallbacks:Dict[str,bool]={
      "onCreate":False,
      "onTick":False,
      "onDestroy":False,
      "onTickClassCallback":len(self.tickClassCallbacks)>0
    }

  def onAddedToParent(self,parent:GameObject):
    super().onAddedToParent(parent)

    myPositionSpace:Optional[PositionSpace]= self.searchForRoot(lambda x: isinstance(x,PositionSpace))  # type: ignore
    if myPositionSpace==None:
      raise(PositionedGameObjectNotPartOfPositionSpace(self))
    else:
      self.positionSpace:PositionSpace= myPositionSpace
      myPositionSpace.positionedGameObjects.append(self)

    #find positioned root
    closestPositionedGameObject:Optional[PositionedGameObject]= self.searchForRoot(lambda x: isinstance(x,PositionedGameObject))  # type: ignore
    if not closestPositionedGameObject:
      self.positionedRoot:Union[PositionedGameObject,PositionSpace]= self.positionSpace
    else:
      self.positionedRoot:Union[PositionedGameObject,PositionSpace]= closestPositionedGameObject


  def getAbsolutePosition(self)->ndarray:
    return self.position+self.positionedRoot.getAbsolutePosition()

  def getPositionOfChild(self,child:PositionedGameObject)->ndarray:
    return self.position+child.position
