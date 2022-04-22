
from gameobs.GameObject import *

class Enemy( GameObject ):
    
    def __init__( self, pos, modelName, modelAnims, maxHealth, maxSpeed, colliderName ):
        GameObject.__init__( self, pos, modelName, modelAnims, maxHealth, maxSpeed, colliderName )

        self.scoreValue = 1

    def update( self, player, dt ):

        GameObject.update( self, dt )

        self.runLogic( player, dt )

        if self.walking:
            
            walkingControl = self.actor.getAnimControl( "walk" )
            if not walkingControl.isPlaying():
                self.actor.loop( "walk" )

        else:

            spawnControl =self.actor.getAnimControl( "spawn" )
            if spawnControl is None or not spawnControl.isPlaying():
                attackControl = self.actor.getAnimControl( "attack" )
                if attackControl is None or not attackControl.isPlaying():
                    standControl = self.actor.getAnimControl( "stand" )
                    if not standControl.isPlaying():
                        self.actor.loop( "stand" )

    def runLogic( self, player, dt ):
        pass
