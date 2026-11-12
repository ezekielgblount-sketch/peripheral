; Jack's forearms in first person. Two of these (Side 1 right, -1 left) hold the arm meshes cut from his body just below
; the camera and bring them up into view while he carries, pushes or inspects something; the right one also reaches out
; for a moment when he presses Use.
(event EventBeginPlay
  (bind f (Actor|GetAllActorsOfClass :ActorClass "/Game/Blueprints/BP_Player.BP_Player_C"))
  (for p f (Variables|Default|SetPlayerRef p)))

(event EventTick (DeltaSeconds)
  (bind pc (Game|GetPlayerController :PlayerIndex 0))
  (bind pl (Variables|Default|GetPlayerRef))
  (bind cm (Game|GetPlayerCameraManager :PlayerIndex 0))
  (bind cl (Camera|GetCameraLocation :self cm))
  (bind cr (Camera|GetCameraRotation :self cm))
  (bind fw (Math|Vector|GetForwardVector :InRot cr))
  (bind rt (Math|Vector|GetRightVector :InRot cr))
  (bind up (Math|Vector|GetUpVector :InRot cr))
  (bind side (Variables|Default|GetSide))
  (bind frozen (Input|IsMoveInputIgnored :self pc))
  (if (and (> side 0.0) (and (not frozen) (Game|Player|WasInputKeyJustPressed :self pc :Key (Class|BPPlayer|GetKUse :self pl))))
    (Variables|Default|SetReach 0.4))
  (Variables|Default|SetReach (- (Variables|Default|GetReach) DeltaSeconds))
  (bind busy (or (Class|BPPlayer|GetCarrying :self pl) (or (Class|BPPlayer|GetPushing :self pl) (Class|BPPlayer|GetInspecting :self pl))))
  (bind want (and (not frozen) (or busy (> (Variables|Default|GetReach) 0.0))))
  (Variables|Default|SetA (Math|Interpolation|FInterpTo :Current (Variables|Default|GetA) :Target (select want 1.0 0.0) :DeltaTime DeltaSeconds :InterpSpeed 9.0))
  (bind a (Variables|Default|GetA))
  (Rendering|SetActorHiddenInGame :bNewHidden (< a 0.04))
  (Transformation|SetActorLocationAndRotation
    :NewLocation (Math|Vector|MakeVector :X (+ (.x cl) (+ (* (.x fw) (+ 6.0 (* 30.0 a))) (+ (* (.x rt) (* side (- 27.0 (* 5.0 a)))) (* (.x up) (- (* 12.0 a) 40.0))))) :Y (+ (.y cl) (+ (* (.y fw) (+ 6.0 (* 30.0 a))) (+ (* (.y rt) (* side (- 27.0 (* 5.0 a)))) (* (.y up) (- (* 12.0 a) 40.0))))) :Z (+ (.z cl) (+ (* (.z fw) (+ 6.0 (* 30.0 a))) (+ (* (.z rt) (* side (- 27.0 (* 5.0 a)))) (* (.z up) (- (* 12.0 a) 40.0))))))
    :NewRotation (Math|Rotator|MakeRotfromXY :X (Math|Vector|MakeVector :X (+ (.x fw) (+ (* (.x rt) (* side -0.20)) (* (.x up) 0.16))) :Y (+ (.y fw) (+ (* (.y rt) (* side -0.20)) (* (.y up) 0.16))) :Z (+ (.z fw) (+ (* (.z rt) (* side -0.20)) (* (.z up) 0.16)))) :Y up)))
