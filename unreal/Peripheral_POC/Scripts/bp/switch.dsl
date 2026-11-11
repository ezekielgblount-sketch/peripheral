; A lamp or a wall switch. E toggles it; the lights (and lit / unlit fixture meshes) tagged with its group follow.
; Nothing lights until the breaker has reached this switch's stage (the blackboard actor's Z is the power stage).
(event EventBeginPlay
  (Variables|Default|SetShown -1)
  (bind f_BB (Actor|GetAllActorswithTag :Tag "bb"))
  (for a_BB f_BB (Variables|Default|SetBB a_BB)))

(event Game|Damage|EventAnyDamage (Damage DamageType InstigatedBy DamageCauser)
  (Variables|Default|SetOn (not (Variables|Default|GetOn)))
  (Audio|PlaySoundatLocation :Sound "/Game/Audio/click.click" :Location (Transformation|GetActorLocation) :VolumeMultiplier 0.6))

(event EventTick (DeltaSeconds)
  (bind power (.z (Transformation|GetActorLocation :self (Variables|Default|GetBB))))
  (bind lit (and (Variables|Default|GetOn) (>= power (Math|Conversions|ToFloat(Integer) (Variables|Default|GetStage)))))
  (bind want (select lit 1 0))
  (if (!= want (Variables|Default|GetShown))
    (Variables|Default|SetShown want)
    (bind g (Actor|GetAllActorswithTag :Tag (Variables|Default|GetGroup)))
    (for a g (Rendering|SetActorHiddenInGame :self a :bNewHidden (not lit)))
    (bind g2 (Actor|GetAllActorswithTag :Tag (Variables|Default|GetGroupOff)))
    (for a2 g2 (Rendering|SetActorHiddenInGame :self a2 :bNewHidden lit))
    (if lit
      (Components|StaticMesh|SetStaticMesh :self (Variables|StaticMeshActor|GetStaticMeshComponent) :NewMesh (Variables|Default|GetMeshOn))
      (else
        (Components|StaticMesh|SetStaticMesh :self (Variables|StaticMeshActor|GetStaticMeshComponent) :NewMesh (Variables|Default|GetMeshOff))))))
