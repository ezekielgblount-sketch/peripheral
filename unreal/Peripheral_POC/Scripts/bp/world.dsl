(event EventBeginPlay
  (Audio|PlaySound2D :Sound (Variables|Default|GetSndTone) :VolumeMultiplier 0.6))

; N = day/night. 1 / 2 / 3 = low / medium / high graphics quality.
(event EventTick (DeltaSeconds)
  (bind pc (Game|GetPlayerController :PlayerIndex 0))
  (if (Game|Player|WasInputKeyJustPressed :self pc :Key "N")
    (bind night (not (Variables|Default|GetNight)))
    (Variables|Default|SetNight night)
    (Rendering|Material|SetScalarParameterValue :Collection "/Game/Materials/MPC_World.MPC_World" :ParameterName "Night"
                                                :ParameterValue (select night 1.0 0.0))
    (bind nl (Actor|GetAllActorswithTag :Tag "night_light"))
    (for a nl
      (Rendering|SetActorHiddenInGame :self a :bNewHidden (not night)))
    (bind dl (Actor|GetAllActorswithTag :Tag "day_light"))
    (for b dl
      (Rendering|SetActorHiddenInGame :self b :bNewHidden night)))
  (if (Game|Player|WasInputKeyJustPressed :self pc :Key "One")
    (Development|ExecuteConsoleCommand :Command "Scalability 1")
    (Development|ExecuteConsoleCommand :Command "r.ScreenPercentage 60"))
  (if (Game|Player|WasInputKeyJustPressed :self pc :Key "Two")
    (Development|ExecuteConsoleCommand :Command "Scalability 2")
    (Development|ExecuteConsoleCommand :Command "r.ScreenPercentage 75"))
  (if (Game|Player|WasInputKeyJustPressed :self pc :Key "Three")
    (Development|ExecuteConsoleCommand :Command "Scalability 3")
    (Development|ExecuteConsoleCommand :Command "r.ScreenPercentage 100")))
