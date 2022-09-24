
from typing import Any
from Core.TickClassCallback import TickClassCallback


class InvalidTickClassData(Exception):
  def __init__(self, tickClassCallback:TickClassCallback, data:Any):
    self.tickClassCallback:TickClassCallback = tickClassCallback
    self.data:Any = data

  def __str__(self):
    return f"Invalid tickClassCallback data: {self.data} is not of type {self.tickClassCallback.dataArgType}"
    

class ComponentsCannotHaveChildren(Exception):
  def __init__(self, component):
    self.component = component

  def __str__(self):
    return f"Component {self.component} cannot have children"

class ComponentHasNoParent(Exception):
  def __init__(self, component):
    self.component = component

  def __str__(self):
    return f"Component {self.component} has no parent"

class PositionedGameObjectNotPartOfPositionSpace(Exception):
  def __init__(self, positionedGameObject):
    self.positionedGameObject = positionedGameObject

  def __str__(self):
    return f"PositionedGameObject {self.positionedGameObject} is not part of a position space"