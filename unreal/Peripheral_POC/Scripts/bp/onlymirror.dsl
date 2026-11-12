; Someone who is only there in the mirror. Its mesh is set "owner cannot see"; the owner is Jack, so his own eyes never
; draw it, but the mirror's camera does. The story switches this actor's tick on from the day it should appear.
(event EventBeginPlay
  (Rendering|SetActorHiddenInGame :bNewHidden true))

(event EventTick (DeltaSeconds)
  (Actor|SetOwner :NewOwner (Game|GetPlayerCharacter :PlayerIndex 0))
  (Rendering|SetActorHiddenInGame :bNewHidden false))
