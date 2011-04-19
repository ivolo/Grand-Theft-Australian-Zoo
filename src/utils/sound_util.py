import os
import pygame

class SoundUtil:

    sounds = {}
    stop_sounds = []
    Comment = ""
        
    sound_on = True
        
    def LoadSound(self,filename,cue_name=None):
            """Load a sound into memory, not just its name, for quick use."""
            new_sound = pygame.mixer.Sound( os.path.join("sounds",filename) )
            if not cue_name:
                cue_name = filename
            if cue_name in self.sounds:
                self.stop_sounds.append( self.sounds[ cue_name ] )
            self.sounds[ cue_name ] = new_sound
     
    def PlaySound(self,cue_name):
        ## How to check whether sound player is busy?
        for sound in self.stop_sounds:
            sound.stop()
        self.stop_sounds = []
        if cue_name in self.sounds and self.sound_on:
            self.sounds[ cue_name ].play()
        elif self.sound_on:
            self.Comment("Tried to play sound '"+cue_name+"' without loading it.")
            pass
        
    def StopSound(self, cue_name):
        self.sounds[cue_name].stop()