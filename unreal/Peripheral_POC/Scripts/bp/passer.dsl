; Movement in a doorway. Someone crosses an opening at the far end of a view, once, while it is off to the side of where
; Jack is looking (never in the centre of the screen), then is gone for minutes. It walks from where it was placed to B.
(event EventBeginPlay
  (Variables|Default|SetA (Transformation|GetActorLocation))
  (Variables|Default|SetCool (Math|Random|RandomFloatinRange :Min 40.0 :Max 120.0))
  (Rendering|SetActorHiddenInGame :bNewHidden true))

(event EventTick (DeltaSeconds)
  (bind pcm (Game|GetPlayerCameraManager :PlayerIndex 0))
  (bind camLoc (Camera|GetCameraLocation :self pcm))
  (bind fwd (Math|Vector|GetForwardVector :InRot (Camera|GetCameraRotation :self pcm)))
  (bind a (Variables|Default|GetA))
  (bind b (Variables|Default|GetB))
  (bind mid (+ (* (+ a b) 0.5) (Math|Vector|MakeVector :X 0.0 :Y 0.0 :Z 120.0)))
  (bind to (- mid camLoc))
  (bind dist (+ (Math|Vector|VectorLength :A to) 0.001))
  (bind ang (Math|Trig|Acos(Degrees) :A (/ (Math|Vector|DotProduct :A fwd :B to) dist)))
  (if (Variables|Default|GetMoving)
    (bind t (+ (Variables|Default|GetT) DeltaSeconds))
    (Variables|Default|SetT t)
    (bind f (Math|Float|Clamp(Float) :Value (/ t (Variables|Default|GetTime)) :Min 0.0 :Max 1.0))
    (Transformation|SetActorLocation :NewLocation (+ a (* (- b a) f)))
    (if (>= f 1.0)
      (Variables|Default|SetMoving false)
      (Rendering|SetActorHiddenInGame :bNewHidden true)
      (Transformation|SetActorLocation :NewLocation a)
      (Variables|Default|SetCool (Math|Random|RandomFloatinRange :Min 150.0 :Max 300.0)))
    (else
      (if (> (Variables|Default|GetCool) 0.0)
        (Variables|Default|SetCool (- (Variables|Default|GetCool) DeltaSeconds))
        (else
          (if (and (and (> dist (Variables|Default|GetMinDist)) (< dist (Variables|Default|GetRange))) (and (> ang 20.0) (< ang 48.0)))
            (Variables|Default|SetMoving true) (Variables|Default|SetT 0.0)
            (Rendering|SetActorHiddenInGame :bNewHidden false)))))))
