from abc import abstractmethod
from typing import Any, Dict, Optional

from Core.TickClassCallback import TickClassCallback
from Core.Exceptions import ComponentHasNoParent, ComponentsCannotHaveChildren, InvalidTickClassData
from ..GameObject import GameObject

#component has no children and must have a parent
class Component(GameObject):

  def __init__(self, name: Optional[str] = None):
    super().__init__(name)

  @abstractmethod
  def instantiateDefaultCallbackRoutes(self):
    self.implementedCallbacks:Dict[str,bool]={
      "onCreate":True,
      "onTick":False,
      "onDestroy":False,
      "onTickClassCallback":len(self.tickClassCallbacks)>0
    }

  #override addChild to not allow children
  def addChild(self,component:GameObject):
    raise(ComponentsCannotHaveChildren(self))

  #override callbacks to not call children
  def onCreate(self):
    #check if there is a parent
    if self.parent == None:
      raise(ComponentHasNoParent(self))
    #do not attempt to call children

  def onTick(self):
    pass

  def onDestroy(self):
    pass

  def onFixedTick(self,tickClassCallback:TickClassCallback,data:Any):
    #perform typeCheck
    if type(data) is not tickClassCallback.dataArgType:
      raise(InvalidTickClassData(tickClassCallback,data))

    #call the tickClassCallback if supported
    try:
      self.tickClassCallbacks[tickClassCallback](data)

    except KeyError:
      return


  