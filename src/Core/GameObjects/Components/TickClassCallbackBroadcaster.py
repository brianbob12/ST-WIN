from Core.TickClassCallback import TickClassCallback
from Core.Exceptions import ComponentHasNoParent
from .Component import Component
from ..GameObject import GameObject
from typing import Dict, Optional

class TickClassCallbackBroadcaster(Component):
  __slots__=("tickClassCallback")
  def __init__(self,tickClassCallback:TickClassCallback, name: Optional[str] = None):
    self.tickClassCallback=tickClassCallback
    super().__init__(name)

  def instantiateDefaultCallbackRoutes(self):
    self.implementedCallbacks:Dict[str,bool]={
      "onCreate":True,
      "onTick":False,
      "onDestroy":False,
      "onTickClassCallback":False
    }

  def onAddedToParent(self, parent: GameObject):
    # add tickClassCallback to parent so that it calls its children
    parent.implementTickClassCallback(self.tickClassCallback,lambda data: None)
    
    return super().onAddedToParent(parent)

  def broadcast(self,data):
    if self.parent != None:
      self.parent.onTickClassCallback(self.tickClassCallback,data)
    else:
      raise(ComponentHasNoParent(self))