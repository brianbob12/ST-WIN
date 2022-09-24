from __future__ import annotations
from abc import abstractmethod

from typing import Any, Callable, Dict, List, Optional

from Core.TickClassCallback import TickClassCallback

from Core.Exceptions import InvalidTickClassData


class GameObject:
  __slots__=(
    "children",
    "parent",
    "tickClassCallbacks",
    "name",
    "implementedCallbacks"
  )
  
  def __init__(self,name:Optional[str]=None):
    self.children: List[GameObject]= []
    self.parent: Optional[GameObject]= None
    self.tickClassCallbacks:Dict[TickClassCallback,Callable[[Any],None]]= {}
    self.name:Optional[str]= name
    # onCreate: "onCreate", onTick: "onTick", onDestroy: "onDestroy", onTickClassCallback: "onTickClassCallback"
    self.instantiateDefaultCallbackRoutes()

  @abstractmethod
  def instantiateDefaultCallbackRoutes(self):
    self.implementedCallbacks:Dict[str,bool]={
      "onCreate":False,
      "onTick":False,
      "onDestroy":False,
      "onTickClassCallback":len(self.tickClassCallbacks)>0
    }

     


  def addChild(self,component:GameObject):
    self.children.append(component)
    component.onAddedToParent(self)

    #update implementedCallbacks
    self.implementedCallbacks={
      "onCreate":self.implementedCallbacks["onCreate"] or component.implementedCallbacks["onCreate"],
      "onTick":self.implementedCallbacks["onTick"] or component.implementedCallbacks["onTick"],
      "onDestroy":self.implementedCallbacks["onDestroy"] or component.implementedCallbacks["onDestroy"],
      "onTickClassCallback":self.implementedCallbacks["onTickClassCallback"] or component.implementedCallbacks["onTickClassCallback"]
    }

  def recomputeCallbackRoutes(self):
    self.implementedCallbacks={
      "onCreate":False,
      "onTick":False,
      "onDestroy":False,
      "onTickClassCallback":False
    }

    for child in self.children:
      self.implementedCallbacks={
        "onCreate":self.implementedCallbacks["onCreate"] or child.implementedCallbacks["onCreate"],
        "onTick":self.implementedCallbacks["onTick"] or child.implementedCallbacks["onTick"],
        "onDestroy":self.implementedCallbacks["onDestroy"] or child.implementedCallbacks["onDestroy"],
        "onTickClassCallback":self.implementedCallbacks["onTickClassCallback"] or child.implementedCallbacks["onTickClassCallback"]
      }
    
  def removeChild(self,component:GameObject):
    self.children.remove(component)
    component.parent = None

    #recompute implementedCallbacks
    self.recomputeCallbackRoutes() 

  def implementTickClassCallback(self,tickClassCallback:TickClassCallback, callback:Callable[[Any],None]):
    self.tickClassCallbacks[tickClassCallback]=callback
    self.implementedCallbacks["onTickClassCallback"]=True

  #utility functions

  #NOTE this will return the first root to meet the condition  
  def searchForRoot(self,condition:Callable[[GameObject],bool])->Optional[GameObject]:
    if condition(self):
      return self

    if self.parent is None:
      return None

    return self.parent.searchForRoot(condition)

  def searchForChild(self,condition:Callable[[GameObject],bool])->Optional[GameObject]:
    for child in self.children:
      if condition(child):
        return child
      result = child.searchForChild(condition)
      if result:
        return result

    return None

  def hasDirectChildOfType(self,type:type)-> bool:
    for child in self.children:
      if isinstance(child,type):
        return True

    return False

  def hasChildOfType(self,type:type) -> bool:
    for child in self.children:
      if isinstance(child,type):
        return True

      if child.hasChildOfType(type):
        return True

    return False


  #setup callback

  def onAddedToParent(self,parent:GameObject):
    self.parent=parent

  def onRemovedFromParent(self):
    self.parent=None

  #Game callbacks

  def onCreate(self):
    #call onCreate on all children
    for child in self.children:
      if child.implementedCallbacks["onCreate"]:
        child.onCreate()

  def onTick(self):
    #call onTick on all children
    for child in self.children:
      if child.implementedCallbacks["onTick"]:
        child.onTick()

  def onDestroy(self):
    #call onDestroy on all children
    for child in self.children:
      if child.implementedCallbacks["onDestroy"]:
        child.onDestroy()

  def onTickClassCallback(self, tickClassCallback:TickClassCallback,data:Any):


    #call the tickClassCallback if supported
    try:
      self.tickClassCallbacks[tickClassCallback](data)

    except KeyError:
      return
    #NOTE there is no need to verify the type of data because it was verified in the broadcaster

    #call onTickClassCallback on all children
    for child in self.children:
      if child.implementedCallbacks["onTickClassCallback"]:
        child.onTickClassCallback(tickClassCallback,data)

  
  


