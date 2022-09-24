from typing import List, Optional

from Core.Components.TickClassCallbackBroadcaster import TickClassCallbackBroadcaster

class TickClassCallback:

  __slots__=(
    "name",
    "dataArgType",
    "broadcasters"
    )

  def __init__(self,dataArgType:type, name:Optional[str]=None):
    self.name=name
    self.dataArgType:type = dataArgType
    self.broadcasters:List[TickClassCallbackBroadcaster] = []

  def broadcast(self,data):
    for broadcaster in self.broadcasters:
      broadcaster.broadcast(data)


    
