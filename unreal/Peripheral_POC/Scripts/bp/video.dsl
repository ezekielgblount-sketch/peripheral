; The home video. A picture in front of the old television's tube in the parents' room, with its glow.
; It comes on when Jack has played the tape (the story's third memory) and keeps playing to the end.
(event EventBeginPlay
  (Rendering|SetActorHiddenInGame :bNewHidden true)
  (bind st (Actor|GetAllActorsOfClass :ActorClass "/Game/Blueprints/BP_Story.BP_Story_C"))
  (for s st (Variables|Default|SetStoryRef s)))

(event EventTick (DeltaSeconds)
  (bind sr (Variables|Default|GetStoryRef))
  (bind on (Class|BPStory|GetM2 :self sr))
  (if (!= on (Variables|Default|GetOn))
    (Variables|Default|SetOn on)
    (Rendering|SetActorHiddenInGame :bNewHidden (not on))
    (bind glow (Actor|GetAllActorswithTag :Tag "st_video_glow"))
    (for g glow (Rendering|SetActorHiddenInGame :self g :bNewHidden (not on)))
    (if on (Audio|PlaySoundatLocation :Sound "/Game/Audio/tv_burst.tv_burst" :Location (Transformation|GetActorLocation) :VolumeMultiplier 0.6 :AttenuationSettings "/Game/Audio/ATT_House.ATT_House"))))
