; The corridor's ceiling. On some trips into the corridor (day 4 on) the ceiling lifts as Jack walks out along it, up to about two metres,
; and its lights go up with it. It never comes down while he is in there; it is put back once he is in the hall again and looking away.
; Everything tagged "ax_rise" (the ceiling slab, the lights, their fixtures) is moved by the same amount.
(event EventBeginPlay
  (bind f_LB (Actor|GetAllActorswithTag :Tag "lb"))
  (for a_LB f_LB (Variables|Default|SetLB a_LB))
  (bind f_S (Actor|GetAllActorsOfClass :ActorClass "/Game/Blueprints/BP_Story.BP_Story_C"))
  (for a_S f_S (Variables|Default|SetStoryRef a_S)))

(event EventTick (DeltaSeconds)
  (bind lb (Variables|Default|GetLB))
  (if (> (.x (Transformation|GetActorLocation :self lb)) 0.5)
    (bind p (Transformation|GetActorLocation :self (Game|GetPlayerPawn :PlayerIndex 0)))
    (bind py (.y p))
    (bind inside (and (> (.z p) 300.0) (< py -700.0)))
    (bind fwdY (.y (Math|Vector|GetForwardVector :InRot (Camera|GetCameraRotation :self (Game|GetPlayerCameraManager :PlayerIndex 0)))))
    (if (and inside (not (Variables|Default|GetWasIn)))
      (Variables|Default|SetRiseMax (select (and (>= (Class|BPStory|GetDay :self (Variables|Default|GetStoryRef)) 4) (< (Math|Random|RandomFloatinRange :Min 0.0 :Max 1.0) 0.55)) (Math|Random|RandomFloatinRange :Min 90.0 :Max 210.0) 0.0)))
    (Variables|Default|SetWasIn inside)
    (bind h0 (Variables|Default|GetH))
    (if inside
      (bind want (* (Variables|Default|GetRiseMax) (Math|Float|Clamp(Float) :Value (/ (- -860.0 py) 500.0) :Min 0.0 :Max 1.0)))
      (Variables|Default|SetH (Math|Float|Max(Float) :A h0 :B (Math|Interpolation|FInterpTo :Current h0 :Target want :DeltaTime DeltaSeconds :InterpSpeed 1.5))))
    (if (and (not inside) (and (> h0 0.0) (> fwdY 0.35))) (Variables|Default|SetH 0.0))
    ; (a bound value is read again each time it is used, so the last height applied is kept in its own variable)
    (bind dh (- (Variables|Default|GetH) (Variables|Default|GetPrev)))
    (if (!= dh 0.0)
      (bind gR (Actor|GetAllActorswithTag :Tag "ax_rise"))
      (for aR gR
        (bind rl (Transformation|GetActorLocation :self aR))
        (Transformation|SetActorLocation :self aR :NewLocation (Math|Vector|MakeVector :X (.x rl) :Y (.y rl) :Z (+ (.z rl) dh))))
      (Variables|Default|SetPrev (Variables|Default|GetH)))))
