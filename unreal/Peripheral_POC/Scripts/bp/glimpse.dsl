; A figure seen only out of the corner of the eye, through glass or down a long view (no wall test, so it works through windows).
; It stands there while Jack is at a distance and not looking at it. Looked at directly for a moment, it is gone, and stays gone for a while.
(event EventBeginPlay
  (Rendering|SetActorHiddenInGame :bNewHidden true))

(event EventTick (DeltaSeconds)
  (bind pcm (Game|GetPlayerCameraManager :PlayerIndex 0))
  (bind camLoc (Camera|GetCameraLocation :self pcm))
  (bind fwd (Math|Vector|GetForwardVector :InRot (Camera|GetCameraRotation :self pcm)))
  (bind to (- (+ (Transformation|GetActorLocation) (Math|Vector|MakeVector :X 0.0 :Y 0.0 :Z 120.0)) camLoc))
  (bind dist (+ (Math|Vector|VectorLength :A to) 0.001))
  (bind ang (Math|Trig|Acos(Degrees) :A (/ (Math|Vector|DotProduct :A fwd :B to) dist)))
  (bind cool (Variables|Default|GetCool))
  (bind inrange (and (< dist (Variables|Default|GetRange)) (> dist (Variables|Default|GetMinDist))))
  (if (> cool 0.0)
    (Variables|Default|SetCool (- cool DeltaSeconds))
    (else
      (if (not inrange)
        (Rendering|SetActorHiddenInGame :bNewHidden true) (Variables|Default|SetUp false) (Variables|Default|SetT 0.0)
        (else
          (if (> ang 17.0)
            (Rendering|SetActorHiddenInGame :bNewHidden false) (Variables|Default|SetUp true) (Variables|Default|SetT 0.0)
            (else
              (if (Variables|Default|GetUp)
                (Variables|Default|SetT (+ (Variables|Default|GetT) DeltaSeconds))
                (if (>= (Variables|Default|GetT) 0.16)
                  (Rendering|SetActorHiddenInGame :bNewHidden true) (Variables|Default|SetUp false) (Variables|Default|SetT 0.0)
                  (Variables|Default|SetCool (Math|Random|RandomFloatinRange :Min 90.0 :Max 170.0)))))))))))
