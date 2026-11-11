(event EventTick (DeltaSeconds)
  (bind pc (Game|GetPlayerController :PlayerIndex 0))
  ; --- walk ---
  (bind fwd (- (select (Game|Player|IsInputKeyDown :self pc :Key "W") 1.0 0.0)
               (select (Game|Player|IsInputKeyDown :self pc :Key "S") 1.0 0.0)))
  (bind side (- (select (Game|Player|IsInputKeyDown :self pc :Key "D") 1.0 0.0)
                (select (Game|Player|IsInputKeyDown :self pc :Key "A") 1.0 0.0)))
  (Pawn|Input|AddMovementInput :WorldDirection (Transformation|GetActorForwardVector) :ScaleValue fwd)
  (Pawn|Input|AddMovementInput :WorldDirection (Transformation|GetActorRightVector) :ScaleValue side)
  ; --- look ---
  (bind (dx dy) (Game|Player|GetInputMouseDelta :self pc))
  (Pawn|Input|AddControllerYawInput :Val (* dx 1.2))
  (Pawn|Input|AddControllerPitchInput :Val (* dy -1.2))
  ; --- flashlight ---
  (if (Game|Player|WasInputKeyJustPressed :self pc :Key "F")
    (Rendering|ToggleVisibility :self (Variables|Default|GetFlashlight))))
