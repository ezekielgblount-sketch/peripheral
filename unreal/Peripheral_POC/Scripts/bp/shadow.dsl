; Jack's shadow. This actor is a plain figure that is never drawn; only its shadow is. It stands exactly where he does, so
; lamps and the sun give him a shadow. When the house is unstable (the loop is running) and he stands still for a few
; seconds, the shadow stops copying him: it turns, steps aside and lifts an arm. The moment he moves it is his again.
; H forces the same thing anywhere, for testing.
(event EventBeginPlay
  (bind f_LB (Actor|GetAllActorswithTag :Tag "lb"))
  (for a_LB f_LB (Variables|Default|SetLB a_LB)))

(event EventTick (DeltaSeconds)
  (bind pc (Game|GetPlayerController :PlayerIndex 0))
  (bind pawn (Game|GetPlayerPawn :PlayerIndex 0))
  (bind p (Transformation|GetActorLocation :self pawn))
  (bind speed (Math|Vector|VectorLengthXY (Transformation|GetVelocity :self pawn)))
  (if (Game|Player|WasInputKeyJustPressed :self pc :Key "H") (Variables|Default|SetForce (not (Variables|Default|GetForce))))
  ; no figure (so no shadow) while the camera is not Jack: title screen, the drive in, cut scenes
  (Rendering|SetActorHiddenInGame :bNewHidden (Input|IsMoveInputIgnored :self pc))
  (Variables|Default|SetStill (select (and (< speed 5.0) (not (Input|IsMoveInputIgnored :self pc))) (+ (Variables|Default|GetStill) DeltaSeconds) 0.0))
  (bind loose (or (and (Variables|Default|GetForce) (> (Variables|Default|GetStill) 1.0))
                  (and (> (.x (Transformation|GetActorLocation :self (Variables|Default|GetLB))) 0.5) (> (Variables|Default|GetStill) 4.0))))
  (Variables|Default|SetA (Math|Interpolation|FInterpTo :Current (Variables|Default|GetA) :Target (select loose 1.0 0.0) :DeltaTime DeltaSeconds :InterpSpeed (select loose 0.7 7.0)))
  (bind a (Variables|Default|GetA))
  (bind yaw (.yaw (Transformation|GetActorRotation :self pawn)))
  (bind rt (Transformation|GetActorRightVector :self pawn))
  (bind fw (Transformation|GetActorForwardVector :self pawn))
  (Transformation|SetActorLocationAndRotation
    :NewLocation (Math|Vector|MakeVector :X (+ (.x p) (- (* (.x rt) (* 28.0 a)) (* (.x fw) (* 0.0 a)))) :Y (+ (.y p) (- (* (.y rt) (* 28.0 a)) (* (.y fw) (* 0.0 a)))) :Z (- (.z p) 91.0))
    :NewRotation (Math|Rotator|MakeRotator :Roll 0.0 :Pitch 0.0 :Yaw (+ yaw (* 40.0 a))))
  (bind want (select (> a 0.45) 1 0))
  (if (!= want (Variables|Default|GetShown))
    (if (== want 1)
      (Components|StaticMesh|SetStaticMesh :self (Variables|StaticMeshActor|GetStaticMeshComponent) :NewMesh "/Game/Meshes/SM_shadow_body_alt.SM_shadow_body_alt")
      (else (Components|StaticMesh|SetStaticMesh :self (Variables|StaticMeshActor|GetStaticMeshComponent) :NewMesh "/Game/Meshes/SM_shadow_body.SM_shadow_body")))
    (Variables|Default|SetShown want)))
