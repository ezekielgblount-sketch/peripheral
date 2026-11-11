(event EventBeginPlay
  ; a door can be placed already open in the editor: work back to its closed pose
  (bind o (select (Variables|Default|GetOpen) 1.0 0.0))
  (bind r0 (Transformation|GetActorRotation))
  (bind cr (Math|Rotator|MakeRotator :Roll (.roll r0) :Pitch (.pitch r0) :Yaw (- (.yaw r0) (* (Variables|Default|GetOpenYaw) o))))
  (Variables|Default|SetClosedRot cr)
  (Variables|Default|SetClosedLoc (- (Transformation|GetActorLocation) (Math|Vector|RotateVector :A (* (Variables|Default|GetSlide) o) :B cr)))
  (Variables|Default|SetAlpha o))

(event Game|Damage|EventAnyDamage (Damage DamageType InstigatedBy DamageCauser)
  (bind stick (Variables|Default|GetStickCount))
  (if (or (Variables|Default|GetLocked) (> stick 0))
    (Variables|Default|SetStickCount (- stick 1))
    (Audio|PlaySoundatLocation :Sound (Variables|Default|GetSndLocked) :Location (Transformation|GetActorLocation))
    (else
      (Variables|Default|SetOpen (not (Variables|Default|GetOpen)))
      (Audio|PlaySoundatLocation :Sound (Variables|Default|GetSndOpen) :Location (Transformation|GetActorLocation)
                                 :PitchMultiplier (Math|Random|RandomFloatinRange :Min 0.85 :Max 1.1)))))

(event EventTick (DeltaSeconds)
  (bind a (Math|Interpolation|FInterpTo :Current (Variables|Default|GetAlpha)
                                        :Target (select (Variables|Default|GetOpen) 1.0 0.0)
                                        :DeltaTime DeltaSeconds :InterpSpeed (Variables|Default|GetSpeed)))
  (Variables|Default|SetAlpha a)
  (bind r (Variables|Default|GetClosedRot))
  (Transformation|SetActorLocationAndRotation
    :NewLocation (+ (Variables|Default|GetClosedLoc) (Math|Vector|RotateVector :A (* (Variables|Default|GetSlide) a) :B r))
    :NewRotation (Math|Rotator|MakeRotator :Roll (.roll r) :Pitch (.pitch r) :Yaw (+ (.yaw r) (* (Variables|Default|GetOpenYaw) a)))))
