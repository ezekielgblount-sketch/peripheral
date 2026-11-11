(event Game|Damage|EventAnyDamage (Damage DamageType InstigatedBy DamageCauser)
  (Audio|PlaySoundatLocation :Sound "/Game/Audio/box_thump.box_thump" :Location (Transformation|GetActorLocation) :VolumeMultiplier 0.5)
  (Actor|DestroyActor))
