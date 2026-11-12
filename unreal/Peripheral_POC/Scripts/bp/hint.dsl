; The objective hint: a faint warm glow on the thing Day One's note is about. The director (BP_HUD) still moves its old
; marker (tag s_hint, now an empty actor); for the four tasks whose places it only knows from the first, smaller house,
; this light goes to the real thing instead: the front door, the fridge, the parents' door, Jack's bed.
(event EventBeginPlay
  (bind f_H (Actor|GetAllActorsOfClass :ActorClass "/Game/Blueprints/BP_HUD.BP_HUD_C")) (for a_H f_H (Variables|Default|SetHudRef a_H))
  (bind f_M (Actor|GetAllActorswithTag :Tag "s_hint")) (for a_M f_M (Variables|Default|SetMarker a_M))
  (bind f_D (Actor|GetAllActorswithTag :Tag "s_door")) (for a_D f_D (Variables|Default|SetDoor a_D))
  (bind f_F (Actor|GetAllActorswithTag :Tag "s_fridge")) (for a_F f_F (Variables|Default|SetFridge a_F))
  (bind f_P (Actor|GetAllActorswithTag :Tag "s_pdoor")) (for a_P f_P (Variables|Default|SetPDoor a_P))
  (bind f_B (Actor|GetAllActorswithTag :Tag "ch_bed")) (for a_B f_B (Variables|Default|SetBed a_B)))

(event EventTick (DeltaSeconds)
  (bind hud (Variables|Default|GetHudRef))
  (bind task (Class|BPHUD|GetTask :self hud))
  (bind up (Math|Vector|MakeVector :X 0.0 :Y 0.0 :Z 100.0))
  (bind loc (select (== task 2) (+ (Transformation|GetActorLocation :self (Variables|Default|GetDoor)) up)
            (select (== task 8) (+ (Transformation|GetActorLocation :self (Variables|Default|GetFridge)) up)
            (select (== task 9) (+ (Transformation|GetActorLocation :self (Variables|Default|GetPDoor)) up)
            (select (>= task 10) (+ (Transformation|GetActorLocation :self (Variables|Default|GetBed)) (Math|Vector|MakeVector :X 0.0 :Y 0.0 :Z 70.0))
                    (Transformation|GetActorLocation :self (Variables|Default|GetMarker)))))))
  (Transformation|SetActorLocation :NewLocation loc)
  (Rendering|SetActorHiddenInGame :bNewHidden (or (!= (Class|BPHUD|GetMode :self hud) 1) (> (Class|BPHUD|GetUnease :self hud) 55.0))))
