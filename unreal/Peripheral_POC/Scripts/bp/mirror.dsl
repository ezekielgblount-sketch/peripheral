; A mirror that shows Jack. This actor is a camera behind the wall: each frame the player is near and in front of the
; glass it moves to where his eye would be if the wall were a window (his eye mirrored through the glass), looks back at
; the centre of the mirror and films the room, Jack's whole body included, into a small picture drawn on the glass.
; The body he sees in first person (no head) and his forearms are left out of that picture.
(event EventBeginPlay
  (bind c (Variables|DecalActor|GetCaptureComponent2D))
  (bind fp (Actor|GetAllActorswithTag :Tag "jack_fp"))
  (for a fp (Rendering|SceneCapture|HideActorComponents :self c :InActor a)))

(event EventTick (DeltaSeconds)
  (bind c (Variables|DecalActor|GetCaptureComponent2D))
  (bind cm (Game|GetPlayerCameraManager :PlayerIndex 0))
  (bind e (Camera|GetCameraLocation :self cm))
  (bind C (Variables|Default|GetC))
  (bind N (Variables|Default|GetN))
  (bind rel (Math|Vector|MakeVector :X (- (.x e) (.x C)) :Y (- (.y e) (.y C)) :Z (- (.z e) (.z C))))
  (bind d (Math|Vector|DotProduct :A rel :B N))
  (bind D (Math|Vector|VectorLength :A rel))
  (bind cf (Math|Vector|GetForwardVector :InRot (Camera|GetCameraRotation :self cm)))
  ; only while he is in front of the glass, within 4.5 m, and it is somewhere in his view (it costs a second picture of the room)
  (bind active (and (and (and (> d 25.0) (< D 450.0)) (< (* (.z rel) (.z rel)) 16900.0)) (< (Math|Vector|DotProduct :A rel :B cf) (* -0.35 D))))
  (Class|SceneCaptureComponent|SetCaptureEveryFrame :self c :bCaptureEveryFrame active)
  (if active
    (bind m (Math|Vector|MakeVector :X (- (.x e) (* (* 2.0 d) (.x N))) :Y (- (.y e) (* (* 2.0 d) (.y N))) :Z (- (.z e) (* (* 2.0 d) (.z N)))))
    (Transformation|SetActorLocationAndRotation :NewLocation m :NewRotation (Math|Rotator|FindLookatRotation :Start m :Target C))
    (Class|SceneCaptureComponent2D|SetFieldofView :self c :FOVAngle (* 2.0 (Math|Trig|Atan(Degrees) :A (/ 60.0 D))))
    (Class|SceneCaptureComponent2D|SetCustomNearClippingPlane :self c :CustomNearClippingPlane (+ (+ D 3.0) (* 52.0 (Math|Float|Sqrt :A (- 1.0 (* (/ d D) (/ d D)))))))))
